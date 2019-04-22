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
        self.__static = {}
        self.__scope = -1
        self.__cur_symtable = symtable
  
        self.__temp_addr_count = 0

        self.verbose = verbose
        self.errors = 0
        self.warnings = 0

        self.generate()

    def __str__(self):
        rows = self.split(self.__code, 8)
        out = ''
        for row in rows:
            for hex in row:
                out += f'{hex} '
            print(out)
            out = ''
        return ''

    @property
    def code(self):
        return self.__code

    # used for printing
    def split(self, arr, size):
        arrs = []
        while len(arr) > size:
            splice = arr[:size]
            arrs.append(splice)
            arr = arr[size:]
        arrs.append(arr)
        return arrs

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
        # print(self.__static)
        print(self)

    def createStatement(self, node):
        self.log(f'Found {node.name}')

        if node.name == 'Block':
            self.createBlock(node)
        elif node.name == 'VarDecleration':
           self.createVarDecleration(node)
        elif node.name == 'AssignmentStatement':
            self.createAssignmentStatement(node)
        elif node.name == 'PrintStatement':
            self.createPrintStatement(node)
        elif node.name == 'WhileStatement':
            pass
        elif node.name == 'IfStatement':
            pass
        
    # Add static values and handle all the temp value stuff
    def addStatic(self, var, scope):
        key =  var.name + str(scope)
        temp_addr = f'T{self.__temp_addr_count}XX'
        offset = len(self.__static)

        self.__static[key] = [temp_addr, var.name, scope, offset]
        self.__temp_addr_count += 1
        return temp_addr[:2], temp_addr[2:]

    def hex(self, decimal):
        return '{0:x}'.format(int(decimal))

    def getTempAddr(self, id):
        # If the addr exists at the current scope level,
        # than everthing is good, just return it.
        temp_addr = self.__static[f'{id}{self.__scope}']
        # However if None is returned meaning it cannot be 
        # found at that scope level...we need to go deeper.
        # if temp_addr is None:
        #     wh
        return temp_addr

    def getType(self, value):
        if value.isdigit():
            return 'int'
        elif value in ['true', 'false']:
            return 'boolean'
        elif value == 'CharList':
            return 'string'
        # Its a variable
        else:
            return 'variable'

    # code gen 

    def createBlock(self, node):
        self.__scope += 1
        self.log(f'Creating New Block with Scope: {self.__scope}')
        for child in self.__cur_symtable.children:
            if child.scope is self.__scope:
                self.__cur_symtable = child

        for node in node.children:
            self.createStatement(node)

        
    
    def createVarDecleration(self, node):
        # TODO: rearange scoping, gotta get the right one
        # Load the accumulator with 0
        [self.__code.append(hex) for hex in ['A9', '00']]

        # Store the accumulator in temp location 
        # Add new temp value to static table
        self.__code.append('8D')
        var = node.children[1]
        temp = self.addStatic(var, self.__scope)
        [self.__code.append(hex) for hex in temp]

    def createAssignmentStatement(self, node):
        # Get the type of the assignment statement
        id = node.children[0].name
        type = self.__cur_symtable.get(id)[0]

        if type is 'int':
            # load the value into the accumulator
            value = '0' + node.children[1].name
            [self.__code.append(hex) for hex in ['A9', value]]
        elif type is 'boolean':
            # translate the bool val to a int
            if node.children[1].name is 'true':
                pass
            elif node.children[1].name is 'false':
                pass
        # string
        else:
            pass

    def createPrintStatement(self, node):
        # Get the type of the value
        value = node.children[0].name
        val_type = self.getType(value)
        
        print(val_type)
        if val_type is 'int':
            # load y reg with value
            constant = '0' + value
            [self.__code.append(hex) for hex in ['A0', constant]]
        elif val_type is 'string':
            pass
        elif val_type is 'variable':
            val_type = self.__cur_symtable.get(id)[0]



        
        
        
