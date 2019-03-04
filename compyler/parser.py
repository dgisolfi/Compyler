#!/usr/bin/python3
# 2019-2-12
from tree import Tree
from error import Error
from termcolor import colored
# from production import createProductions
# from tree import Tree
class Parser:
    def __init__(self, tokens, verbose, program):
        # Reverses tokens so I can use pop
        self.__tokens = tokens[::-1]
        self.cst = Tree()
        self.verbose = verbose
        self.warnings = 0
        self.errors = 0
        self.program = program     
        self.parse()

    # Check if the current token is an appropriate token for the scope
    def match(self, current_token, expected_tokens):
        retval = False
        # print(current_token, expected_tokens)
        if current_token in expected_tokens:
            retval = True
        return retval
    
    # This handles all error messages
    # as it was getting messy inside of function
    def error(self, token, expected):
        Error('Parser', f'Expected {expected} found {token.value}', 
        token.line, token.position)
        self.errors += 1
        # Get outta here this program is not Alan++ Compliant
        self.exit()

    def exit(self):
        # Fail the Parser if there were any errors
        if self.errors > 0:
            print(colored(f'Parse Failed for Program {self.program}. Errors: {self.errors}\n', 'red'))
        else:
            print(colored(f'Parse Completed for Program {self.program}. Errors: {self.errors}\n', 'blue'))

    def logProduction(self, fn):
        if self.verbose:
            print(colored(f'PARSER ❯ {fn}', 'green'))
    
    ''' All productions to preform "derivations" '''
    
    def parse(self):
        print(colored(f'Parsing Program {self.program}', 'blue'))
        self.logProduction('parse()')
        self.cst.addNode('parse', 'branch')
        
        # The most basic program is <block>$, 
        # so check for block and then $
        if self.parseBlock():
            
            current_token = self.__tokens.pop()
            if self.match(current_token.kind, 'T_EOP'):
                self.cst.cutOffChildren()
                self.cst.addNode(current_token.value, 'leaf')
                # We finished with 0 errors, exit safely now.
                self.exit()
            else:
                self.error(current_token, 'T_EOP')

    
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
            self.cst.addNode(current_token.value, 'leaf')

            # Check the contents of the block
            if self.parseStatementList(): 
                # There better be a right brace to close this block
                current_token = self.__tokens.pop()
                if self.match(current_token.kind, 'T_RIGHT_BRACE'):
                    self.cst.addNode(current_token.value, 'leaf')
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
            # print(f'NAME:{self.cst.current_node.name}')
            while self.cst.current_node.name is 'StatementList':
                # print(f'NAME:{self.cst.current_node.name}')
                self.cst.cutOffChildren()

            # Epsilon
            return True

    def parseStatement(self):
        self.logProduction('parseStatement()')
        self.cst.addNode('Statement', 'branch')

        # Check all possible statements
        if self.parseBlock() or self.parsePrintStatement() or (self.parseAssignmentStatement() 
        or self.parseVarDecl() or self.parseWhileStatement()):
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
            self.cst.addNode(current_token.value, 'leaf')

            current_token = self.__tokens.pop()
            # The next token better be a open paren
            if self.match(current_token.kind, 'T_LEFT_PAREN'):
                self.cst.addNode(current_token.value, 'leaf')
                # Check for expr inside parens
                if self.parseExpr():
                    self.cst.cutOffChildren()
                
                    # Check for closing paren
                    current_token = self.__tokens.pop()
                    if self.match(current_token.kind, 'T_RIGHT_PAREN'):
                        self.cst.addNode(current_token.value, 'leaf')
                        return True
                    else:
                        self.error(current_token, 'T_RIGHT_PAREN')
                else:
                    self.error(current_token, 'Expr')
            else:
                self.error(current_token, 'T_LEFT_PAREN')
        else:
            return False

    def parseAssignmentStatement(self):
        # Look at the next token but dont remove until we are sure this is a print statement
        current_token = self.__tokens[-1]

        if self.match(current_token.kind, 'T_ID'):
            # We are sure this is a Assignment so pop the token
            current_token = self.__tokens.pop()
            self.logProduction('parseAssignmentStatement()')
            self.cst.addNode('AssignmentStatement', 'branch')
            self.parseId(current_token)
           
            current_token = self.__tokens.pop()
            # Now look for the actual '='
            if self.match(current_token.kind, 'T_ASSIGN_OP'):
                self.cst.addNode(current_token.value, 'leaf')

                # Finally validate what the ID is being assigned to
                if self.parseExpr():
                    self.cst.cutOffChildren()
                    return True
                else:
                    self.error(current_token, 'Expr')
            else:
                self.error(current_token, 'T_ASSIGN_OP')
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
            self.cst.addNode(current_token.value, 'leaf')
            
            current_token = self.__tokens.pop()
            if self.match(current_token.kind, 'T_ID'):
                self.parseId(current_token)
                return True
            else:
                self.error(current_token, 'T_ID')
        else:
            # Not a valid decleration
            return False
    
    def parseWhileStatement(self):
        return False

    def parseIfStatement(self):
        return False

    # Expressions
    def parseExpr(self):
        self.logProduction('parseExpr()')
        self.cst.addNode('Expr','branch')
        current_token = self.__tokens.pop()

        if self.match(current_token.kind, 'T_ID'):
            # New Expr ID
            self.parseId(current_token)
            return True

        # New Expr INT, BOOL or String
        elif self.parseIntExpr()  or self.parseBooleanExpr() or self.parseStringExpr():
            self.cst.cutOffChildren()
            return True
        else:
            return False

    def parseIntExpr(self):
        return False
    def parseStringExpr(self):
        return False
    def parseBooleanExpr(self):
        return False

    def parseId(self, id_token):
        self.logProduction('parseId()')
        self.cst.addNode('ID', 'branch')
        self.cst.addNode(id_token.value,'leaf')
        # go back to parent node
        self.cst.cutOffChildren()
        return False
    
    def parseCharList(self):
        return False

    def parseType(self):
        return False

    def parseChar(self):
        return False

    def parseSpace(self):
        return False

    def parseDigit(self):
        return False

    def parseBoolOp(self):
        return False
    def parseBoolVal(self):
        return False
    def parseIntOp(self):
        return False