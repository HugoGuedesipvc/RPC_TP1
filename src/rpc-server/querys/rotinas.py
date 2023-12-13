import os
from datetime import datetime
from querys.query_id_1 import get_sales_country
from querys.query_id_2 import get_cars_by_year
from querys.query_id_3 import get_cars_by_attributes
from querys.query_id_4 import list_ordered_people
from querys.query_id_5 import count_cars_by_brand

RESULTS_DIRECTORY = "/src/rpc-base_dados/data/"
RESULTS_FILE_NAME = "results"

def execute_queries(xml_list, id):
    results = []

    try:
        for xml in xml_list:
            if id == 1:
                result = get_sales_country(xml)
                if result:
                    results.append(result)
            elif id == 2:
                result = get_cars_by_year(xml)
                if result:
                    results.append(result)
            elif id == 3:
                result = get_cars_by_attributes(xml)
                if result:
                    results.append(result)
            elif id == 4:
                result = list_ordered_people(xml)
                if result:
                    results.append(result)
            elif id == 5:
                result = count_cars_by_brand(xml)
                if result:
                    results.append(result)
            else:
                print(f"Consulta com ID {id} não encontrada.")

    except Exception as e:
        print(f"Erro durante a execução da consulta {id}: {e}")

    if results:
        print("Consulta realizada")
        write_results_to_file(results)
        print("Dados guardados")

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_results_to_file(results):
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file_path = os.path.join(RESULTS_DIRECTORY, f"{RESULTS_FILE_NAME}_{date_str}.txt")

    create_directory_if_not_exists(os.path.dirname(results_file_path))

    try:
        with open(results_file_path, "w") as file:
            for result_set in results:
                for result in result_set:
                    file.write(result + "\n")
                file.write("\n")
        print(f"Dados escritos em {results_file_path}")
        return True
    except Exception as e:
        print(f"Erro ao escrever no arquivo {results_file_path}: {e}")
        return False
