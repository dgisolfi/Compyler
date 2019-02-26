#!/usr/bin/python3
# 2019-2-12
from tree import Tree
from error import Error
from termcolor import colored
# from production import createProductions
# from tree import Tree
class Parser:
    def __init__(self, tokens, verbose, program):
        self.__tokens = tokens
        self.token_pointer = 0
        self.current_token = self.__tokens[self.token_pointer]
        self.cst = Tree()
        self.verbose = verbose
        self.warnings = 0
        self.errors = 0
        self.program = program
        # self.productions = self.createProductions()

        # self.productions.get('Statement')['T_PRINT']()
     
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
            print(colored(f'PARSER ❯ {fn}', 'green'))
    
    ''' All productions to preform "derivations" '''
    def parse(self):
        print(colored(f'Parsing Program {self.program}', 'blue'))
        self.logProduction('parse()')
        self.cst.addNode('parse()', 'branch')
        self.parseProgram()
        self.cst.cutOffChildren()

    def parseProgram(self):
        self.logProduction('parseProgram()')
        self.cst.addNode('parseProgram()', 'branch')
        # Parse the block then Check for EOP!
        self.parseBlock()
        self.cst.cutOffChildren()

        if not self.match(self.current_token.kind, ['T_EOP']):
            Error('Parser', f'Expected [ $ ] found {self.current_token} at', self.current_token.line, self.current_token.position)
            self.errors += 1
        else:
            self.consume()

    def parseBlock(self):
        self.logProduction('parseBlock()')
        
        # Match Open 
        if not self.match(self.current_token.kind, ['T_LEFT_BRACE']):
            # Cant use F string here as curly braces cant be escaped in them
            Error('Parser', 'Expected [ { ] found ' + self.current_token.kind +' at', 
            self.current_token.line, self.current_token.position)
            self.errors += 1
        else:
            self.consume()
        
        self.cst.addNode('parseBlock()', 'branch')
        self.parseStatementList()
        self.cst.cutOffChildren()

        # ...and close brace
        if not self.match(self.current_token.kind, ['T_RIGHT_BRACE']):
            # Cant use F string here as curly braces cant be escaped in them
            Error('Parser', 'Expected [ } ] found ' + self.current_token.kind +' at', 
            self.current_token.line, self.current_token.position)
            self.errors += 1
        else:
            self.consume()
 


    # Statements 
    def parseStatementList(self):
        self.logProduction('parseStatementList()')
        
        while not self.match(self.current_token, ['T_RIGHT_BRACE']):
            self.parseStatement()
        
        return True

    def parseStatement(self):
        self.logProduction('parseStatement()')

        # Match for any valid statements
        if not self.match(self.current_token.kind, self.productions.get('Statement')):
            # Cant use F string here as curly braces cant be escaped in them
            Error('Parser', f'Expected {self.productions.get("Statement")} found {self.current_token.kind} at', 
            self.current_token.line, self.current_token.position)
            self.errors += 1
        else:
            self.consume()
            # productions_functions[self.current_token.kind]()
            

    # All possible statements 
    def parsePrintStatement(self):
        print('fuck')

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


    def createProductions(self):
        productions = {}

        statements = []
        statements.append({'T_PRINT':self.parsePrintStatement})
        statements.append({'T_ASSIGNMENT_OP':self.parseAssignmentStatement})
        statements.append({'T_TYPE':self.parseVarDecl})
        statements.append({'T_WHILE':self.parseWhileStatement})
        statements.append({'T_IF':self.parseIfStatement})
        statements.append({'T_LEFT_BRACE':self.parseBlock})

        expr = []
        expr.append({'T_INT':self.parseIntExpr})
        expr.append({'T_QUOTE':self.parseStringExpr})
        expr.append({'T_BOOLEAN':self.parseBooleanExpr})
        expr.append({'T_ID':self.parseId})

        productions['Statement'] = statements
        productions['Expr'] = expr
        return productions

    
    