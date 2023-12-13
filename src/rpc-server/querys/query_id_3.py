from lxml import etree

def get_cars_by_attributes(xml):

    brand = "Ford"
    model = "Club Wagon"
    color = "Teal"

    try:
        tree = etree.fromstring(xml)
        cars = tree.xpath(f"/Data/Cars/Car[contains(@brand, '{brand}') and contains(@model, '{model}') and contains(@color, '{color}')]")

        results = []
        for car in cars:
            result = (
                f"Carro ID: {car.get('id')}, "
                f"Marca: {car.get('brand')}, "
                f"Modelo: {car.get('model')}, "
                f"Cor: {car.get('color')}, "
                f"Ano: {car.get('year_of_manufacture')}"
            )
            results.append(result)

        return results
    except etree.XMLSyntaxError as syntax_error:
        print(f"Erro de sintaxe XML na consulta get_cars_by_attributes: {syntax_error}")
        return []
    except Exception as e:
        print(f"Erro durante a execução da consulta get_cars_by_attributes: {e}")
        return []