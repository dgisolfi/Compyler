
#!/usr/bin/python3
# 2019-3-24

from ast import AST
from tree import Tree
from error import Error
from termcolor import colored
from symbols import SymbolTable

class SemanticAnalyser:
    def __init__(self, verbose, printmode, program, cst):
        self.ast = Tree(printmode)
        self.cst = cst
        self.warnings = 0
        self.errors = 0
        self.program = program     
        self.verbose = verbose
        self.__symbol_table = SymbolTable(0)
        self.genAST()
        self.analyze()

    def genAST(self):
        abstractedTree = AST(self.cst, self.ast)
        self.ast = abstractedTree.ast

    def log(self, msg):
        if self.verbose and self.errors is 0:
            print(colored(f'ANALYSER ❯ {msg}', 'green'))

    def analyze(self):
        print(colored(f'Analysing Program {self.program}', 'blue'))

        self.checkBlock(self.ast.root)



    def checkBlock(self, node):
        # New Block means new scope
        self.__symbol_table = SymbolTable(
            self.__symbol_table.scope+1, 
            inner_block=self.__symbol_table
        )

    def checkExpr(self):
        pass

    def checkAssignmentStatement(self, node):
        pass 

    def checkVarDecleration(self):
        pass

    def checkPrintStatement(self):
        pass

    def checkWhileStatement(self):
        pass

    def checkIfStatement(self):
        pass 

   

    def checkUnusedVariables(self):
        self.log('Checking for Unused Variables')