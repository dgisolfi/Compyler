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
        self.pos = 0
        self.lex()


    @property
    def tokens(self):
        return self.__tokens
    
    def match(self):
        pass
            
    def logToken(self, token):
        print(colored(f'LEXER ❯ {token.kind} [ {token.value} ] on line {token.line} at position {token.position}', 'cyan'))
    
    # def splitPrograms(self):
        
    def nextChar(self):
        self.pos += 1
        self.col += 1

    def lex(self):
        comment = False
        seperator_found = False
        # arr[0] is the lexeme and arr[1] is the val 
        longest_match = ['', '']
        seperators = ['"', '(', ')', '{', '}', '=', '==', '!=', '+']
        striped_code = self.code.replace(' ', '')
        print(striped_code)
        spaces = 0
        lines = self.code.split('\n')
        while self.pos < len(self.code):
            line = lines[self.line]
            char = line[self.col]

            # # Keep track of line and col numbers
            # if re.match(r'[\n]', char):
            #     self.line += 1
            #     self.col = 0
            #     self.nextChar()
            #     continue

            # Remove Spaces, They cant be trusted!
            if re.match(r' ', char):
                self.nextChar()
                spaces += 1
                continue

            else: 
                # This char is or is part of a token, compare it to the lexemes
                self.buffer.append(char)

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
                print(self.buffer)
                if char in seperators:
                    token = Token(longest_match[0], longest_match[1], self.line, self.col)
                    self.__tokens.append(token)
                    self.logToken(token)
                    length = len(longest_match[1])
                    self.buffer = self.buffer[length:]
                    longest_match[0] = ''
                    longest_match[1] = ''
                    seperator_found = False
                   
                   
                    if len(self.buffer) > 1:
                        self.pos -= (len(self.buffer))
                        print(self.buffer, self.pos, 'New POS:') #striped_code[self.pos])
                        self.buffer = []
                        spaces = 0
                        self.nextChar()
                        continue

               


                # print(char, self.col, self.pos)
                self.nextChar()
  
            