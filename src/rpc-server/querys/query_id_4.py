from lxml import etree

def list_ordered_people(xml):
    try:
        tree = etree.fromstring(xml)
        persons = tree.xpath("/Data/Persons/Person")

        # Ordenar pessoas por primeiro nome
        ordered_persons = sorted(persons, key=lambda person: person.get("first_name"))

        results = []
        for person in ordered_persons:
            result = f"Person ID: {person.get('id')}, Nome: {person.get('first_name')} {person.get('last_name')}"
            results.append(result)

        return results
    except etree.XMLSyntaxError as syntax_error:
        print(f"Erro de sintaxe XML na consulta list_ordered_people: {syntax_error}")
        return []
    except Exception as e:
        print(f"Erro durante a execução da consulta list_ordered_people: {e}")
        return []
