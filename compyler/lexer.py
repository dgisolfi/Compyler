#!/usr/bin/python3
# 2019-1-22

import sys
import re
from error import Error
from warning import Warning
from tokens import Token
from lexemes import lexemes, buffer_lexemes
from termcolor import colored

class Lexer:
    def __init__(self, code, verbose):
        self.code = code
        self.verbose = verbose
        self.__tokens = []
        self.code = code
        self.verbose = verbose
        self.program_count = 1
        self.line = 1
        self.col = 1
        self.cur_pos = 0
        self.prev_pos = 0
        self.errors = 0
        self.lex()
       
    @property
    def tokens(self):
        return self.__tokens

    def removeComments(self, code):
        code = re.sub(r'\/\*[^\*]*\*\/', '', code)
        return code

    def replaceTabs(self, code):
        code = re.sub(r'\t', '   ', code)
        return code
    
    def checkEOP(self, code):
        if not re.match(r'\$', code[-1]):
            Warning('Lexer', f'EOP not found at end of program, inserting EOP', self.line, self.col)
            code += '$'
            
        return code
            
    def programExit(self):
        if self.errors > 0:
            print(colored(f'Lex Failed for Program {self.program_count}. Errors: {self.errors}', 'red'))
        else:
            print(colored(f'Lex Completed for Program {self.program_count}. Errors: {self.errors}', 'blue'))
        self.warnings = 0
        self.errors = 0
        self.program_count += 1
        
    def logToken(self, token):
        # Only log tokens if the -v flag was passed.
        if self.verbose:
            print(colored(f'LEXER ❯ {token.kind} [ {token.value} ] on line {token.line} column {token.position}', 'cyan'))

    def lex(self):
        # Remove all Comments and replace tab characters
        self.code = self.removeComments(self.code)
        self.code = self.replaceTabs(self.code)

        # Check for EOP at end of file
        self.code = self.checkEOP(self.code)

        symbols = r'\(|\)|\{|\}|\$|\+'
        buffer = ''

        while self.cur_pos < len(self.code):
            char = self.code[self.cur_pos]
            buffer = self.code[self.prev_pos:self.cur_pos]

            if not re.match(r'[a-z0-9]', char):
                if len(buffer) > 0:
                   self.consumeBuffer(buffer)
                if re.match(' ', char):
                    pass
                elif re.match('\n', char):
                    self.line += 1
                    self.col = 0
                elif re.match(lexemes['EOP']['pattern'], char):
                    token = Token('EOP', char, self.line, self.col)
                    self.__tokens.append(token)
                    self.logToken(token)
                    self.programExit()
                elif re.match(lexemes['QUOTE']['pattern'], char):
                    self.buildQuote()
                elif re.match(lexemes['ASSIGN_OP']['pattern'], char):
                    next = self.code[self.cur_pos+1]
                    if re.match(lexemes['ASSIGN_OP']['pattern'], next):
                        token = Token('EQUALITY_OP', '==', self.line, self.col)
                        self.__tokens.append(token)
                        self.logToken(token)
                        self.cur_pos += 1
                        self.col += 1
                    else:
                        token = Token('ASSIGN_OP', char, self.line, self.col)
                        self.__tokens.append(token)
                        self.logToken(token)

                elif re.match(r'^!$', char):
                    next = self.code[self.cur_pos+1]
                    if re.match(lexemes['ASSIGN_OP']['pattern'], next):
                        token = Token('INEQUALITY_OP', '!=', self.line, self.col)
                        self.__tokens.append(token)
                        self.logToken(token)
                        self.cur_pos += 1
                        self.col += 1
                
                elif re.match(symbols, char):
                    for lexeme in lexemes:
                        if re.match(lexemes[lexeme]['pattern'], char):
                            token = Token(lexeme,char, self.line, self.col)
                            self.__tokens.append(token)
                            self.logToken(token)
                
                else:
                    self.errors += 1
                    Error('Lexer', f'Character: [ {repr(char)} ] is not valid in this grammer.', self.line, self.col)
                
                
                self.cur_pos += 1
                self.col += 1
                self.prev_pos = self.cur_pos
            else:
                self.cur_pos += 1
                self.col += 1

        print(colored(f'Lexical Analysis Completed', 'blue'))
        return self.__tokens
            

    def consumeBuffer(self, buffer):
        identifier = ''
        value = ''
        # Keep track of our location within the buffer whilst consuming
        temp_col = self.col - len(buffer)

        # Consume the buffer till its empty
        while len(buffer) > 0:
            # Loop through known lexemes and determine longest 
            for lexeme in buffer_lexemes:
                if re.match(buffer_lexemes[lexeme]['pattern'], buffer):
                    identifier = buffer_lexemes[lexeme]['token']
                    if identifier is 'DIGIT' or identifier is 'ID':
                        value = buffer[0]
                    else: 
                        value = buffer_lexemes[lexeme]['value']
                
            # Create a token based off the longest match found
            token = Token(identifier, value, self.line, temp_col);
            # log it and make it all pretty and stuff
            self.logToken(token)
            self.__tokens.append(token);
            # Adjust the buffer once the token was found/created
            buffer = buffer[len(value):]
            temp_col += len(value)

    def buildQuote(self):
        end_found = False
        token = Token('QUOTE', self.code[self.cur_pos], self.line, self.col)
        self.__tokens.append(token)
        self.logToken(token)
        self.cur_pos += 1
        self.col += 1

        while not end_found:
            char = self.code[self.cur_pos]
            if re.match(r'\"', char):
                token = Token('QUOTE', char, self.line, self.col)
                self.__tokens.append(token)
                self.logToken(token)
                end_found = True
            else:
                # Check foor invalid types!
                if not re.match(r'^[a-z\s]$', char):
                    self.errors += 1
                    Error('Lexer', f'Character list contains invalid character: "{char}". It can only contain lowercase letters and spaces.', 
                    self.line, self.col)
                token = Token('CHAR', char, self.line, self.col)
                self.__tokens.append(token)
                self.logToken(token)

                self.cur_pos += 1
                self.col += 1
    