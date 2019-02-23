#!/usr/bin/python3
# 2019-1-27

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
        if self.module is 'lexer':
           print(f"{colored(f'Error in {self.module}', 'red')}: {self.message} at line:{self.line} col:{self.pos}")
        else:
            if self.module is 'main':
                print(f"{colored(f'Error in {self.module}', 'red')}: {self.message}")
            else:
                print(f"{colored(f'Error in {self.module}', 'red')}: {self.message} at line:{self.line} col:{self.pos}")
            # Terminate the program
            sys.exit()