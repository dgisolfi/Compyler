#!/usr/bin/python3
# 2019-1-22

import re
from token import Token
from termcolor import colored

class Lexer:
    def __init__(self, code):
        self.code = code
        self.__tokens = []
        self.buffer = ''
        self.line = 1
        self.col = 0
        self.comment = False
        self.verbose = True
        self.lex()

    @property
    def tokens(self):
        return self.__tokens
    
    def match(self):
        pass
            
    def logToken(self, token):
        print(colored(f'LEXER ❯ {token.kind} [ {token.value} ] on line {token.line} at position {token.position}', 'cyan'))
    
    def lex(self):
        symbol_found = False
        for pos, char in enumerate(self.code):
            self.col += 1
            # next = self.code[pos+1]
    
            # Keep track of line and col numbers
            if re.match(r'[\n]', char):
                self.line += 1
                self.col = 0
                continue

            # Remove Spaces, They cant be trusted!
            if re.match(r' ', char):
                continue

            # Check Buffer
            else: 
                self.buffer += char
                # iterate through all token patterns and find all matches
                for lexeme in self.lexemes:
                    # print(self.lexemes.get(lexeme))
                    # print(self.lexemes[lexeme], self.buffer)
                    if re.match(self.lexemes[lexeme], self.buffer):
                        token = Token(lexeme, self.buffer, self.line, self.col)
                        self.__tokens.append(token)
                        self.logToken(token)
                        self.buffer = ''
                        break
    lexemes = {
        'L_BRACE': r'^{$',
        'R_BRACE': r'^}$',
        'L_PAREN': r'^\($',
        'R_PAREN': r'^\)$',
        'PRINT': r'^print$',
        'TYPE': r'^(int|string|boolean)$',
        'IF': r'^if$',
        'QUOTE': r'^"$',
        'ID': r'^[a-z]$',
        'CHAR': r'[a-z]',
        'DIGIT': r'^\d$',
        'WHILE':  r'^while$',
        'BOOLEAN': r'^(true|false)$',
        'EQUALITY_OP': r'^==$',
        'INEQUALITY_OP': r'^!=$',
        'ADDITION_OP': r'^\+$',
        'ASSIGN_OP': r'^=$',
        'EOP': r'^\$$'   
    }
    