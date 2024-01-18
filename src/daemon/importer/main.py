import time
import uuid
import csv
import math
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from base_dados.bd import insert_xml_data, get_all_active_csv, insert_csv_data

from utils.csv_to_xml_converter import CSVtoXMLConverter
from utils.xml_process import generate_and_validate_xml

NUM_XML_PARTS_str = os.getenv("NUM_XML_PARTS", "3")

if not NUM_XML_PARTS_str:
    NUM_XML_PARTS_str = "3"

NUM_XML_PARTS = int(NUM_XML_PARTS_str)

CSV_INPUT_PATH = "/csv"
XML_OUTPUT_PATH = "/xml"

def split_csv(file_path, num_parts):
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        total_rows = sum(1 for row in csv_reader)

    rows_per_part = int(math.ceil(total_rows / num_parts))

    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        for part_num in range(num_parts):
            part_rows = []
            for _ in range(rows_per_part):
                try:
                    part_rows.append(next(csv_reader))
                except StopIteration:
                    break

            part_file_path = f"{file_path}_part{part_num + 1}.csv"
            with open(part_file_path, 'w', newline='') as part_file:
                csv_writer = csv.writer(part_file)
                csv_writer.writerow(header)
                csv_writer.writerows(part_rows)

            yield part_file_path

def store_csv(csv_path):
    try:
        with open(csv_path, 'rb') as csv_file:
            csv_content = csv_file.read()
        csv_size = os.path.getsize(csv_path)
        csv_filename = os.path.basename(csv_path)

        result = insert_csv_data(csv_filename, csv_content, csv_size)
        if result:
            print(f"Inserção bem-sucedida no banco de dados para CSV: {csv_filename}")
            return True
        return False
    except FileNotFoundError:
        print(f"Erro: O arquivo CSV não foi encontrado: {csv_path}")
        return True
    except Exception as e:
        print(f"Erro durante a inserção no banco de dados para CSV: {e}")
        return True

def store_xml(xml_path, xml_data):
    try:
        insert_xml_data(xml_path, xml_data)
        print(f"Inserção bem-sucedida no banco de dados para XML: {os.path.basename(xml_path)}")
    except Exception as e:
        print(f"Erro durante a inserção no banco de dados para XML: {e}")

def generate_unique_file_name(directory, extension):
    return f"{directory}/{str(uuid.uuid4())[:8]}.{extension}"


def convert_csv_to_xml(in_path, out_path):
    print(f"Converting CSV: {in_path}")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    try:
        converter = generate_and_validate_xml(in_path)

        if isinstance(converter, CSVtoXMLConverter):
            with open(out_path, "w") as file:
                file.write(converter.to_xml_str())
            print("Conversion completed.")
        else:
            print("Erro: O objeto converter não é do tipo esperado.")
            return None
    except Exception as e:
        print(f"Erro durante a geração e validação do XML: {e}")
        return None

    return out_path


class CSVHandler(FileSystemEventHandler):
    def __init__(self, input_path, output_path):
        self._output_path = output_path
        self._input_path = input_path

    def on_created(self, event):
        print(f"File created: {event.src_path}")
        if not event.is_directory and event.src_path.endswith(".csv"):
            self.process_csv(event.src_path)

    def process_csv(self, csv_path):
        csv_filename = os.path.basename(csv_path)

        existing_record = store_csv(csv_path)
        print(f"'{existing_record}'")

        if not existing_record:
            print(f"CSV '{csv_filename}' já existe no banco de dados. Ignorando o processamento.")
            return

        print(f"Starting splitting for CSV: {csv_path} into {NUM_XML_PARTS} parts")

        for part_num in range(NUM_XML_PARTS):
            print(f"Starting conversion for CSV part: {part_num + 1}")
            xml_path = generate_unique_file_name(XML_OUTPUT_PATH, "xml")

            converted_path = convert_csv_to_xml(csv_path, xml_path)

            if converted_path:
                print(f"New XML file generated: '{converted_path}'")

                with open(converted_path, 'r') as xml_file:
                    xml_data = xml_file.read()

                store_xml(converted_path, xml_data)
                print(f"Conversion completed for CSV part: {part_num + 1}")


if __name__ == "__main__":
    if not os.path.exists(CSV_INPUT_PATH):
        os.makedirs(CSV_INPUT_PATH)

    if not os.path.exists(XML_OUTPUT_PATH):
        os.makedirs(XML_OUTPUT_PATH)

    observer = Observer()
    handler = CSVHandler(CSV_INPUT_PATH, XML_OUTPUT_PATH)
    observer.schedule(handler, path=CSV_INPUT_PATH, recursive=True)
    observer.start()

    try:
        print("Observer started. Waiting for CSV files...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Observer stopped by the user.")
    except Exception as e:
        print(f"Erro inesperado durante a execução do Observer: {e}")
    finally:
        observer.stop()
        observer.join()
