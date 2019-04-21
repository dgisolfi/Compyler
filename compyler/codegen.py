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
        self.__static = []
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
        print(self.__static)

    def createStatement(self, node):
        self.log(f'Found {node.name}')

        if node.name == 'Block':
            self.createBlock(node)
        elif node.name == 'VarDecleration':
           self.createVarDecleration(node)
        elif node.name == 'AssignmentStatement':
            self.createAssignmentStatement(node)
        elif node.name == 'Pr intStatement':
           pass
        elif node.name == 'WhileStatement':
            pass
        elif node.name == 'IfStatement':
            pass
        
    # Add static values and handle all the temp value stuff
    def addStatic(self, var, scope):
        temp = 'T0XX'
        offset = 0
        if len(self.__static) is not 0:
            # This looks gross....but it works perfectly.
            # So were grabing the last element using the -1
            # and with that we grab the string at element 0
            # then grab the 2nd char in the string...the num
            prev_temp = self.__static[-1][0][1]
            # now cast it to an int, add 1 to it and
            # squish it all together in the new address
            temp_num = int(prev_temp) + 1
            temp = temp[:1] + str(temp_num) + temp[2:]
            # Add to the offeset as well
            offset = (self.__static[-1][3] + 1)

        self.__static.append([temp, var.name, scope, offset])
        return temp[:2], temp[2:]

    def createBlock(self, node):
        self.log(f'Creating New Block with Scope: {self.__scope}')
        self.__scope += 1
        for node in node.children:
            self.createStatement(node)

        self.__scope -= 1

    
    def createVarDecleration(self, node):
        # TODO: rearange scoping, gotta get the right one
        # Load the accumulator with 0
        [self.__code.append(hex) for hex in ['A9', '00']]

        # Store the accumulator in temp location 
        # Add new temp value to static table
        self.__code.append('8D')
        var = node.children[1]
        scope = self.__symtable.get(var.name)[1]
        temp = self.addStatic(var, scope)
        [self.__code.append(hex) for hex in temp]

    def createAssignmentStatement(self, node):
        # Get 
        var = node.children[0]
        print(self.__symtable.get(var.name))
        

        
