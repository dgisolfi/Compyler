#!/usr/bin/python3
# 2019-1-27
# Daniel Nicolas Gisolfi

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
        if self.module is not  'main':
           print(f"{colored(f'Error in {self.module}', 'red')}: {self.message} at line:{self.line} col:{self.pos}")
        else:
            print(f"{colored(f'Error in {self.module}', 'red')}: {self.message}")
            sys.exit(1)