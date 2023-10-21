
import json
from os import environ
from dotenv import load_dotenv
import requests
from ngrok import Ngrok
from flask import Flask, request
from flask_cors import CORS
from apis import API_MANAGER
import logging

load_dotenv(".env")

# requests.packages.urllib3.disable_warnings()
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

if (environ.get("IS_DEVELOPMENT") or "false").lower() == "true":
    print("VERSÂO DE TESTE")

app = Flask(__name__)

CORS(app)


apis = API_MANAGER()

# Tratamento para rota inexistente
@app.errorhandler(404)
def acessar_api(e):

    url_splited = request.url.split("/")
    api = url_splited[3]
    rota = '/'.join(url_splited[4:])

    if not apis.api_existe(api):
        return {"msg":"rota não existe", "rota":f'/{api}/{rota}'}
    
    port = apis.get_api(api).port

    req = requests.get(f'http://127.0.0.1:{port}/{api}/{rota}')

    if req.status_code == 200:
        return req.json()

    return {"msg":"houve um erro ao acessar a rota", "rota":rota}


@app.errorhandler(Exception)
def handle_exception(e):
    # Aqui você pode adicionar o código para manipular a exceção
    return {"success":False, "msg":"houve algum erro interno", "exception":str(e)}


@app.post("/add_api/<nome>")
def add_api(nome):
    
    if apis.api_existe(nome):
        api = apis.add_nova_api(nome)
        return {"success":True, "msg":f"Api ({nome}) já existia", "port":api.port}
        
    api = apis.add_nova_api(nome)


    return {"success":True, "msg":f"", "port":api.port}


@app.get("/get_port/<nome>")
def get_api_port(nome):
    
    if not apis.api_existe(nome):
        return {"success":False, "msg":f"Api ({nome}) não existe"}
    
    return {"success":True, "msg":f"", "port":apis.get_api(nome).port}
    

@app.route("/")
def Home():
    return "ONLINE"


port = environ.get("NGROK_PORT") or 5110

ngk = Ngrok()
ngk.start(port)

# rotas = [rule.rule for rule in app.url_map.iter_rules() if not rule.rule.startswith("/static")]

# print(rotas)
if __name__ == "__main__":
    app.run(port=port)