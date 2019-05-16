#!/usr/bin/python3
# 2019-4-18
# Daniel Nicolas Gisolfi

import re
from error import Error
from warning import Warning
from termcolor import colored

class CodeGenerator:
    def __init__(self, verbose, program, ast, symtable):
        self.__ast = ast
        self.__symtable = symtable
        self.__code = []
        self.__heap = []
        self.__static = {}
        self.__dynamic = {}
        self.__jump = {}
        self.__scope = -1
        self.__cur_symtable = symtable
        self.__temp_addr_count = 0
        self.__jump_count = 0
        self.verbose = verbose
        self.program = program
        self.errors = 0
        self.warnings = 0
        print(colored(f'\nGenerating Program {self.program}', 'blue', attrs=['bold']))
        self.generate()
        if self.errors is 0:
            self.checkMemoryLimit()
            print(colored(f'Code Generation Completed for Program {self.program}', 'blue', attrs=['bold']))

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

    def error(self, msg):
        if self.errors is 0:
            Error('Code Generation', msg)
            self.errors += 1

    def log(self, msg):
        if self.verbose and self.errors is 0:
            print(colored(f'GENERATOR ❯ {msg}', 'blue'))

    def checkMemoryLimit(self):
        if len(self.code) > 256:
            self.error(f'Maximum Memory Limit of 256 Bytes Exceeded')

    def generate(self):
        # The Program must always start with a block
        self.generateBlock(self.__ast.root)
        # Program Break
        self.progBreak()
        self.backpatch()
        self.mergeHeap()
        
    ''' Generation Tools '''
    # Add static values and handle all the temp value stuff
    def addStatic(self, var, var_type):
        # stealing format of var@scope from alans example because there 
        # is no cleaner way to represent this.
        key =  f'{var}@{str(self.__scope)}'

        temp_addr = f'T{self.__temp_addr_count}XX'
        offset = len(self.__static)+1

        self.__static[key] = [temp_addr, var_type, offset]
        self.__temp_addr_count += 1
        return temp_addr[:2], temp_addr[2:]

    def addJump(self):
        self.__jump_count
        key = f'J{self.__jump_count}'
        self.__jump[key] = 0
        self.branch(key)
        jump_distance = len(self.code)-1
        self.__jump_count += 1
        return jump_distance

    def getTemp(self, var):
        scope = self.__scope
        symbol_table = self.__cur_symtable
        while scope is not -1:
            if symbol_table.get(var) is not None:
                return self.__static.get(f'{var}@{symbol_table.scope}', None)
            else:
                symbol_table = symbol_table.parent
                scope -= 1
       
        return None

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
        hex_string = []
        for char in string:
            hex_string.append(self.hex(ord(char)))
        # The string terminator
        hex_string.append('00')
        self.__heap = hex_string + self.__heap

        pointer = self.hex(255-len(self.__heap)+1)
        self.__dynamic[string] = pointer
        return pointer

    def getPointer(self, string):
        return self.__dynamic.get(string, None)

    def hex(self, decimal):
        return ("0x%02X" % decimal).upper()[2:]

    def getType(self, value):
        if value.isdigit() and re.match(r'[0-9]', value):
            return 'int'
        elif value in ['true', 'false']:
            return 'boolean'
        elif value == 'CharList':
            return 'string'
        elif re.match(r'[a-z]', value):
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
        if len(self.__code) is 0:
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
            self.generateWhileStatement(node)
        elif node.name == 'IfStatement':
            self.generateIfStatement(node)

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
        temp_addr = self.addStatic(var.name, var_type)
        
        if var_type != 'string':
            # Load the accumulator with 0
            self.loadAccConst('00')
            # Store the accumulator in temp location 
            # Add new temp value to static table
            self.storeAccMem(temp_addr)

    def generateAssignmentStatement(self, node):
        # Get the type of the assignment statement
        var = node.children[0].name
        value = node.children[1]
        val_type = self.generateExpr(value, 'Acc')
        
        if val_type is 'string':
            if self.getTempAddr(var) is None:
                self.addStatic(node.children[0].name, 'string')
        
        temp_addr = self.getTempAddr(var)
        self.storeAccMem(temp_addr)
        

    def generatePrintStatement(self, node):
        value = node.children[0]
        if value.name in ['IsEqual', 'NotEqual']:
            self.generateBoolean(value)
        
            # before doing anything get a pointer 
            # to each of the values in memory
            if self.getPointer('true') is None:
                self.addToHeap('true')
            true_pointer = self.getPointer('true')
            if self.getPointer('false') is None:
                self.addToHeap('false')
            false_pointer = self.getPointer('false')

            # add a jump entry to the table
            jump1 = self.addJump()

            self.loadYRegConst(true_pointer)
            self.loadXRegConst(self.hex(2))
            self.sysCallPrint()
            
            self.loadXRegConst(self.hex(2))
            self.loadAccConst(self.hex(1))
            temp_addr = self.addStatic(f'CompVal{self.__temp_addr_count}', 'int')
            self.storeAccMem(temp_addr)
            self.xRegCompare(temp_addr)
            jump2 = self.addJump()
            # jump 5 ahead to the FF call
            self.code[jump2] = self.hex(5)
            self.code[jump1] = self.hex((len(self.code) - jump1) - 1)
        
            self.loadYRegConst(false_pointer)
            self.loadXRegConst(self.hex(2))
            self.sysCallPrint()

        else:
            val_type = self.generateExpr(value, 'Y')

            if val_type is 'int':
                self.loadXRegConst(self.hex(1))
            else:
                # go to a memory location
                self.loadXRegConst(self.hex(2))
            self.sysCallPrint() 

    def generateIfStatement(self, node):
        bool_expr = node.children[0]
        block = node.children[1]
        self.generateBoolean(bool_expr)

        jump = self.addJump()
        self.generateBlock(block)
        self.code[jump] = self.hex((len(self.code) - jump) - 1)

    def generateWhileStatement(self, node):
        bool_expr = node.children[0]
        block = node.children[1]
        destination = len(self.code)
        self.generateBoolean(bool_expr)

        jump1 = self.addJump()
        self.generateBlock(block)
        self.loadXRegConst(self.hex(2))
        self.loadAccConst(self.hex(1))
        temp_addr = self.addStatic(f'CompVal{self.__temp_addr_count}', 'int')
        self.storeAccMem(temp_addr)
        self.xRegCompare(temp_addr)
        jump2 = self.addJump()
        loc = (256 - len(self.code))
        self.code[jump2] = self.hex(loc + destination)
        self.code[jump1] = self.hex((len(self.code) - jump1) - 1)


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
            addr = self.generateAddition(node)
            self.loadRegMem(register, addr)
            return 'int'

        elif value is 'true':
            string = value
            # get the address of the boolean value in memory
            if self.getPointer(string) is None:
                # add it to the heap if its not present
                self.addToHeap(string)
            # get a pointer to its address in memeory
            pointer = self.getPointer(string)

            self.loadRegConst(register, pointer)
            return 'boolean'

        elif value is 'false':
            string = value
            # get the address of the boolean value in memory
            if self.getPointer(string) is None:
                # add it to the heap if its not present
                self.addToHeap(string)
            # get a pointer to its address in memeory
            pointer = self.getPointer(string)

            self.loadRegConst(register, pointer)
            return 'boolean'

        elif val_type is 'variable':
            temp_entry = self.getTemp(value)
            temp_addr = self.getTempAddr(value)
            temp_type = temp_entry[1]

            self.loadRegMem(register, temp_addr)
            return temp_type


    def generateBoolean(self, node):
        # If the first var is just a normal boolean 
        # we can start generating code for it
        if node.name in ['true', 'false']:
            string = node.name
            # get the address of the value 'true' in memory
            if self.getPointer(string) is None:
                self.addToHeap(string)
            pointer = self.getPointer(string)
            # load the pointer as a constant
            self.loadXRegConst(pointer)
            self.loadAccConst(pointer)
            temp_addr = self.addStatic(node.name, 'boolean')
            # Now store the pointer into the temp address
            self.storeAccMem(temp_addr)
        else:
            left_expr = node.children[0]
            right_expr = node.children[1]

            # Two nested bool expr
            if left_expr.name in ['IsEqual', 'NotEqual'] and right_expr.name in ['IsEqual', 'NotEqual']:
                # both exprs are boolean exprs, put result of right expr in X reg
                self.generateBooleanExpr(left_expr)
                temp_addr = self.generateBooleanExpr(right_expr)
                self.loadXRegMem(temp_addr)

            # Left nested bool expr
            elif left_expr.name in ['IsEqual', 'NotEqual']:
                # there is a nested boolexpr
                self.generateExpr(right_expr, 'X')
                temp_addr = self.generateBooleanExpr(left_expr)

            # Right nested bool expr
            elif right_expr.name in ['IsEqual', 'NotEqual']:
                # there is a nested boolexpr
                self.generateExpr(left_expr, 'X')
                temp_addr = self.generateBooleanExpr(right_expr)

            # No nested bool exprs
            else:
                temp_addr = self.generateBooleanExpr(node)

        self.xRegCompare(temp_addr)

        # Add additional jump for a not equal case
        if node.name == 'NotEqual':
            self.generateNotEqualExpr()
        
        return temp_addr


    def generateBooleanExpr(self, node):
        left_expr = node.children[0]
        right_expr = node.children[1]
        
        self.generateExpr(left_expr, 'X')
        right_expr_type = self.getType(right_expr.name)
        # the right expression is not as easy, generate the needed code below
        
        if right_expr.name == 'Add':
            temp_addr = self.generateAddition(right_expr)
        elif right_expr.name in ['IsEqual', 'NotEqual']:
            temp_addr = self.generateBoolean(node)

        if right_expr_type == 'boolean':
            string = right_expr.name

            # get the address of the boolean value in memory
            if self.getPointer(string) is None:
                # add it to the heap if its not present
                self.addToHeap(string)
            # get a pointer to its address in memeory
            pointer = self.getPointer(string)

            # take the pointer and store it in the static variable location
            self.loadAccConst(pointer)
            temp_addr = self.addStatic(f'CompVal{self.__temp_addr_count}', 'boolean')
            self.storeAccMem(temp_addr) 

        elif right_expr_type == 'string':
            string = right_expr.children[0].name
            # check if the string has already been stored in the heap
            if self.getPointer(string) is None:
                # if not add to the heap
                self.addToHeap(string)
            # wether just added or already found, grab the pointer to the 
            # string in the heap
            pointer = self.getPointer(string)
            
            # Store the pointer to the string in the static location for that value
            self.loadAccConst(pointer)
            temp_addr = self.addStatic(f'CompVal{self.__temp_addr_count}', 'string')
            self.storeAccMem(temp_addr)

        elif right_expr_type == 'int':
            integer = int(right_expr.name)
            self.loadAccConst(self.hex(integer))
            temp_addr = self.addStatic(f'CompVal{self.__temp_addr_count}', 'int')
            self.storeAccMem(temp_addr)
        elif right_expr_type == 'variable':
            temp_addr = self.getTempAddr(right_expr.name)

        return temp_addr
    

    def generateNotEqualExpr(self):
        self.loadAccConst(self.hex(0))
        jump = self.addJump()
        # jump ahead 2 to the FF call
        self.code[jump] = self.hex(2)
        self.loadAccConst(self.hex(1))
        temp_addr = self.addStatic(f'CompVal{self.__temp_addr_count}', 'int')
        self.storeAccMem(temp_addr)
        self.loadXRegConst(self.hex(0))
        self.xRegCompare(temp_addr)

    def generateAddition(self, node):
        value1 = node.children[0].name
        # in the addition statement the value can be either a int or a var(of type int)
        # first load the Acc with the first value, the first value can't be a var
        # so we don't have to check
        self.loadAccConst(self.hex(int(value1)))
        
        # Now store the value in memory for future use
        add_addr = self.addStatic(f'ADD_VAL{self.__temp_addr_count}', 'int')
        self.storeAccMem(add_addr)
        value = node.children[1]
        while( value.name == 'Add'):
            # load Acc with the next value in the addition tree
            self.loadAccConst(self.hex(int(value.children[0].name)))
            # Add the value located at the sum to the new digit in the Acc
            self.addToAcc(add_addr)
            # save the new sum in the Acc for further use
            self.storeAccMem(add_addr)
            # get the next sub tree
            value = value.children[1]

        # the last value , could be a var or digit
        # if it is a var....
        if re.match(r'[a-z]', value.name):
            # get the temp address of the var
            temp_addr = self.getTempAddr(value.name)
            # add the value located at the address to the Acc
            self.addToAcc(temp_addr)
            self.storeAccMem(add_addr)
        else:
            # just one more digit, do the usual...
            self.loadAccConst(self.hex(int(value.name)))
            self.addToAcc(add_addr)
            self.storeAccMem(add_addr)

        # return the address at which to find the summed value
        return add_addr
        
           
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