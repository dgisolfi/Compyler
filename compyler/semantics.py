#!/usr/bin/python3
# 2019-3-24
# Daniel Nicolas Gisolfi

import re
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
        self.__scope = -1
        self.__cur_scope_level = -1
        print(colored(f'Analyzing Program {self.program}', 'green', attrs=['bold']))
        self.genAST()
        self.log('Building Symbol Table')
        self.analyze(self.__ast.root)
        if self.errors is 0:
            self.log('Checking for Unused Variables')
            self.checkUnusedVariables(self.__symbol_table)
            self.log('Checking for Uninitialized Variables')
            self.checkUninitializedVariables(self.__symbol_table)
            self.log('Done.')
            print(colored(f'Analysis Completed for Program {self.program}', 'green', attrs=['bold']))
    
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
        
      
        for child in node.children:
            self.analyze(child)
        # This will return the scope back to its
        # parent once the block has been analyzed
        if node.name == 'Block':
            self.__cur_table = self.__cur_table.parent
            self.__cur_scope_level -= 1


    def getVariable(self, symbol, table):
        # lookup symbol in cur scope
        symbol_entry = table.get(symbol)
       
        if symbol_entry is None:
            # this doesnt mean it doesnt exist, we need to check high scopes
            if table.parent != None:
                self.log(f'Identifier: {symbol} not found in current scope, looking to parent scope.')
                var_type, scope = self.getVariable(symbol, table.parent)
                return var_type, table.scope
            else:
                # if none of the parents have it then it dont exist
                if table.scope is -1:
                    return None, None
        else:
            return symbol_entry[0], None

    def getType(self, value):
        if value.isdigit() and re.match(r'[0-9]', value):
            return 'int'
        elif value in ['true', 'false', 'IsEqual', 'NotEqual']:
            return 'boolean'
        elif value == 'CharList':
            return 'string'
        elif re.match(r'[a-z]', value):
            return 'variable'
           
    def markAsUsed(self, symbol, table):
        symbol_entry = table.get(symbol)
        if symbol_entry is None:
            if table.parent != None:
                self.markAsUsed(symbol, table.parent)
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
            self.log(f'Marking "{symbol}" as Initialized.')
            symbol_entry[2] = True
            table.update(symbol, symbol_entry)  

    def scopeCheck(self, symbol, table):
        if table.scope is not -1:
            self.log(f'Scope Checking Identifier: [{symbol.name}] in Scope: {table.scope}')
        # lookup symbol in cur scope
        symbol_entry = table.get(symbol.name)
        if symbol_entry is None:
            if table.parent != None:
                self.log(f'Identifier: [{symbol.name}] not found in current scope, looking to parent scope.')
                self.scopeCheck(symbol, table.parent)
            else:
                # Variable was Undeclared 
                self.error(f'Undeclared variable [{symbol.name}]', 
                symbol.line, symbol.position)

    def typeCheck(self, first_value, second_value, table):
        self.log(f'Type Checking [{first_value.name}] with [{second_value.name}]')

        first_value_type = self.getType(first_value.name)
        if first_value_type == 'variable':
            first_value_type, scope = self.getVariable(first_value.name, self.__cur_table)
        elif first_value_type == 'string':
            first_value = first_value.children[0]
        
        second_value_type = self.getType(second_value.name)
        if second_value_type == 'variable':
            second_value_type, scope = self.getVariable(second_value.name, self.__cur_table)
        elif second_value_type == 'string':
            second_value = second_value.children[0]

        if first_value_type != second_value_type:
            self.error(f'Type mismatch for Identifier: [{first_value.name}] with Value: {second_value.name}', 
            first_value.line, first_value.position)            
        
    def checkBlock(self, node):
        self.log(f'Checking {node.name}')
        self.__scope += 1
        self.__cur_scope_level += 1
        
        if self.__symbol_table is None:
            self.__symbol_table = SymbolTable(SymbolTable(None, -1, -1), 0, self.__cur_scope_level)
            self.__cur_table = self.__symbol_table
        else:
            self.log(f'New Scope Detected')
            # New Block means new scope
            self.__cur_table = SymbolTable(
                self.__cur_table,
                self.__scope,
                self.__cur_scope_level
            )
            self.__cur_table.parent.addChild(self.__cur_table)

    def checkAssignmentStatement(self, node):
        self.log(f'Checking {node.name}')
        if node.children[1].name is 'Add':
            self.checkAddition(node.children[1])
        elif node.children[0].name in ['IsEqual','NotEqual']:
            self.checkBooleanExpr(node.children[0])
        elif node.children[1].name in ['IsEqual','NotEqual']:
            self.checkBooleanExpr(node.children[1])
        else:
            # lookup symbol in cur scope
            self.scopeCheck(node.children[0], self.__cur_table)
            term_2 = node.children[1]
            if node.children[1].name is 'Add':
                term_2 = node.children[1].children[0]
            # check the type of 
            self.typeCheck(node.children[0], term_2, self.__cur_table)
        
        self.markAsInitialized(node.children[0].name, self.__cur_table)
    
    def checkVarDecleration(self, node):
        self.log(f'Checking {node.name}')
        self.log(f'Adding [{node.children[0].name} {node.children[1].name}] to Symbol Table')
        
        var_type, scope = self.getVariable(node.children[1].name, self.__cur_table)
        if var_type is not None and scope is not self.__cur_table.scope:
            self.error(f'Attempt to redeclare variable [{node.children[1].name}]', 
            node.children[1].line, node.children[1].position)
          
        # Add the Decleration to the Symbol table
        self.__cur_table.add(
            node.children[1].name, # symbol
            node.children[0].name, # type
            node.children[1].line  # line number
        )

    def checkPrintStatement(self, node):
        self.log(f'Checking {node.name}')

        # Check for BoolExpr
        if node.children[0].name in ['IsEqual','NotEqual']:
            self.checkBooleanExpr(node.children[0])
        # check for IntExpr
        elif node.children[0].name is 'Add':
            self.checkAddition(node.children[0])
        # Check if its a ID
        elif self.getType(node.children[0].name) is 'variable':
            self.scopeCheck(node.children[0], self.__cur_table)
            self.markAsUsed(node.children[0].name, self.__cur_table)
    

    def checkWhileStatement(self, node):
        self.log(f'Checking {node.name}')
        self.checkBooleanExpr(node.children[0])

    def checkIfStatement(self, node):
        self.log(f'Checking {node.name}')
        self.checkBooleanExpr(node.children[0]) 

    def checkAddition(self, node):
        self.log(f'Checking {node.name}')
        term_1 = node.children[0]
        term_2 = node.children[1]

        if term_1.name is '\"':
            self.error(f'Attempt to add Non Integer value: [{term_1.name}]', 
            term_1.line, term_1.position)            
        elif term_2.name is '\"':
            self.error(f'Attempt to add Non Integer value: [{term_2.name}]', 
            term_2.line, term_2.position)     

        if term_2.name is 'Add':
            self.checkAddition(term_2)
            self.typeCheck(term_2.children[0], term_1, self.__cur_table)
        # if not term_2.name.isdigit():
        elif self.getType(term_2.name) is 'variable':
            self.scopeCheck(term_2, self.__cur_table)
            self.markAsUsed(term_2.name, self.__cur_table)
          
            if term_2.name is 'Add':
                self.typeCheck(term_2.children[0], term_1, self.__cur_table)
            else:
                # check the type of the var compared to the term
                self.typeCheck(term_2, term_1, self.__cur_table)

    def checkBooleanExpr(self, node):
        self.log(f'Checking Boolean Expression')

        if not node.name in ['true', 'false']:

            if node.children[0].name in ['IsEqual', 'NotEqual']:
                # there is a nested boolexpr
                self.checkBooleanExpr(node.children[0])
            else:
                self.checkExpr(node.children[0])

            if node.children[1].name in ['IsEqual', 'NotEqual']: 
                # there is a nested boolexpr
                self.checkBooleanExpr(node.children[1])
            else:
                self.checkExpr(node.children[1])
            self.typeCheck(node.children[0], node.children[1], self.__cur_table)

            
           
    def checkExpr(self, node):
        expr_type = self.getType(node.name)

        if node.name == 'Add':
            self.checkAddition(node)

        if expr_type == 'variable':
            self.scopeCheck(node, self.__cur_table)
            self.markAsUsed(node.name, self.__cur_table)


    def checkUnusedVariables(self, symbol_table):
        # look through the symbol table and find identifiers that have 
        # false in there isUsed feild
        for var in symbol_table.table:
            if not symbol_table.table[var][3]:
                Warning('Semantic Analyzer', 
                f'Variable [{var}] was declared on line:{symbol_table.table[var][1]} but never used'
                )
                self.warnings += 1

        if len(symbol_table.children) is not 0:
            for child in symbol_table.children:
                self.checkUnusedVariables(child)

    def checkUninitializedVariables(self, symbol_table):
        # look through the symbol table and find identifiers that have 
        # false in there isInitialized feild
        for var in symbol_table.table:
            if not symbol_table.table[var][2]:
                Warning('Semantic Analyzer', 
                f'Variable [{var}] was declared on line:{symbol_table.table[var][1]} but never Initialized'
                )
                self.warnings += 1

        if len(symbol_table.children) is not 0:
            for child in symbol_table.children:
                self.checkUninitializedVariables(child)