from lxml import etree

def get_cars_by_year(xml):
    year = 2010
    try:
        tree = etree.fromstring(xml)
        car_sales = tree.xpath(
            f"/Data/Sales/Sales[number(substring-after(@car_id, 'year_of_manufacture: ')) > {year}]")

        results = []
        for car_sale in car_sales:
            car_id = car_sale.get('car_id').split(",")[0].split(":")[1].strip()
            car_element = tree.xpath(f"/Data/Cars/Car[@id='{car_id}']")[0]

            result = (
                f"Carro ID: {car_id}, "
                f"Marca: {car_element.get('brand')}, "
                f"Modelo: {car_element.get('model')}, "
                f"Cor: {car_element.get('color')}, "
                f"Ano: {car_element.get('year_of_manufacture')}"
            )
            results.append(result)

        return results
    except etree.XMLSyntaxError as syntax_error:
        print(f"Erro de sintaxe XML na consulta get_cars_by_year: {syntax_error}")
        return []
    except IndexError:
        print(f"Erro: Nenhum elemento <Car> encontrado para o ID do carro.")
        return []
    except Exception as e:
        print(f"Erro durante a execução da consulta get_cars_by_year: {e}")
        return []
