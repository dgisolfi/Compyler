#!/usr/bin/python3
# 2019-1-22

import re
from lexemes import lexemes
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
        comment = False
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
            
            # COMMENTS
            # Check for Open Comment
            elif re.match('\/\*', self.buffer):
                comment = True
                self.buffer = ''
                continue
            # Once a comment has been opened skip the 
            # input until it has been ended
            elif comment:
                # If the '*' or '/' char are noticed add them to the buffer
                if re.match(r'\*', char):
                    if re.match(r'\/', self.code[pos+1]):
                        self.buffer += char
                elif re.match(r'\/', char):
                     if re.match(r'\*', self.code[pos-1]):
                        self.buffer += char

                # Check the buffer for the closing comment symbol
                if re.match(r'\*\/', self.buffer):
                    # if it was found were out of the comment, clear our buffer 
                    # and go back to normal tokenizing
                    comment = False
                    self.buffer = ''
                continue

            # Check Buffer
            else: 
                self.buffer += char
                # iterate through all token patterns and find all matches
                for lexeme in lexemes:
                    # print(lexemes.get(lexeme))
                    # print(lexemes[lexeme], self.buffer)
                    if re.match(lexemes[lexeme], self.buffer):
                        token = Token(lexeme, self.buffer, self.line, self.col)
                        self.__tokens.append(token)
                        self.logToken(token)
                        self.buffer = ''
                        break