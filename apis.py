import socket

class API():

    def __init__(self, nome, port) -> None:
        self.nome = nome
        self.port = port




class API_MANAGER():

    def __init__(self) -> None:
        self.apis:dict[str,API] = {}
        self.START_PORT = 5200

    def add_nova_api(self, nome) -> API:
        """adiciona uma nova api"""

        port = self.START_PORT+len(self.apis.keys())
        
        print(port)
        while not verifica_porta_livre(port):
            print(port)
            port+=1

        api = API(nome, port)
        self.apis[nome] = api

        return api

    def api_existe(self, nome):

        return nome in self.apis.keys()
        
        
    def get_api(self, nome) -> API:

        if not self.api_existe(nome):
            raise Exception("Não existe a API "+nome)
        
        return self.apis[nome]



def verifica_porta_livre(porta):
    # Cria um objeto socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)

    try:
        s.connect(('localhost', porta))
        s.close()
        return False
    except (ConnectionRefusedError, TimeoutError, socket.timeout):
        return True      




