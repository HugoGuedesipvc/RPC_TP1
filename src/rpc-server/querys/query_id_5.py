from lxml import etree

def count_cars_by_brand(xml):

    brand = "BMW"

    try:
        tree = etree.fromstring(xml)
        car_count = len(tree.xpath(f"/Data/Cars/Car[contains(@brand, '{brand}')]"))

        result = f"Número de carros da marca '{brand}': {car_count}"
        return [result]
    except etree.XMLSyntaxError as syntax_error:
        print(f"Erro de sintaxe XML na consulta count_cars_by_brand: {syntax_error}")
        return []
    except Exception as e:
        print(f"Erro durante a execução da consulta count_cars_by_brand: {e}")
        return []
