from lxml import etree

def get_sales_country(xml):

    country = "Indonesia"

    try:
        tree = etree.fromstring(xml)
        sales = tree.xpath(f"/Data/Sales/Sales[@country='{country}']")

        results = []
        for sale in sales:
            person_info = sale.get('person_id')
            car_info = sale.get('car_id')
            result = f"Venda ID: {sale.get('id')}, Dados Cliente: {person_info}, Dados do veiculo: {car_info}"
            results.append(result)

        return results
    except etree.XMLSyntaxError as syntax_error:
        print(f"Erro de sintaxe XML na consulta get_sales_country: {syntax_error}")
        return []
    except Exception as e:
        print(f"Erro durante a execução da consulta get_sales_country: {e}")
        return []

