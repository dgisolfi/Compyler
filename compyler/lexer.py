#!/usr/bin/python3
# 2019-1-22

import re
from token import Token
from lexemes import lexemes
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
        longest_match = ['', '']
        symbols = ['(', ')', '{', '}', '=', '==', '!=', '+']
        for pos, char in enumerate(self.code):
            self.col += 1
            if pos+1 >= len(self.code):
                next_char = ' '
            else:
                next_char = self.code[pos+1]
    
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
                if char in symbols:
                    print('symbol: ' + char)
                    symbol_found = True
                # iterate through all token patterns and find all matches
                # arr[0] is the lexeme and arr[1] is the val 
                for lexeme in lexemes:
                    # print(lexemes.get(lexeme))
                    # print(lexemes[lexeme], self.buffer)
                  
                    if re.match(lexemes[lexeme]['pattern'], self.buffer):
                        print(lexeme, self.buffer)
                        if len(self.buffer) > len(longest_match[1]):
                            longest_match[0] = lexeme
                            longest_match[1] = self.buffer
                        elif len(self.buffer) == len(longest_match[1]):
                            if lexemes[longest_match[0]]['priority'] < lexemes[lexeme]['priority']:
                                longest_match[0] = lexeme
                                longest_match[1] = self.buffer

                    # print(longest_match)

                if symbol_found:
                # if longest_match is not ['', '']:
                    token = Token(longest_match[0], longest_match[1], self.line, self.col)
                    self.__tokens.append(token)
                    self.logToken(token)
                    self.buffer = ''
                    longest_match[0] = ''
                    longest_match[1] = ''
                    symbol_found = False
    
                # else:
                #     print('error')