import os
from xml_generation.csv_to_xml_converter import CSVtoXMLConverter
from xml_generation.validacao import validar_xml_com_schema
from lxml import etree

def generate_and_validate_xml(file_name, csv_path):
    try:
        # Chama a função para converter CSV para XML
        converter = CSVtoXMLConverter(csv_path)
        xml_str = converter.to_xml_str()

        # Validar XML
        validar_xml_com_schema(xml_str)

        save_path = "/src/rpc-base_dados/data"

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        xml_save_path = os.path.join(save_path, f"{file_name}.xml")
        with open(xml_save_path, 'w') as xml_file:
            xml_file.write(xml_str)

        return xml_str

    except Exception as e:
        print(f"Erro durante a geração e validação do XML: {e}")
        return None
