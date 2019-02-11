#!/usr/bin/python3
# 2019-1-22

import sys
import re
from error import Error
from tokens import Token
from lexemes import lexemes
from termcolor import colored

class Lex:
    def __init__(self, code, verbose, program):
        self.code = code
        self.verbose = verbose
        self.program = program
        self.tokens = []
        self.line = 1
        self.col = 1
        self.pos = 0
        self.prev_pos = -1
        self.seperator_found = False
        self.warnings = 0
        self.errors = 0
        self.lex()

    def logToken(self, token):
        # Only log tokens if the -v flag was passed.
        if self.verbose:
            print(colored(f'LEXER ❯ {token.kind} [ {token.value} ] on line {token.line} column {token.position}', 'cyan'))
    def exit(self):
        print(colored(f'Program {self.program} Lexed. Errors: {self.errors} Warnings: {self.warnings}', 'blue'))

    def lex(self):
        symbols = r'\(|\)|\{|\}|\$|\+'
        isQuote = False
        buffer = ''
        longest_match = ['','']

        while self.pos < len(self.code):
            char = self.code[self.pos]
            # print(f'Last:{self.prev_pos} Cur:{self.pos} Char:{char}')
            if not re.match(r'[a-z0-9]', char):
                self.seperator_found = True
                if len(buffer) > 0:
                    buffer, longest_match = self.consumeBuffer(buffer, longest_match)
                # if char is '':
                #     # End of file
                #     pass
                if re.match(r'^\s$', char):
                    pass
                elif re.match('\n', char):
                    self.line += 1
                    self.col = 0
                elif re.match(lexemes['EOP']['pattern'], char):
                    token = Token('EOP', char, self.line, self.col)
                    self.tokens.append(token)
                    self.logToken(token)
                elif re.match(lexemes['QUOTE']['pattern'], char):
                    self.buildQuote()
                elif re.match(lexemes['ASSIGN_OP']['pattern'], char):
                    next = self.code[self.pos+1]
                    if re.match(lexemes['ASSIGN_OP']['pattern'], next):
                        token = Token('EQUALITY_OP', '==', self.line, self.col)
                        self.tokens.append(token)
                        self.logToken(token)
                        self.pos += 1
                        self.col += 1
                    else:
                        token = Token('ASSIGN_OP', char, self.line, self.col)
                        self.tokens.append(token)
                        self.logToken(token)

                elif re.match(r'^!$', char):
                    next = self.code[self.pos+1]
                    if re.match(lexemes['ASSIGN_OP']['pattern'], next):
                        token = Token('INEQUALITY_OP', '!=', self.line, self.col)
                        self.tokens.append(token)
                        self.logToken(token)
                        self.pos += 1
                        self.col += 1
                
                elif re.match(symbols, char):
                    for lexeme in lexemes:
                        if re.match(lexemes[lexeme]['pattern'], char):
                            token = Token(lexeme,char, self.line, self.col)
                            self.tokens.append(token)
                            self.logToken(token)
                
                else:
                    self.errors += 1
                    Error('Lexer', f'Character: [ {repr(char)} ] is not valid in this grammer.', self.line, self.col)
                    self.exit()
                
                self.col += 1
                self.pos += 1
                self.prev_pos = self.pos
            else:
                buffer += char
                self.pos += 1
                self.col += 1
        
        self.exit()
            

    def consumeBuffer(self, buffer, longest_match):
        temp_col = self.col - len(buffer)
        longest_match = ['','']
        
        for lexeme in lexemes:
            # print(lexemes[lexeme]['pattern'], buffer)
            if re.match(lexemes[lexeme]['pattern'], buffer):
                print(buffer, lexeme)
                if len(buffer) > len(longest_match[1]):
                    longest_match[0] = lexeme
                    longest_match[1] = buffer
                elif len(buffer) == len(longest_match[1]):
                    if lexemes[longest_match[0]]['priority'] > lexemes[lexeme]['priority']:
                        longest_match[0] = lexeme
                        longest_match[1] = buffer

        if self.seperator_found:
            token = Token(longest_match[0], longest_match[1], self.line, temp_col)
            self.tokens.append(token)
            self.logToken(token)
            temp_col += len(longest_match[1])
            buffer = buffer[len(longest_match[1]):]
            self.seperator_found = False

        return buffer, longest_match

    def buildQuote(self):
        end_found = False
        token = Token('QUOTE', self.code[self.pos], self.line, self.col)
        self.tokens.append(token)
        self.logToken(token)
        self.pos += 1
        self.col += 1

        while not end_found:
            char = self.code[self.pos]
            
            
            if re.match(r'\"', char):
                token = Token('QUOTE', char, self.line, self.col)
                self.tokens.append(token)
                self.logToken(token)
                end_found = True
            else:
                # Check foor invalid types!
                if not re.match(r'^[a-z\s]$', char):
                    self.errors += 1
                    Error('Lexer', f'Character list contains invalid character: "{char}". It can only contain lowercase letters and spaces.', 
                    self.line, self.col)
                    self.exit()
                token = Token('CHAR', char, self.line, self.col)
                self.tokens.append(token)
                self.logToken(token)

                self.pos += 1
                self.col += 1