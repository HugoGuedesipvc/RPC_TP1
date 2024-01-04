import xmlrpc.client
import time
if __name__ == "__main__":

    time.sleep(3)

    try:
        print("Conectando ao servidor...")
        server = xmlrpc.client.ServerProxy('http://is-rpc-server:9000')

        try:
            result = server.list_xml()
            if result:
                print("Lista de arquivos XML:")
                for item in result:
                    print(item)
            else:
                print("Nenhum arquivo XML encontrado.")
        except Exception as e:
            print(f"Erro ao listar arquivos XML: {e}")

        try:
            result = server.list_csv()
            if result:
                print("Lista de arquivos csv:")
                for item in result:
                    print(item)
            else:
                print("Nenhum arquivo csv encontrado.")
        except Exception as e:
            print(f"Erro ao listar arquivos XML: {e}")

    except Exception as e:
        print(f"Erro durante a execução do cliente: {e}")
