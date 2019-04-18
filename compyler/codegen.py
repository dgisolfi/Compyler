#!/usr/bin/python3
# 2019-4-18
# Daniel Nicolas Gisolfi

from error import Error
from warning import Warning
from termcolor import colored

class CodeGenerator:
    def __init__(self, verbose, ast, symtable):
        self.__ast = ast
        self.__symtable = symtable
        self.__code = []
        self.__heap = []
        self.__scope = 0

        self.verbose = verbose
        self.errors = 0
        self.warnings = 0

        self.generate()

    @property
    def code(self):
        return self.__code


    def error(self, msg, line, pos):
        if self.errors is 0:
            Error('Code Generation', msg, line, pos)
            self.errors += 1

    def log(self, msg):
        if self.verbose and self.errors is 0:
            print(colored(f'GENERATOR ❯ {msg}', 'blue'))

    def generate(self):
        # The Program must always start with a block
        self.createBlock(self.__ast.root)

    def createStatement(self, node):
        self.log(f'Found {node.name}')

        if node.name == 'Block':
            self.createBlock(node)
        elif node.name == 'AssignmentStatement':
           pass
        elif node.name == 'VarDecleration':
           pass
        elif node.name == 'PrintStatement':
           pass
        elif node.name == 'WhileStatement':
            pass
        elif node.name == 'IfStatement':
            pass
        

    def createBlock(self, node):
        self.log(f'Creating New Block with Scope: {self.__scope}')
        self.__scope += 1
        for node in node.children:
            self.createStatement(node)

        self.__scope -= 1
        
