#!/usr/bin/python3
# 2019-2-12
from error import Error
from termcolor import colored
# from tree import Tree

class Parser:
    def __init__(self, tokens, verbose, program):
        self.__tokens = tokens
        self.token_pointer = 0
        self.current_token = self.__tokens[self.token_pointer]
        self.cst = None
        self.verbose = verbose
        self.warnings = 0
        self.errors = 0
        self.program = program
        self.parse()

    # Check if the current token is an appropriate token for the scope
   
    def match(self, current_token, expected_tokens):
        retval = False
        print(current_token, expected_tokens)
        if current_token in expected_tokens:
            retval = True
        return retval
    
    # After matching will consume the token
    def consume(self):
        if  self.token_pointer < len(self.__tokens)-1:
            self.token_pointer += 1
            self.current_token = self.__tokens[self.token_pointer]
        else:
            self.exit()

    def exit(self):
        # Fail the Parser if there were any errors
        if self.errors > 0:
            print(colored(f'Parse Failed for Program {self.program}. Errors: {self.errors}', 'red'))
        else:
            print(colored(f'Parse Completed for Program {self.program}. Errors: {self.errors}\n', 'blue'))
        # Reset incase of another program
        self.warnings = 0
        self.errors = 0

    def logProduction(self, fn):
        if self.verbose:
            print(colored(f'PARSER ❯ {fn}', 'cyan'))
    
    ''' All productions to preform "derivations" '''
    def parse(self):
        print(colored(f'Parsing Program {self.program}', 'blue'))
        self.parseProgram()

    def parseProgram(self):
        # Parse the block then Check for EOP!
        self.parseBlock()
        if not self.match(self.current_token.kind, ['T_EOP']):
            Error('Parser', f'Expected [ $ ] found {self.current_token} at', self.current_token.line, self.current_token.position)
            self.errors += 1
        else:
            self.consume()

    def parseBlock(self):
        # Match Open 
        if not self.match(self.current_token.kind, ['T_LEFT_BRACE']):
            # Cant use F string here as curly braces cant be escaped in them
            Error('Parser', 'Expected [ { ] found ' + str(self.current_token) +' at', 
            self.current_token.line, self.current_token.position)
            self.errors += 1
        else:
            self.consume()

        self.parseStatementList()
        # ...and close brace
        if not self.match(self.current_token.kind, ['T_RIGHT_BRACE']):
            # Cant use F string here as curly braces cant be escaped in them
            Error('Parser', 'Expected [ { ] found ' + str(self.current_token) +' at', 
            self.current_token.line, self.current_token.position)
            self.errors += 1
        else:
            self.consume()


    # Statements 
    def parseStatementList(self):
        pass

    def parseStatement(self):
        pass

    # All possible statements 
    def parsePrintStatement(self):
        pass

    def parseAssignmentStatement(self):
        pass
    
    def parseVarDecl(self):
        pass
    
    def parseWhileStatement(self):
        pass

    def parseIfStatement(self):
        pass

    # Expressions

    def parseExpr(self):
        pass
    def parseIntExpr(self):
        pass
    def parseStringExpr(self):
        pass
    def parseBooleanExpr(self):
        pass
    def parseId(self):
        pass
    
    def parseCharList(self):
        pass

    def parseType(self):
        pass

    def parseChar(self):
        pass

    def parseSpace(self):
        pass

    def parseDigit(self):
        pass

    def parseBoolOp(self):
        pass
    def parseBoolVal(self):
        pass
    def parseIntOp(self):
        pass

    
    
    

       
       

    
