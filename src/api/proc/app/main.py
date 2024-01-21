
import sys
from flask import Flask, jsonify, request
import xmlrpc.client

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 8091

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def home():
    return 'Test ligação'

@app.route('/api/list-xml/', methods=['GET', 'POST'])
def list_xml_endpoint():
    if request.method == 'GET' or request.method == 'POST':
        params = {
        }

        rpc_server_url = "http://is-rpc-server:9000/RPC2"
        proxy = xmlrpc.client.ServerProxy(rpc_server_url)

        try:
            result = proxy.list_xml(**params)
            return jsonify({"result": result})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Method Not Allowed"}), 405


@app.route('/api/routinas-query/', methods=['GET', 'POST'])
def routinas_query_endpoint():
    if request.method == 'GET' or request.method == 'POST':
        params = {
            "atributo": "valor",
        }

        rpc_server_url = "http://is-rpc-server:9000/RPC2"
        proxy = xmlrpc.client.ServerProxy(rpc_server_url)

        try:
            result = proxy.routinas_query(**params)
            return jsonify({"result": result})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Method Not Allowed"}), 405

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=True)
