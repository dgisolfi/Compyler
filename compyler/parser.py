#!/usr/bin/python3
# 2019-2-12
# Daniel Nicolas Gisolfi

from tree import Tree
from error import Error
from termcolor import colored

class Parser:
    def __init__(self, tokens, verbose, printmode, program):
        # Reverses tokens so I can use pop...cleans 
        # up the code significantly
        self.__tokens = tokens[::-1]
        self.cst = Tree(printmode)
        self.verbose = verbose
        self.warnings = 0
        self.errors = 0
        self.program = program     
        self.parse()

    # Check if the current token is an appropriate token for the scope
    def match(self, current_token, expected_tokens):
        retval = False
        if current_token in expected_tokens:
            retval = True
        return retval
    
    # This handles all error messages
    # as it was getting messy inside of function
    def error(self, token, expected):
        if self.errors is 0:
            Error('Parser', f'Expected [ {expected} ] found [ {token.value} ]', 
            token.line, token.position)
            self.errors += 1

    def exit(self):
        # Fail the Parser if there were any errors
        if self.errors > 0:
            print(colored(f'Parse Failed for Program {self.program}.\n', 'red'))
        else:
            print(colored(f'Parse Completed for Program {self.program}.\n', 'magenta', attrs=['bold']))

    def logProduction(self, fn):
        if self.verbose and self.errors is 0:
            print(colored(f'PARSER ❯ {fn}', 'magenta'))
    
    ''' All productions to preform "derivations" '''
    def parse(self):
        print(colored(f'Parsing Program {self.program}', 'magenta', attrs=['bold']))
        self.logProduction('parse()')
        self.cst.addNode('program', 'branch')

        # This is grabbing the first token but not removing it, 
        # this is so if the first '{' is left out we can say what was 
        # in its place
        current_token = self.__tokens[-1]
        
        # The most basic program is <block>$, 
        # so check for block and then $
        if self.parseBlock():
            current_token = self.__tokens.pop()
            if self.match(current_token.kind, 'T_EOP'):
                self.cst.cutOffChildren()
                # print(current_token.line)
                self.cst.addNode(current_token.value, 'leaf', 
                line=current_token.line, pos=current_token.position)

                # We finished with 0 errors, exit safely now.
                self.exit()
            else:
                self.error(current_token, '$')
        else:
            self.error(current_token, '{')

    
    def parseBlock(self):
        # Look at the next token but dont remove until we are sure this is a print statement
        current_token = self.__tokens[-1]
        # Match open brace of block
        if self.match(current_token.kind, 'T_LEFT_BRACE'):
            # Actually remove it now
            current_token = self.__tokens.pop()
            # New Block
            self.logProduction('parseBlock()')
            self.cst.addNode('Block', 'branch')
            self.cst.addNode(current_token.value, 'leaf',
            line=current_token.line, pos=current_token.position)

            # Check the contents of the block
            if self.parseStatementList(): 
                # There better be a right brace to close this block
                current_token = self.__tokens.pop()
                if self.match(current_token.kind, 'T_RIGHT_BRACE'):
                    self.cst.addNode(current_token.value, 'leaf',
                    line=current_token.line, pos=current_token.position)
                else:
                    self.error(current_token, '}')
                    return False
            # This is a valid block
            return True
        else:
            # No block detected, move on
            return False

    def parseStatementList(self):
        self.logProduction('parseStatementList()')
        self.cst.addNode('StatementList', 'branch')
        
        if self.parseStatement():
            # Move up the tree
            self.cst.cutOffChildren()
            return self.parseStatementList()
        else:
            while self.cst.current_node.name is 'StatementList':
                self.cst.cutOffChildren()
            # Epsilon
            return True

    def parseStatement(self):
        self.logProduction('parseStatement()')
        self.cst.addNode('Statement', 'branch')

        # Check all possible statements
        if self.parseBlock() or self.parsePrintStatement() or (self.parseAssignmentStatement() 
        or self.parseIfStatement() or self.parseVarDecl() or self.parseWhileStatement()):
            self.cst.cutOffChildren()
            return True
        else:
            # Remove the Statement branch node we didnt need it
            self.cst.delCurNode()
            return False

    # All possible statements 
    def parsePrintStatement(self):
        # Look at the next token but dont remove until we are sure this is a print statement
        current_token = self.__tokens[-1]

        if self.match(current_token.kind, 'T_PRINT'):
            # Actually remove it now
            current_token = self.__tokens.pop()

            # New Print Statement
            self.logProduction('parsePrintStatement()')
            self.cst.addNode('PrintStatement', 'branch')
            self.cst.addNode(current_token.value, 'leaf',
            line=current_token.line, pos=current_token.position)

            current_token = self.__tokens.pop()
            # The next token better be a open paren
            if self.match(current_token.kind, 'T_LEFT_PAREN'):
                self.cst.addNode(current_token.value, 'leaf',
                line=current_token.line, pos=current_token.position)
                # Check for expr inside parens
                if self.parseExpr():
                    self.cst.cutOffChildren()
                    # Check for closing paren
                    current_token = self.__tokens.pop()
                    if self.match(current_token.kind, 'T_RIGHT_PAREN'):
                        self.cst.addNode(current_token.value, 'leaf',
                        line=current_token.line, pos=current_token.position)
                        return True
                    else:
                        self.error(current_token, ')')
                else:
                    self.error(current_token, 'ID, Int, String, or Boolean')
            else:
                self.error(current_token, '(')
        else:
            return False

    def parseAssignmentStatement(self):
        # Look at the next token but dont remove until we are sure this is a print statement
        current_token = self.__tokens[-1]

        if self.match(current_token.kind, 'T_DIGIT') or self.match(current_token.kind, 'T_QUOTE'):
            self.error(current_token, 'ID')   

        if self.match(current_token.kind, 'T_ID'):
            # We are sure this is a Assignment so pop the token
            self.logProduction('parseAssignmentStatement()')
            self.cst.addNode('AssignmentStatement', 'branch')
            self.parseId()
           
            current_token = self.__tokens.pop()
            # Now look for the actual '='
            if self.match(current_token.kind, 'T_ASSIGN_OP'):
                self.cst.addNode(current_token.value, 'leaf',
                line=current_token.line, pos=current_token.position)

                # Finally validate what the ID is being assigned to
                if self.parseExpr():
                    self.cst.cutOffChildren()
                    return True
                else:
                    self.error(current_token, 'ID, Int, String, or Boolean')
            else:
                self.error(current_token, '=') # T_ASSIGN_OP
        else:
            # Not an Assignment statement or not 
            # valid(didnt start with a ID)
            return False
    
    def parseVarDecl(self):
        # Look at the next token but dont remove until we are sure this is a print statement
        current_token = self.__tokens[-1]

        if self.match(current_token.kind, 'T_TYPE'):
            # We are sure this is a Assignment so pop the token
            current_token = self.__tokens.pop()
            self.logProduction('parseVarDecl()')
            self.cst.addNode('VarDecleration', 'branch')
            self.parseType(current_token)
            
            current_token = self.__tokens[-1]
            if self.parseId():
                return True
            else:
                self.error(current_token, 'ID')
        else:
            # Not a valid decleration
            return False
    
    def parseWhileStatement(self):
        current_token = self.__tokens[-1]
        
        if self.match(current_token.kind, 'T_WHILE'):
            current_token = self.__tokens.pop()
            self.logProduction('parseWhileStatement()')
            self.cst.addNode('WhileStatement', 'branch')

            if self.parseBooleanExpr():
                self.cst.cutOffChildren() 
                if self.parseBlock():
                    self.cst.cutOffChildren()
                    
                    return True
                else:
                    self.error(self.__tokens[-1], '{')
                    return False
            else:
                self.error(self.__tokens[-1], 'BooleanExpr')
                return False
        else:
            return False

    def parseIfStatement(self):
        current_token = self.__tokens[-1]
        
        if self.match(current_token.kind, 'T_IF'):
            current_token = self.__tokens.pop()
            self.logProduction('parseIfStatement()')
            self.cst.addNode('IfStatement', 'branch')
            if self.parseBooleanExpr(): 
                self.cst.cutOffChildren()
               
                if self.parseBlock():
                    self.cst.cutOffChildren()
                    return True
                else:
                    self.error(self.__tokens[-1], 'T_LEFT_BRACE')
                    return False
            else:
                self.error(self.__tokens[-1], 'BooleanExpr')
                return False
        else:
            return False

    # Expressions
    def parseExpr(self):
        self.logProduction('parseExpr()')
        self.cst.addNode('Expr','branch')

         # New Expr INT, BOOL or String
        if self.parseIntExpr() or self.parseBooleanExpr() or self.parseStringExpr():
            self.cst.cutOffChildren()
            return True

        elif self.parseId():
            # New Expr ID
            return True
            
        else:
            return False

    def parseIntExpr(self):
        # Look at the next token but dont remove until we are sure this is a print statement
        current_token = self.__tokens[-1]
        if self.match(current_token.kind, 'T_DIGIT'):
            self.logProduction('parseIntExpr()')
            self.cst.addNode('IntExpr','branch')
            if self.parseDigit():
                if self.parseIntOp():
                    if self.parseExpr():
                       self.cst.cutOffChildren()
                       return True
                    else:
                        self.error(current_token, 'Expr')
                else:
                    # this is valid => a = 3
                    return True
            else:
                self.error(current_token,'digit(0-9)')
                
        else:
            # Its not a IntEpr
            return False

    def parseStringExpr(self):
        # Check for quote else dis aint a string
        current_token = self.__tokens[-1]

        if self.match(current_token.kind, 'T_QUOTE'):
            current_token = self.__tokens.pop()
            self.logProduction('parseStringExpr()')
            self.cst.addNode('StringExpr','branch')
            self.cst.addNode(current_token.value, 'leaf',
            line=current_token.line, pos=current_token.position)
            self.cst.addNode('CharList','branch')
           
                
            if self.parseCharList():
                current_token = self.__tokens.pop()
                if self.match(current_token.kind, 'T_QUOTE'):
                    self.cst.addNode(current_token.value, 'leaf',
                    line=current_token.line, pos=current_token.position)
                    return True
                else:
                    self.error(self.__tokens[-1], 'T_Quote')
            else:
                self.error(self.__tokens[-1], 'Charlist')
        else:
            return False

    def parseBooleanExpr(self):
        # Check for BoolOp first
        current_token = self.__tokens[-1]

        if self.match(current_token.kind, 'T_BOOLEAN'):
            self.logProduction('parseBooleanExpr()')
            self.cst.addNode('BooleanExpr','branch')
            self.parseBoolVal()
            return True
        elif self.match(current_token.kind, 'T_LEFT_PAREN'):
            current_token = self.__tokens.pop()
            self.logProduction('parseBooleanExpr()')
            self.cst.addNode('BooleanExpr','branch')
            self.cst.addNode(current_token.value,'leaf',
            line=current_token.line, pos=current_token.position)

            if self.parseExpr():
                self.cst.cutOffChildren()
                
                if self.parseBoolOp():

                    if self.parseExpr():
                        self.cst.cutOffChildren()

                        current_token = self.__tokens.pop()
                        if self.match(current_token.kind, 'T_RIGHT_PAREN'):
                            self.cst.addNode(current_token.value,'leaf',
                            line=current_token.line, pos=current_token.position)

                            return True
                        else:
                            self.error(current_token, ')')
                    else:
                        self.error(current_token, 'Expr')
                else:
                    self.error(current_token, '== or !=')
            else:
                self.error(current_token, 'Expr')
        else:
            # Not a valid BoolExpr
            return False

    def parseId(self):
        current_token = self.__tokens[-1]

        if self.match(current_token.kind, 'T_ID'):
            current_token = self.__tokens.pop()
            # We dont need to check for char as 
            # the lexer already took care of that
            self.logProduction('parseId()')
            self.cst.addNode('Id', 'branch')
            self.cst.addNode(current_token.value,'leaf',
            line=current_token.line, pos=current_token.position)
            # go back to parent node
            self.cst.cutOffChildren()
            return True
        else:
            return False
    
    def parseCharList(self):
        self.logProduction('parseCharList()')

        if self.parseChar():
            return self.parseCharList()
        else:
            # move back up tree to get back to the branch node
            while self.cst.current_node.name is 'CharList':
                self.cst.cutOffChildren()
            return True

    def parseType(self, type_token):
        self.logProduction('parseType()')
        self.cst.addNode('Type', 'branch')
        self.cst.addNode(type_token.value,'leaf',
        line=type_token.line, pos=type_token.position)
        # go back to parent node
        self.cst.cutOffChildren()

    def parseChar(self):
        current_token = self.__tokens[-1]
        
        if self.match(current_token.kind, 'T_CHAR'):
            current_token = self.__tokens.pop()
            self.logProduction('parseChar()')
            self.cst.addNode('char', 'branch')
            self.cst.addNode(current_token.value,'leaf',
            line=current_token.line, pos=current_token.position)
            # go back to parent node
            self.cst.cutOffChildren()
            return True
        else:
            # Not a char
            return False

    def parseDigit(self):
        self.logProduction('parseDigit()')
        current_token = self.__tokens.pop()
        if self.match(current_token.kind, 'T_DIGIT'):
            self.cst.addNode('digit', 'branch')
            self.cst.addNode(current_token.value,'leaf',
            line=current_token.line, pos=current_token.position)
            # go back to parent node
            self.cst.cutOffChildren()
            return True
        else:
            return False

    def parseBoolOp(self):
        current_token = self.__tokens[-1]

        if self.match(current_token.kind, 'T_BOOL_OP'):
            current_token = self.__tokens.pop()
            self.logProduction('parseBoolOp()')
            self.cst.addNode('BoolOp','branch')
            self.cst.addNode(current_token.value,'leaf',
            line=current_token.line, pos=current_token.position)
            self.cst.cutOffChildren()
            return True
        else:
            return False

    def parseBoolVal(self):
        current_token = self.__tokens[-1]

        if self.match(current_token.kind, 'T_BOOLEAN'):
            current_token = self.__tokens.pop()
            self.logProduction('parseBoolVal()')
            self.cst.addNode('BoolVal', 'branch')
            self.cst.addNode(current_token.value, 'leaf',
            line=current_token.line, pos=current_token.position)
            self.cst.cutOffChildren()
            return True
        else:
            return False

    def parseIntOp(self):
        current_token = self.__tokens[-1]

        if self.match(current_token.kind, 'T_ADDITION_OP'):
            current_token = self.__tokens.pop()
            self.cst.addNode('IntOP','branch')
            self.cst.addNode(current_token.value,'leaf',
            line=current_token.line, pos=current_token.position)
            self.cst.cutOffChildren()
            return True
        else:
            return False