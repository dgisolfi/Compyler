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
        self.__dynamic = {}
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
        self.mergeHeap()
        print(self)

        
    ''' Generation Tools '''

    # Add static values and handle all the temp value stuff
    def addStatic(self, var, var_type):
        # stealing format of var@scope from alans example because there 
        # is no cleaner way to represent this.
        key =  f'{var.name}@{str(self.__scope)}'
        temp_addr = f'T{self.__temp_addr_count}XX'
        offset = len(self.__static)

        self.__static[key] = [temp_addr, var_type, offset]
        self.__temp_addr_count += 1
        return temp_addr[:2], temp_addr[2:]


    def getTemp(self, var):
        scope = self.__scope
        symbol_table = self.__cur_symtable
        while scope is not -1:
            print(scope)
            if symbol_table.get(var) is not None:
                print(f'{var}@{scope}')
                return self.__static.get(f'{var}@{scope}', None)
            else:
                symbol_table = symbol_table.parent
                scope -= 1

    def getTempAddr(self, var):
        # If the addr exists at the current scope level,
        # than everthing is good, just return it.
        temp_entry = self.getTemp(var)
        # However if None is returned meaning it cannot be 
        # found at that scope level...we need to go deeper.
        if temp_entry is None:
            return None
        else:
            temp_addr = temp_entry[0]
            return temp_addr[:2], temp_addr[2:]

    def addToHeap(self, string):
        for char in string:
            self.__heap.append(self.hex(ord(char)))
        # The string terminator
        self.__heap.append('00')
        pointer = self.hex(255-len(self.__heap)+1)
        self.__dynamic[string] = pointer
        return pointer

    def getPointer(self, string):
        return self.__dynamic.get(string, None)

    def hex(self, decimal):
        return ("0x%02X" % decimal).upper()[2:]

    # def getVarType(self, variable):
    #     search = True
    #     while search:
    #         print(self.)
    #     if self.__static.get(variable):
    #         return self.
    #     else:
    #         return None

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
            offset = self.__static[key][2]

            # get the final address of the value
            addr = self.hex((len(self.__code)-1) + offset)

            self.log(f'Backpatching [ {temp_addr} ] to [ {addr+"00"} ]')
            for index, hex in enumerate(self.__code):
                # match the TX val in the code and static table
                if hex == temp_addr[:2]:
                    self.__code[index] = addr
                    # Add 00's for little endian
                    self.__code[index+1] = '00'

    def mergeHeap(self):
        # no use adding a ton of zeros if the heap went unused
        if len(self.__heap) is 0:
            return
    
        max_addr = 255-len(self.__heap)
        [self.append('00') for null in range(len(self.code)-1, max_addr)]
        self.append(self.__heap)

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
        var = node.children[1]
        var_type = node.children[0].name
        print(var_type)
        if var_type != 'string':
            # Load the accumulator with 0
            self.loadAccConst('00')
            # Store the accumulator in temp location 
            # Add new temp value to static table
            temp_addr = self.addStatic(var, var_type)
            self.storeAccMem(temp_addr)

    def generateAssignmentStatement(self, node):
        # Get the type of the assignment statement
        var = node.children[0].name
        val_type = self.generateExpr(node.children[1], 'Acc')

        if val_type is 'string':
            if self.getTempAddr(var) is None:
                temp_addr = self.addStatic(node.children[0], 'string')
        else:
            temp_addr = self.getTempAddr(var)

        self.storeAccMem(temp_addr)
        

    def generatePrintStatement(self, node):
        # TODO: check for BoolOp

        val_type = self.generateExpr(node.children[0], 'Y')
        # print(val_type)

        if val_type is 'int':
            self.loadXRegConst(self.hex(1))
        else:
            # go to a memory location
            self.loadXRegConst(self.hex(2))
        self.sysCallPrint() 


    def generateExpr(self, node, register):
        value = node.name
        val_type = self.getType(value)

        if val_type is 'int':
            integer = int(value)
            self.loadRegConst(register, self.hex(integer))
            return val_type
           
        elif val_type is 'string':
            value = node.children[0]
            string = value.name
            
            if self.getPointer(string) is None:
                self.addToHeap(string)

            pointer = self.getPointer(string)
            # load the pointer into the Y reg
            self.loadRegConst(register, pointer)
            return val_type

        elif value is 'Add':
            print('Addd')
        elif value is 'true':
            return 'boolean'
        elif value is 'false':
            return 'boolean'
        elif val_type is 'variable':
            # print(value)
            # print(self.__static)
            temp_addr = self.getTempAddr(value)

            self.loadRegMem(register, temp_addr)
            # TODO: get type of var
            return self.getTemp(value)[1]

           


    ''' Op Codes '''
    # some of these op codes have no reason to be there own methods
    # however it makes everything easier to read

    # explanation for syntax: *variable...
    # it will unpack the contents of the var,
    # I use it often below for tuples and lists

    def loadRegMem(self, reg, addr):
        if reg is 'X':
            self.loadXRegMem(addr)
        elif reg is 'Y':
            self.loadYRegMem(addr)
        elif reg is 'Acc':
            self.loadAccMem(addr)
    
    def loadRegConst(self, reg, const):
        if reg is 'X':
            self.loadXRegConst(const)
        elif reg is 'Y':
            self.loadYRegConst(const)
        elif reg is 'Acc':
            self.loadAccConst(const)

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
        self.append(['A2', constant])

    # AE -- Load the x register from memory
    def loadXRegMem(self, addr):
        self.append(['AE', *addr])

    # A0 -- Load the y register with a given constant
    def loadYRegConst(self, constant):
        self.append(['A0', constant])

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
    def xRegCompare(self, addr):
        self.append(['EC', *addr])

    # D0 -- if Z flag is 0, branch x number of bytes
    def branch(self, bytes):
        self.append(['D0', bytes]) 

    # EE -- Increment the value of a byte
    def inccByte(self, addr):
        self.append(['EE', *addr])

    # FF -- System Call...print
    def sysCallPrint(self):
        self.append('FF')