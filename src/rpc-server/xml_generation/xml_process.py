import tempfile
from csv_to_xml_converter import CSVtoXMLConverter
from validacao import validar_xml_com_schema

def generate_and_validate_xml(csv_file="cars.csv"):

    converter = CSVtoXMLConverter(csv_file)
    xml_str = converter.to_xml_str()
    print(xml_str)

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_xml_file:
        temp_xml_file.write(xml_str)
        temp_xml_filename = temp_xml_file.name

    try:
        validar_xml_com_schema(temp_xml_filename, "schema.xsd")
        print("O XML é válido de acordo com a XML Schema fornecida.")
    finally:
        import os
        os.remove(temp_xml_filename)

    output_text_file = "output.txt"
    with open(output_text_file, "w") as output_file:
        output_file.write(xml_str)

    print(f"O XML foi salvo em {output_text_file}")

    return True

if __name__ == "__main__":
    generate_and_validate_xml()

