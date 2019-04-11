
#!/usr/bin/python3
# 2019-3-24

from ast import AST
from tree import Tree
from error import Error
from warning import Warning
from termcolor import colored
from symtable import SymbolTable

class SemanticAnalyser:
    def __init__(self, verbose, printmode, program, cst):
        self.__ast = Tree(printmode)
        self.cst = cst
        self.warnings = 0
        self.errors = 0
        self.program = program     
        self.verbose = verbose
        self.__symbol_table = None
        self.__cur_table = None
        print(colored(f'Analyzing Program {self.program}', 'blue'))
        self.genAST()
        self.log('Building Symbol Table')
        self.analyze(self.__ast.root)
        self.log('Checking for Unused Variables')
        self.checkUnusedVariables(self.__symbol_table)
    
    @property
    def ast(self):
        return self.__ast
    
    @property
    def symbol_table(self):
        return self.__symbol_table

    def genAST(self):
        self.log('Generating AST')
        abstractedTree = AST(self.cst, self.__ast)
        self.__ast = abstractedTree.ast

    def error(self, msg, line, pos):
        if self.errors is 0:
            Error('Semantic Analyzer', msg, line, pos)
            self.errors += 1

    def log(self, msg):
        if self.verbose and self.errors is 0:
            print(colored(f'ANALYSER ❯ {msg}', 'green'))

    def analyze(self, node):
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
            for child in node.children:
                self.analyze(child)
            # This will return the scope back to its
            # parent once the block has been analyzed
            if node.name == 'Block':
                self.__cur_table = self.__cur_table.parent

    def getType(self, value):
        if value.isdigit():
            return 'int'
        elif value in ['true', 'false']:
            return 'boolean'
        else:
            return 'string'

    def markAsUsed(self, symbol, table):
        symbol_entry = table.get(symbol)
        if symbol_entry is None:
            if table.parent != None:
                self.markAsUsed(symbol, table.parent)
            else:
                if table.scope is -1:
                    print('If you are seeing this, the variable couldnt be found in the table.')  
        else:
            self.log(f'Marking "{symbol}" as Used.')
            symbol_entry[3] = True
            table.update(symbol, symbol_entry)

    def markAsInitialized(self, symbol, table):
        symbol_entry = table.get(symbol)
        if symbol_entry is None:
            if table.parent != None:
                self.markAsInitialized(symbol, table.parent)
            else:
                if table.scope is -1:
                    print('If you are seeing this, the variable couldnt be found in the table.')  
        else:
            self.log(f'Marking "{symbol}" as Initialized.')
            symbol_entry[2] = True
            table.update(symbol, symbol_entry)
           

    def scopeCheck(self, symbol, table):
        self.log(f'Scope Checking Identifier: "{symbol.name}" in Scope: {table.scope}')
        # lookup symbol in cur scope
        symbol_entry = table.get(symbol.name)
        if symbol_entry is None:
            if table.parent != None:
                self.log(f'Identifier: "{symbol.name}" not found in current scope, looking to parent scope.')
                self.scopeCheck(symbol, table.parent)
               
            else:
                # Variable was Undeclared 
                self.error(f"Undeclared variable '{symbol.name}'", 
                symbol.line, symbol.position)


    def typeCheck(self, symbol, value, table):
        self.log(f'Type Checking Identifier: "{symbol.name}" with Value: {value.name}')

        # lookup symbol in cur scope
        symbol_entry = table.get(symbol.name)
        if symbol_entry is None:
            if table.parent != None:
                self.log(f'Identifier: {symbol.name} not found in current scope, looking to parent scope.')
                self.typeCheck(symbol, value, table.parent)
            else:
                if table.scope is -1:
                    print('If you are seeing this, the variable couldnt be found in the table.')        
        else:
            var_type = symbol_entry[0]
            if var_type != self.getType(value.name):
                self.error(f'Type mismatch for Identifier: \'{symbol.name}\' with Value: {value.name}', 
                symbol.line, symbol.position)            
        
    def checkBlock(self, node):
        self.log(f'Checking [{node.name}]')
        if self.__symbol_table is None:
            self.__symbol_table = SymbolTable(SymbolTable(None, -1), 0)
            self.__cur_table = self.__symbol_table
        else:
            self.log(f'New Scope Detected')
            # New Block means new scope
            self.__cur_table = SymbolTable(
                self.__cur_table,
                self.__cur_table.scope+1
            )
            self.__cur_table.parent.addChild(self.__cur_table)

    def checkAssignmentStatement(self, node):
        self.log(f'Checking [{node.name}]')
        # [print(i.name) for i in node.children]
        if node.children[1].name is 'Add':
            self.checkAddition(node.children[1])
        else:
            # lookup symbol in cur scope
            self.scopeCheck(node.children[0], self.__cur_table)
            # check the type of 
            self.typeCheck(node.children[0], node.children[1], self.__cur_table)
        
        self.markAsInitialized(node.children[0].name, self.__cur_table)

    
    def checkVarDecleration(self, node):
        self.log(f'Checking [{node.name}]')
        self.log(f'Adding {node.children[0].name} {node.children[1].name} to Symbol Table')
        # Add the Decleration to the Symbol table
        self.__cur_table.add(
            node.children[1].name,
            node.children[0].name,
            node.children[1].line
        )

    def checkPrintStatement(self, node):
        self.log(f'Checking [{node.name}]')

        # Check if its a ID
        if (not node.children[0].name == 'CharList' 
        and node.children[0].name not in ['true', 'false']):
            self.scopeCheck(node.children[0], self.__cur_table)
            self.markAsUsed(node.children[0].name, self.__cur_table)
    

    def checkWhileStatement(self, node):
        self.log(f'Checking [{node.name}]')
        self.markAsUsed(node.children[0].children[0].name, self.__cur_table)

    def checkIfStatement(self, node):
        self.log(f'Checking [{node.name}]')
        pass 

    def checkAddition(self, node):
        self.log(f'Checking [{node.name}]')
        
        term_1 = node.children[0]
        term_2 = node.children[1]

        if not term_2.name.isdigit():
            # lookup symbol in cur scope
            self.scopeCheck(term_2, self.__cur_table)
            # check the type of the var compared to the term
            self.typeCheck(term_2, term_1, self.__cur_table)
        
        # else its just two numbers so its fine
    

    def checkUnusedVariables(self, symbol_table):
        # look through the symbol table and find identifiers that have 
        # false in there isUsed feild
        for var in symbol_table.table:
            if not symbol_table.table[var][3]:
                Warning('Semantic Analyzer', 
                f'Variable "{var}" was declared on line:{symbol_table.table[var][1]} but never used'
                )

        if len(symbol_table.children) is not 0:
            for child in symbol_table.children:
                self.checkUnusedVariables(child)