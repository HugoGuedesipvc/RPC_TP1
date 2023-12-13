import psycopg2
from psycopg2 import sql
from datetime import datetime
from base_dados.bd_params import db_params

def insert_xml_data(temp_xml_filename, xml_str):
    try:
        with psycopg2.connect(**db_params) as connection, connection.cursor() as cursor:
            cursor.execute("SELECT id FROM public.imported_documents WHERE file_name = %s", (temp_xml_filename,))
            existing_record = cursor.fetchone()

            if existing_record:
                print(f"Registro com o file_name '{temp_xml_filename}' já existe com ID: {existing_record[0]}")
                cursor.execute(
                    sql.SQL("UPDATE public.imported_documents SET xml = %s WHERE id = %s"),
                    (xml_str, existing_record[0]),
                )
                connection.commit()
                return existing_record[0]
            else:
                cursor.execute(
                    sql.SQL("INSERT INTO public.imported_documents (file_name, xml) VALUES (%s, %s) RETURNING id"),
                    (temp_xml_filename, xml_str),
                )
                connection.commit()
    except (Exception, psycopg2.Error) as e:
        print(f"Erro ao inserir o XML na tabela 'imported_documents': {e}")

def list_xml_files():
    try:
        with psycopg2.connect(**db_params) as connection, connection.cursor() as cursor:
            cursor.execute("SELECT id, file_name, deleted_at, created_on, updated_on FROM public.imported_documents")
            records = cursor.fetchall()
            result_list = []

            if records:
                for record in records:
                    file_info = f"ID: {record[0]}, File Name: {record[1]}, Deleted At: {record[2]}, Created On: {record[3]}, Updated On: {record[4]}"
                    if "<deleted>" not in file_info and "</deleted>" not in file_info:
                        result_list.append(file_info)
            else:
                result_list.append("Nenhum arquivo XML encontrado sem a tag 'deleted'.")

            return result_list
    except (Exception, psycopg2.Error) as e:
        print(f"Erro ao listar arquivos XML: {e}")
        return ["Erro ao listar arquivos XML."]

def soft_delete_document(document_id):
    try:
        with psycopg2.connect(**db_params) as connection, connection.cursor() as cursor:
            cursor.execute(
                sql.SQL("UPDATE public.imported_documents SET deleted_at = %s WHERE id = %s"),
                (datetime.now(), document_id),
            )
            connection.commit()
            print(f"Documento com o ID {document_id} foi marcado para ser eliminado {datetime.now()}.")
    except Exception as e:
        print(f"Erro ao marcar o arquivo XML para ser eliminado: {e}")

def get_all_active_xml():
    try:
        with psycopg2.connect(**db_params) as connection, connection.cursor() as cursor:
            cursor.execute("SELECT xml FROM public.imported_documents WHERE deleted_at IS NULL")
            xml_data_list = cursor.fetchall()
            return [xml_data[0] for xml_data in xml_data_list] if xml_data_list else []
    except (Exception, psycopg2.Error) as e:
        print(f"Erro ao obter os XML ativos: {e}")
        return []
