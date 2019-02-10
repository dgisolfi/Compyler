#!/usr/bin/python3
# 2019-1-22

import sys
import re
from error import Error
from tokens import Token
from lexemes import lexemes
from termcolor import colored

class Lexer:
    def __init__(self, code, verbose):
        self.code = code
        self.verbose = verbose
        self.__tokens = []
        self.line = 1
        self.col = 1
        self.pos = 0
        self.prev_pos = -1
        self.seperator_found = False
        self.lex()

    @property
    def tokens(self):
        return self.__tokens

    def logToken(self, token):
        # Only log tokens if the -v flag was passed.
        if self.verbose:
            print(colored(f'LEXER ❯ {token.kind} [ {token.value} ] on line {token.line} at position {token.position}', 'cyan'))

    def programExit(self, program_number):
        print(colored(f'LEXER ❯ Lexed Program: {program_number}', 'cyan'))

    def lex(self):
        symbols = r'\(|\)|\{|\}|\$|\+'
        isQuote = False
        buffer = ''
        longest_match = ['','']
        program = 0
        warnings

        while self.pos < len(self.code):
            char = self.code[self.pos]
            # print(f'Last:{self.prev_pos} Cur:{self.pos} Char:{char}')
            if not re.match(r'[a-z0-9]', char):
                if len(buffer) > 0:
                    buffer, longest_match = self.consumeBuffer(buffer, longest_match)
                self.seperator_found = True
                if char is '':
                    # End of file
                    pass
                elif re.match(' ', char):
                    pass
                elif re.match('\n', char):
                    self.line += 1
                    self.col = 0
                # COMMENTS
                # Check for Open Comment
                elif re.match(r'\/', char):
                    # check next char is *
                    next = self.code[self.pos+1]
                    if re.match(r'\*', next):
                        self.delComment()
                elif re.match(lexemes['EOP']['pattern'], char):
                    token = Token('EOP', char, self.line, self.col)
                    self.__tokens.append(token)
                    self.logToken(token)
                    program += 1
                    self.programExit(program)
                elif re.match(lexemes['QUOTE']['pattern'], char):
                    self.buildQuote()
                elif re.match(lexemes['ASSIGN_OP']['pattern'], char):
                    next = self.code[self.pos+1]
                    if re.match(lexemes['ASSIGN_OP']['pattern'], next):
                        token = Token('EQUALITY_OP', '==', self.line, self.col)
                        self.__tokens.append(token)
                        self.logToken(token)
                        self.pos += 1
                        self.col += 1
                    else:
                        token = Token('ASSIGN_OP', char, self.line, self.col)
                        self.__tokens.append(token)
                        self.logToken(token)

                elif re.match(r'^!$', char):
                    next = self.code[self.pos+1]
                    if re.match(lexemes['ASSIGN_OP']['pattern'], next):
                        token = Token('INEQUALITY_OP', '!=', self.line, self.col)
                        self.__tokens.append(token)
                        self.logToken(token)
                        self.pos += 1
                        self.col += 1
                
                elif re.match(symbols, char):
                    for lexeme in lexemes:
                        if re.match(lexemes[lexeme]['pattern'], char):
                            token = Token(lexeme,char, self.line, self.col)
                            self.__tokens.append(token)
                            self.logToken(token)
                
                else:
                    print(char)

                
                self.col += 1
                self.pos += 1
                self.prev_pos = self.pos
            else:
                buffer += char
                self.pos += 1
                self.col += 1

        print(colored(f'Lexical Analysis Completed', 'blue'))
            

    def consumeBuffer(self, buffer, longest_match):
        temp_col = self.col - len(buffer)
        longest_match = ['','']
        
        for lexeme in lexemes:
            if re.match(lexemes[lexeme]['pattern'], buffer):
                if len(buffer) > len(longest_match[1]):
                    longest_match[0] = lexeme
                    longest_match[1] = buffer
                elif len(buffer) == len(longest_match[1]):
                    # print(lexeme, longest_match[0])
                    if lexemes[longest_match[0]]['priority'] > lexemes[lexeme]['priority']:
                        longest_match[0] = lexeme
                        longest_match[1] = buffer

        if self.seperator_found:
            token = Token(longest_match[0], longest_match[1], self.line, temp_col)
            self.__tokens.append(token)
            self.logToken(token)
            temp_col += len(longest_match[1])
            # print('BUFFER1', buffer)
            buffer = buffer[len(longest_match[1]):]
            # print('BUFFER2', buffer)

        return buffer, longest_match

    def delComment(self):
        end_found = False
        while not end_found:
            if re.match(r'\*', self.code[self.pos]):
                if re.match(r'\/', self.code[self.pos+1]):
                    self.pos += 1
                    self.col += 1
                    end_found = True
                    break
            self.pos += 1
            self.col += 1

    def buildQuote(self):
        end_found = False

        token = Token('QUOTE', self.code[self.pos], self.line, self.col)
        self.__tokens.append(token)
        self.logToken(token)
        self.pos += 1
        self.col += 1

        while not end_found:
            char = self.code[self.pos]
            
            
            if re.match(r'\"', char):
                token = Token('QUOTE', char, self.line, self.col)
                self.__tokens.append(token)
                self.logToken(token)
                end_found = True
            else:
                # Check foor invalid types!
                if not re.match(r'^[a-z]$', char):
                    Error('Lexer', f'Character list contains invalid character: "{char}". It can only contain lowercase letters and spaces.', 
                    self.line, self.col)
                token = Token('CHAR', char, self.line, self.col)
                self.__tokens.append(token)
                self.logToken(token)

                self.pos += 1
                self.col += 1