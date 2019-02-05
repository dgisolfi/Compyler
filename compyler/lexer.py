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
        self.buffer = []
        self.programs = []
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
    
    # def splitPrograms(self):
        


    def lex(self):
        comment = False
        seperator_found = False
        # arr[0] is the lexeme and arr[1] is the val 
        longest_match = ['', '']
        seperators = ['"', '"', '(', ')', '{', '}', '=', '==', '!=', '+']
        pos = 0
        self.code = self.code.replace(' ', '')
        while pos < len(self.code):
            
            char = self.code[pos]
            # print(char)
            self.col += 1
            # Keep track of line and col numbers
            if re.match(r'[\n]', char):
                self.line += 1
                self.col = 0
                pos += 1
                continue
                
            # # Remove Spaces, They cant be trusted!
            # elif re.match(r' ', char):
            #     pos += 1
            #     continue

            else:
                self.buffer.append(char)

                if char in seperators:
                    seperator_found = True
                   
                # iterate through all token patterns and find all matches
                for lexeme in lexemes:
                    if re.match(lexemes[lexeme]['pattern'], ''.join(self.buffer)):
                        if len(self.buffer) > len(longest_match[1]):
                            longest_match[0] = lexeme
                            longest_match[1] = ''.join(self.buffer)
                        elif len(self.buffer) == len(longest_match[1]):
                            # print(lexeme, longest_match[0])
                            if lexemes[longest_match[0]]['priority'] > lexemes[lexeme]['priority']:
                                longest_match[0] = lexeme
                                longest_match[1] = ''.join(self.buffer)

                # if isValid is False:
                #     print('ERROR')
                #     break

                if seperator_found:
                    token = Token(longest_match[0], longest_match[1], self.line, self.col)
                    self.__tokens.append(token)
                    self.logToken(token)

                    # print(self.buffer, pos)
                    
                    length = len(longest_match[1])
                    self.buffer = self.buffer[length:]
                    longest_match[0] = ''
                    longest_match[1] = ''
                    seperator_found = False
                    if len(self.buffer) > 1:
                        pos -= len(self.buffer)
                        # print(self.code[pos])
                        self.buffer = []
                        continue
                
                # print(self.buffer, longest_match[1])
                pos += 1
            