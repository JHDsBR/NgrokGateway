import subprocess
import os
import platform

from utils import execute_in_thread

sys_windows = platform.system() == "Windows"

class Ngrok():

    @execute_in_thread
    def start(self, port):
        diretorio_app = os.path.dirname(os.path.abspath(__file__))
        caminho_para_exe = os.path.join(diretorio_app, 'ngrok')
        print(subprocess.Popen(f'{caminho_para_exe} tunnel --label edge={os.environ.get("EDGE_TOKEN")} http://localhost:{port}', shell=True))
