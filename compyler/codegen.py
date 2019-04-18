#!/usr/bin/python3
# 2019-4-18
# Daniel Nicolas Gisolfi

from error import Error
from warning import Warning
from termcolor import colored

class CodeGenerator:
    def __init__(self, ast, symtable):
        self.__ast = ast
        self.__symtable = symtable
        self.__code = []
        self.__heap = []

    @property
    def code(self):
        return self.__code


    def error(self, msg, line, pos):
        if self.errors is 0:
            Error('Code Generation', msg, line, pos)
            self.errors += 1

    def log(self, msg):
        if self.verbose and self.errors is 0:
            print(colored(f'GENERATOR ❯ {msg}', 'white'))


    def generate(self):
        pass

    def createStatement(self):
        pass