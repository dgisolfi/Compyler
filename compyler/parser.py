#!/usr/bin/python3
# 2019-2-12

# from tree import Tree

class Parser:
    def __init__(self, tokens):
       self.__tokens = tokens
       self.cst = None

    
    ''' All productions to preform "derivations" '''
    def parseProgram(self):
        pass

    def parseBlock(self):
        pass

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

    
    
    

       
       

    
