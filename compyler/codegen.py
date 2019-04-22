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

    def __repr__(self):
        return self.__str__()

    @property
    def code(self):
        return self.__code

    def append(self, code):
        if type(code) is list or type(code) is tuple:
            [self.__code.append(hex) for hex in code]
        else:
            self.__code.append(code)

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
        self.append('00')
        self.backpatch()
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
        return '{0:x}'.format(int(decimal)).upper()

    def getTempAddr(self, id):
        # If the addr exists at the current scope level,
        # than everthing is good, just return it.
        temp_addr = self.__static[f'{id}{self.__scope}'][0]
        # However if None is returned meaning it cannot be 
        # found at that scope level...we need to go deeper.
        # if temp_addr is None:
        #     wh
        return temp_addr[:2], temp_addr[2:]

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


    def backpatch(self):
        # backpath all static values
        for key in self.__static.keys():
            temp_addr = self.__static[key][0]
            offset = self.__static[key][3]

            # get the final address of the value
            addr = self.hex((len(self.__code)-1) + offset)
            for index, hex in enumerate(self.__code):
                # match the TX val in the code and static table
                if hex == temp_addr[:2]:
                    self.__code[index] = addr
                    self.__code[index+1] = '00'


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
        self.append(['A9', '00'])

        # Store the accumulator in temp location 
        # Add new temp value to static table
        self.append('8D')
        var = node.children[1]
        temp = self.addStatic(var, self.__scope)
        self.append(temp)

    def createAssignmentStatement(self, node):
        # Get the type of the assignment statement
        id = node.children[0].name
        value = node.children[1].name
        type = self.getType(value)

        if type is 'int':
            # load the value into the accumulator
            value = '0' + node.children[1].name
            self.append(['A9', value])
        elif type is 'boolean':
            # translate the bool val to a int
            if node.children[1].name is 'true':
                pass
            elif node.children[1].name is 'false':
                pass
        elif type is 'string':
            pass
        elif type is 'variable':
            # Load the accumulator with the contents of the variable
            self.append('AD')
            temp = self.getTempAddr(value)
            self.append(temp)


        self.append('8D')
        temp = self.getTempAddr(id)
        self.append(temp)
        

    def createPrintStatement(self, node):
        # Get the type of the value
        value = node.children[0].name
        val_type = self.getType(value)
        
        print(val_type)
        if val_type is 'int':
            # load y reg with value
            self.append(['A0', ('0'+value)])
        elif val_type is 'string':
            pass
        elif val_type is 'variable':
            # load the y reg with the contents of the variable
            self.append('AC')
            temp = self.getTempAddr(value)
            self.append(temp)

            # load the X reg with 1 and Sys call
            self.append(['A2', '01', 'FF'])



        
        
        
