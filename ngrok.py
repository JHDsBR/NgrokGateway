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
        if sys_windows:
            print(subprocess.Popen(f'{caminho_para_exe} tunnel --label edge={os.environ.get("EDGE_TOKEN")} http://localhost:{port}', shell=True))
        else:
            # Comando que você deseja executar com sudo
            # comando = "sudo ls /root"  # Substitua pelo seu próprio comando

            # Concatena a senha ao comando (via echo e pipe)
            # comando_com_sudo = f'echo "{senha}" | {comando}'

            # Executa o comando com sudo
            # subprocess.run(comando_com_sudo, shell=True)
            senha = os.environ.get("VM_SENHA")
            processo = subprocess.run(f'sudo ngrok tunnel --label edge={os.environ.get("EDGE_TOKEN")} http://localhost:{port}', shell=True)
            # senha = b'SUA_SENHA_AQUI\n'  # Substitua pela sua senha
            processo.stdin.write(str(senha+'\n').encode("utf-8"))
            processo.stdin.flush()
            # subprocess.Popen(f'{senha}', shell=True)

