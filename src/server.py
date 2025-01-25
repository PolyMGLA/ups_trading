import os
from threading import Thread
from subprocess import DEVNULL, STDOUT, check_call
from colorama import init
init()
from colorama import Fore, Back, Style

class Server(Thread):
    def run(self):
        print(Fore.YELLOW + "running dashboard on http://localhost:5173/", Style.RESET_ALL)
        os.system("cd src/frontend && pnpm dev > /dev/null 2>&1")
        # check_call(["sh", "eval '$(cd src/frontend && pnpm dev)'"], stdout=DEVNULL, stderr=STDOUT)

if __name__ == "__main__":
    serv = Server()
    serv.start()