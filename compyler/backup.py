def generateIsEqualBoolean(self, node):
        variable_1 = node.children[0]
        variable_2 = node.children[1]
        
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
            temp_addr = self.addStatic(variable_1.name, 'boolean')
            # Now store the pointer into the temp address
            self.storeAccMem(temp_addr)
            
        # Otherwise if it is and expresssion, we need to get the type of it
        else:
           temp_addr = self.generateBooleanExpr(variable_1, variable_2)

        self.xRegCompare(temp_addr)
      
    
    def generateNotEqualBoolean(self, node):
        self.loadAccConst(self.hex(0))
        jump = self.addJump()
        self.code[jump] = self.hex(2)
        self.loadAccConst(self.hex(1))
        temp_addr = self.addStatic(f'CompVal{self.__temp_addr_count}', 'int')
        self.storeAccMem(temp_addr)
        self.loadXRegConst(self.hex(0))
        self.xRegCompare(temp_addr)
        
    def generateBooleanExpr(self, variable_1, variable_2):
        variable_1_type = self.generateExpr(variable_1, 'X')
        variable_2_type = self.getType(variable_2.name)
        
        print(variable_1.name, variable_2.name)

        if variable_2.name == 'Add':
            pass

        if variable_2_type == 'boolean':
            string = variable_2.name

            # get the address of the boolean value in memory
            if self.getPointer(string) is None:
                # add it to the heap if its not present
                self.addToHeap(string)
            # get a pointer to its address in memeory
            pointer = self.getPointer(string)

            # take the pointer and store it in the static variable location
            self.loadAccConst(pointer)
            temp_addr = self.addStatic(string, 'boolean')
            self.storeAccMem(temp_addr)

        elif variable_2_type == 'string':
            string = variable_2.children[0].name
            # check if the string has already been stored in the heap
            if self.getPointer(string) is None:
                # if not add to the heap
                self.addToHeap(string)
            # wether just added or already found, grab the pointer to the 
            # string in the heap
            pointer = self.getPointer(string)
            
            # Store the pointer to the string in the static location for that value
            self.loadAccConst(pointer)
            temp_addr = self.addStatic(string, 'string')
            self.storeAccMem(temp_addr)

        elif variable_2_type == 'int':
            integer = int(variable_2.name)
            self.loadAccConst(self.hex(integer))
            temp_addr = self.addStatic(variable_2.name, 'int')
            self.storeAccMem(temp_addr)

        elif variable_2_type == 'variable':
            temp_addr = self.getTempAddr(variable_2.name)

        return temp_addr