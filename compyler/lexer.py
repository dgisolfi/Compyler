#!/usr/bin/python3
# 2019-1-22

import re

class Lexer:
    def __init__(self, code):
        self.code = code
        self.__tokens = []
        self.buffer = ''
        self.line = 0
        self.pos = 0
        self.lex()

    @property
    def tokens(self):
        return self.__tokens

    def lex(self):
        comment = False
        while self.pos < len(self.code):
            char = self.code[self.pos]

            # if re.match(r'[\s]', char):
            #     self.pos += 1
            #     continue

            
            # COMMENTS
            # Check for Open Comment
            if re.match('\/\*', self.buffer):
                comment = True
                self.buffer = ''
            # Once a comment has been opened skip the 
            # input until it has been ended
            if comment:
                # Check the buffer for the closing comment symbol
                if re.match(r'\*\/', self.buffer):
                    # if it was found were out of the comment, clear our buffer 
                    # and go back to normal tokenizing
                    comment = False
                    self.buffer = ''
                # If the '*' or '/' char are noticed add them to the buffer
                elif re.match(r'\*', char):
                    if re.match(r'\/', self.code[self.pos+1]):
                        self.buffer += char
                if re.match(r'\/', char):
                     if re.match(r'\*', self.code[self.pos-1]):
                        self.buffer += char
                   
                self.pos += 1
                continue

            
            # PRINT

            # WHILE

            # TYPE

            # IF

            # BOOL

            # LEFT PAREN

            # RIGHT PAREN

            # LEFT BRACE

            # RIGHT BRACE

            # ASSIGNMENT

            # ADDITION

            # IDENTIFIERS

            # DIGITS

            # QUOTES

            # STRINGS

            # EQUALITY

            # INEQAULITY

            # EOP
                

           
            # This hasnt formed a token yet, add to the buffer
            self.buffer += char

            # update the current position on the line and col
            self.pos += 1
            if re.match(r'[\n]', char):
                self.line += 1

        print(self.buffer)
           
            
            
    