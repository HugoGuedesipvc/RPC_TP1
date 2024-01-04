# Importações necessárias
import signal
import socket
import sys
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import tempfile
from xml_generation.xml_process import generate_and_validate_xml
from base_dados.bd import *
from querys.rotinas import *

# Classe para manipulação de requisições XML-RPC
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Criar o servidor XML-RPC
with SimpleXMLRPCServer(('0.0.0.0', 9000), requestHandler=RequestHandler, allow_none=True) as server:
    # Registrar funções de introspecção
    server.register_introspection_functions()


    # Função para lidar com sinais de encerramento
    def signal_handler(signum, frame):
        print("Recebido sinal para encerrar.")
        server.server_close()
        print("Encerrando, graciosamente.")
        sys.exit(0)


    # Associar a função de manipulação de sinal ao sinal correspondente
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)


    # Função para salvar um arquivo CSV no servidor
    def save_csv_file(file_name, csv_data):
        try:
            # Decodificar dados CSV
            csv_content = csv_data.data.decode('utf-8')

            # Escrever CSV em um arquivo temporário
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_csv:
                temp_csv.write(csv_content)
                temp_csv_path = temp_csv.name

                # Gerar e validar XML, em seguida, inserir na base de dados
                data = generate_and_validate_xml(file_name, temp_csv_path)
                insert_xml_data(file_name, data)
        except Exception as e:
            # Em caso de erro, definir o ID como 0 para sinalizar o problema
            print(f"Erro durante o processamento no servidor: {e}")


    # Função para listar arquivos XML na base de dados
    def list_xml():
        try:
            result = list_xml_files()
            return result
        except Exception as e:
            print(f"Erro na base de dados: {e}")
            return None
    def list_csv():
        try:
            result = get_all_active_csv()
            return result
        except Exception as e:
            print(f"Erro na base de dados: {e}")
            return None

    # Função para excluir um documento XML na base de dados
    def eliminar_xml(id):
        try:
            soft_delete_document(id)
        except Exception as e:
            print(f"Erro na base de dados: {e}")


    # Função para realizar rotinas de consulta com base no ID fornecido
    def routinas_query(id):
        try:
            active_xml_list = get_all_active_xml()
            execute_queries(active_xml_list, id)
        except Exception as e:
            print(f"Erro na criação de rotinas: {e}")



    # Registrar funções no servidor
    server.register_function(save_csv_file)
    server.register_function(list_xml)
    server.register_function(eliminar_xml)
    server.register_function(routinas_query)
    server.register_function(list_csv)
    # Iniciar o servidor XML-RPC e aguardar por solicitações
    print("Starting the RPC Server...")
    print("JOMS")
    server.serve_forever()