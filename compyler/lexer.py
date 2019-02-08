#!/usr/bin/python3
# 2019-1-22

import sys
import re
from token import Token
from lexemes import lexemes
from termcolor import colored

class Lexer:
    def __init__(self, code):
        self.code = code
        self.__tokens = []
        self.line = 1
        self.col = 0
        self.pos = 0
        self.prev_pos = 0
        self.seperator_found = False
        self.lex()

    @property
    def tokens(self):
        return self.__tokens

    def logToken(self, token):
        print(colored(f'LEXER ❯ {token.kind} [ {token.value} ] on line {token.line} at position {token.position}', 'cyan'))

    def error(self):
        sys.exit(1)
        pass

    def lex(self):
        symbols = r'\(|\)|\{|\}|\$|\+'
        isQuote = False
        buffer = ''
        longest_match = ['','']

        while self.pos < len(self.code):
            char = self.code[self.pos]

            if not re.match(r'[a-z0-9]', char):
                if len(buffer) > 0:
                    buffer, longest_match = self.dissectBuffer(buffer, longest_match)
                self.seperator_found = True
                if char is '':
                    # End of file
                    # self.error() n 
                    pass
                elif re.match(' ', char):
                    pass
                elif re.match('\n', char):
                    self.line += 1
                    self.col = 0
                elif re.match(lexemes['EOP']['pattern'], char):
                    token = Token('EOP', char, self.line, self.col)
                    self.__tokens.append(token)
                    self.logToken(token)
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
                    

                # COMMENTS
                # Check for Open Comment
                elif re.match(r'\/', char):
                    # check next char is *
                    next = self.code[self.pos+1]
                    if re.match(r'\*', next):
                        self.delComment()

                elif re.match(symbols, char):
                    for lexeme in lexemes:
                        if re.match(lexemes[lexeme]['pattern'], char):
                            token = Token(lexeme,char, self.line, self.col)
                            self.__tokens.append(token)
                            self.logToken(token)

                
                self.col += 1
                self.pos += 1
                self.prev_pos = self.pos
            else:
                buffer += char
                self.pos += 1
            

    def dissectBuffer(self, buffer, longest_match):
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
                    # self.col += 2
                    end_found = True
                    break
            self.pos += 1

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
                token = Token('CHAR', char, self.line, self.col)
                self.__tokens.append(token)
                self.logToken(token)

                self.pos += 1
                self.col += 1