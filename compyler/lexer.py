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
        self.line = 0
        self.col = 0
        self.verbose = True
        self.lex()

    @property
    def tokens(self):
        return self.__tokens

    def lex(self):
        comment = False
        for pos, char in enumerate(self.code):
            self.col += 1
            if re.match(r' ', char):
                continue
                
            if re.match(r'[\n]', char):
                self.line += 1
                self.col = 0
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

            # LEFT BRACE
            elif re.match(r'^{$', char):
                token = Token('T_OPENING_BRACE', '{', self.line, self.col)
                self.__tokens.append(token)
                self.logToken(token)
                continue

            # RIGHT BRACE
            elif re.match(r'^}$', char):
                token = Token('T_CLOSING_BRACE', '}', self.line, self.col)
                self.__tokens.append(token)
                self.logToken(token)
                continue

            # PRINT
            if re.match(r'print\b', self.buffer):
                token = Token('T_PRINT', 'print', self.line, self.col-5)
                self.__tokens.append(token)
                self.logToken(token)
                self.buffer = ''
                
                

            # WHILE

            # TYPE

            # IF

            # BOOL

            # LEFT PAREN
            elif re.match(r'^\($', char):
                token = Token('T_OPENING_PARENTHESIS', '(', self.line, self.col)
                self.__tokens.append(token)
                self.logToken(token)
                continue

            # RIGHT PAREN
            elif re.match(r'^\)$', char):
                token = Token('T_CLOSING_PARENTHESIS', ')', self.line, self.col)
                self.__tokens.append(token)
                self.logToken(token)
                continue

            # ASSIGNMENT

            # ADDITION

            # IDENTIFIERS

            # DIGITS

            # QUOTES

            # STRINGS

            # EQUALITY

            # INEQAULITY

            # EOP
            # elif re.match(r'^\$$', char):
            #     continue
                

           
            # This hasnt formed a token yet, add to the buffer
            self.buffer += char
            

            print(self.buffer)
        # print(self.tokens)
           
            
    def logToken(self, token):
        print(colored(f'LEXER ❯ {token.kind} [ {token.value} ] on line {token.line} at position {token.position}', 'cyan'))
    