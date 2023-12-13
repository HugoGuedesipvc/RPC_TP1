from lxml import etree
from io import StringIO


def validar_xml_com_schema(xml_str):
    try:
        # Carregar o XML e o Schema
        xml_doc = etree.parse(StringIO(xml_str))

        # Use um caminho absoluto ou ajuste conforme necessário
        schema_path = "/app/xml_generation/schema.xsd"
        xml_schema_doc = etree.parse(schema_path)

        # Criar um validador com base na Schema
        xml_schema = etree.XMLSchema(xml_schema_doc)

        # Validar o XML
        xml_schema.assertValid(xml_doc)

        print("XML validado com sucesso usando o XML Schema.")

    except etree.XMLSchemaError as e:
        print(f"Erro na validação da XML Schema: {e}")
    except etree.DocumentInvalid as e:
        print(f"Erro na validação do XML: {e}")
