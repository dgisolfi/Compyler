#!/usr/bin/python3
# 2019-1-27
# Daniel Nicolas Gisolfi

import sys
from termcolor import colored

class Warning:
    def __init__(self, module, message, line=None, pos=None):
        self.module = module
        self.message = message
        self.line = line
        self.pos = pos
        self.warn()

    def warn(self):
        if self.module is 'main':
            print(f"{colored(f'Warning in {self.module}', 'yellow')}: {self.message}")
            # Terminate the program
            sys.exit()
        else:
            if self.line is None or self.pos is None:
                print(f"{colored(f'Warning in {self.module}', 'yellow')}: {self.message}")
            else:
                print(f"{colored(f'Warning in {self.module}', 'yellow')}: {self.message} at line:{self.line} col:{self.pos}")