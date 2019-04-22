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

    @code.setter
    def code(self, code):
        self.__code = code

    def append(self, code):
        if type(code) is tuple:
            code = list(code)
        if type(code) is list:
            self.code = self.code + code
        else:
            self.code = self.code + [code]
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
        self.generateBlock(self.__ast.root)
        # Program Break
        self.progBreak()
        self.backpatch()
        print(self)

        
    ''' Generation Tools '''

    # Add static values and handle all the temp value stuff
    def addStatic(self, var, scope):
        # stealing format of var@scope from alans example because there 
        # is no cleaner way to represent this.
        key =  f'{var.name}@{str(scope)}'
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
        temp_addr = self.__static[f'{id}@{self.__scope}'][0]
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

            self.log(f'Backpatching [ {temp_addr} ] to [ {addr+"00"} ]')
            for index, hex in enumerate(self.__code):
                # match the TX val in the code and static table
                if hex == temp_addr[:2]:
                    self.__code[index] = addr
                    # Add 00's for little endian
                    self.__code[index+1] = '00'

    ''' Code Generation '''

    def generateStatement(self, node):
        self.log(f'Found {node.name}')

        if node.name == 'Block':
            self.generateBlock(node)
        elif node.name == 'VarDecleration':
           self.generateVarDecleration(node)
        elif node.name == 'AssignmentStatement':
            self.generateAssignmentStatement(node)
        elif node.name == 'PrintStatement':
            self.generatePrintStatement(node)
        elif node.name == 'WhileStatement':
            pass
        elif node.name == 'IfStatement':
            pass

    def generateBlock(self, node):
        self.__scope += 1
        self.log(f'Creating New Block with Scope: {self.__scope}')
        for child in self.__cur_symtable.children:
            if child.scope is self.__scope:
                self.__cur_symtable = child

        for node in node.children:
            self.generateStatement(node)
        
    
    def generateVarDecleration(self, node):
        # TODO: rearange scoping, gotta get the right one
        # Load the accumulator with 0
        self.loadAccConst('00')

        # Store the accumulator in temp location 
        # Add new temp value to static table
        var = node.children[1]
        temp = self.addStatic(var, self.__scope)
        self.storeAccMem(temp)

    def generateAssignmentStatement(self, node):
        # Get the type of the assignment statement
        id = node.children[0].name
        value = node.children[1].name
        type = self.getType(value)

        if type is 'int':
            # load the value into the accumulator
            value = '0' + node.children[1].name
            self.loadAccConst(value)
            
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
            temp = self.getTempAddr(value)
            self.loadAccMem(temp)


        temp = self.getTempAddr(id)
        self.storeAccMem(temp)
        

    def generatePrintStatement(self, node):
        # Get the type of the value
        value = node.children[0].name
        val_type = self.getType(value)
        
        print(val_type)
        if val_type is 'int':
            # load y reg with value
            self.loadYRegConst(value)
           
        elif val_type is 'string':
            pass
        elif val_type is 'variable':
            # load the y reg from mem
            temp = self.getTempAddr(value)
            self.loadYRegMem(temp)

            # load the X reg with 1 and Sys call
            self.loadXRegConst('1')
            self.sysCallPrint()


    ''' Op Codes '''
    # some of these op codes have no reason to be there own methods
    # however it makes everything easier to read

    # explanation for syntax: *variable...
    # it will unpack the contents of the var,
    # I use it often below for tuples and lists

    # A9 -- Load the accumulator with a constant
    def loadAccConst(self, constant):
        self.append(['A9', constant])

    # AD -- Load the accumulator from memory
    def loadAccMem(self, addr):
        self.append(['AD', *addr])

    # 8D -- Store the accumulator in memory
    def storeAccMem(self, addr):
        self.append(['8D', *addr])

    # 6D -- Read from memory and add to the accumulator
    def addToAcc(self, addr):
        self.append(['6D', *addr])

    # A2 -- Load the x register with a given constant
    def loadXRegConst(self, constant):
        self.append(['A2', ('0'+constant)])

    # AE -- Load the x register from memory
    def loadXRegMem(self, addr):
        self.append(['AE', *addr])

    # A0 -- Load the y register with a given constant
    def loadYRegConst(self, constant):
        self.append(['A0', ('0'+constant)])

    # AC -- Load the y register from memory
    def loadYRegMem(self, addr):
        self.append(['AC', *addr])

    # EA -- No Operation
    def noOP(self):
        self.append('EA')

    # 00 -- break
    def progBreak(self):
        self.append('00')

    # EC -- Take a byte from memory and compare it with the x Register...if equal z flag is 0
    # D0 -- if flag is 0, branch x number of bytes
    # EE -- Increment the value of a byte
    
    # FF -- System Call...print
    def sysCallPrint(self):
        self.append('FF')



        
        
