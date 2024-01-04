from .csv_to_xml_converter import CSVtoXMLConverter
from .validacao import validar_xml_com_schema

def generate_and_validate_xml(csv_path):
    try:
        # Chama a função para converter CSV para XML
        converter = CSVtoXMLConverter(csv_path)
        xml_str = converter.to_xml_str()

        # Validar XML
        validar_xml_com_schema(xml_str)

        # Retorna a instância do conversor em vez da string
        return converter

    except Exception as e:
        print(f"Erro durante a geração e validação do XML: {e}")
        return None
