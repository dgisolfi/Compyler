import sys
from termcolor import colored

class Error:
    def __init__(self, module, message, line=None, pos=None):
        self.module = module
        self.message = message
        self.line = line
        self.pos = pos
        self.alert()

    def alert(self):
        if self.module == 'main':
            print(f"{colored(f'Error in {self.module}', 'red')}: {self.message}")
        # Terminate the program
        sys.exit()
