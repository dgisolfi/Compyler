
#!/usr/bin/python3
# 2019-3-24

from ast import AST
from tree import Tree
from error import Error
from termcolor import colored
from symtable import SymbolTable

class SemanticAnalyser:
    def __init__(self, verbose, printmode, program, cst):
        self.ast = Tree(printmode)
        self.cst = cst
        self.warnings = 0
        self.errors = 0
        self.program = program     
        self.verbose = verbose
        self.__symbol_table = None
        self.__cur_table = None
        self.__cur_scope = None
        self.genAST()
        print(colored(f'Analyzing Program {self.program}', 'blue'))
        self.analyze(self.ast.root)
        # print(self.__symbol_table)
        # print(self.__symbol_table.children)

    def genAST(self):
        abstractedTree = AST(self.cst, self.ast)
        self.ast = abstractedTree.ast

    def error(self, msg, line, pos):
        if self.errors is 0:
            Error('Semantic Analyzer', msg, line, pos)
            self.errors += 1

    def log(self, msg):
        if self.verbose and self.errors is 0:
            print(colored(f'ANALYSER ❯ {msg}', 'green'))

    def analyze(self, node):
        # TODO: figure out when to make a scope 1 or 2 of orig
        # print(self.__cur_table)
        if node.name == 'Block':
            self.checkBlock(node)
        elif node.name == 'AssignmentStatement':
            self.checkAssignmentStatement(node)
        elif node.name == 'VarDecleration':
            self.checkVarDecleration(node)
        elif node.name == 'PrintStatement':
            self.checkPrintStatement(node)
        elif node.name == 'WhileStatement':
            self.checkWhileStatement(node)
        elif node.name == 'IfStatement':
            self.checkIfStatement(node)
        
        if self.errors == 0:
            for node in node.children:
                self.analyze(node)

    def getType(self, value):
        if value.isdigit():
            return 'int'
        elif value in ['true', 'false']:
            return 'boolean'
        else:
            return 'string'

    def scopeCheck(self, symbol, table):
        self.log(f'Scope Checking Identifier: {symbol.name}')
        print(symbol.name, table)
        # lookup symbol in cur scope
        symbol_entry = table.get(symbol.name)
        print(symbol_entry)
        if symbol_entry is None:
            if table.parent != None:
                self.log(f'Identifier: {symbol.name} not found in current scope, looking to parent scope.')
                self.scopeCheck(symbol, table.parent)
               
            else:
                # Variable was Undeclared 
                self.error(f"Undeclared variable '{symbol.name}'", 
                symbol.line, symbol.position)

    def typeCheck(self, symbol, value):
        self.log(f'Type Checking Identifier: {symbol.name} with Value: {value.name}')
        symbol_entry = self.__cur_table.get(symbol.name)
        # print(symbol_entry)
        var_type = symbol_entry[0]
        if var_type != self.getType(value.name):
            self.error(f'Type mismatch for Identifier: \'{symbol.name}\' with Value: {value.name}', 
            symbol.line, symbol.position)
        
        
    def checkBlock(self, node):
        self.log(f'Checking [{node.name}]')
        if self.__symbol_table is None:
            self.__symbol_table = SymbolTable(None, 0)
            self.__cur_table = self.__symbol_table
        else:
            self.log(f'New Scope Detected')
            # New Block means new scope
            self.__cur_table = SymbolTable(
                self.__cur_table,
                self.__cur_table.scope+1, 
                inner_blocks=self.__symbol_table
            )
            # print(self.__cur_table.scope, (self.__cur_table.parent).scope)
            # print(self.__symbol_table)
        self.__cur_scope = self.__cur_table.scope
            

    def checkExpr(self):
        pass

    def checkAssignmentStatement(self, node):
        self.log(f'Checking [{node.name}]')
        # lookup symbol in cur scope
        self.scopeCheck(node.children[0], self.__cur_table)
        # check the type of 
        self.typeCheck(node.children[0], node.children[1])



    def checkVarDecleration(self, node):
        self.log(f'Checking [{node.name}]')
        # Add the Decleration to the Symbol table
        self.__cur_table.add(node.children[1].name,
        node.children[0].name)

    def checkPrintStatement(self, node):
        self.log(f'Checking [{node.name}]')
        self.scopeCheck(node.children[0], self.__cur_table)
        # print(f'table^ {self.__cur_table}')
        # print(f'parent^ {self.__cur_table.parent}')

    def checkWhileStatement(self, node):
        self.log(f'Checking [{node.name}]')
        pass

    def checkIfStatement(self, node):
        self.log(f'Checking [{node.name}]')
        pass 

   

    def checkUnusedVariables(self):
        self.log('Checking for Unused Variables')