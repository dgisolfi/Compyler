
#!/usr/bin/python3
# 2019-3-24

from ast import AST
from tree import Tree
from error import Error
from termcolor import colored

class SemanticAnalyser:
    def __init__(self, verbose, printmode, program, cst):
        self.ast = Tree(printmode)
        self.cst = cst
        self.warnings = 0
        self.errors = 0
        self.program = program     
        self.verbose = verbose
        self.genAST()
        self.analyze()

    def genAST(self):
        abstractedTree = AST(self.cst, self.ast)
        self.ast = abstractedTree.ast
        print(self.ast)

    def analyze(self):
        pass