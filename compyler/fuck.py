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
        isComment = False
        isQuote = False
        buffer = ''

        while self.pos < len(self.code):
            char = self.code[self.pos]
            buffer = self.code[self.prev_pos:self.pos]
            if not re.match(r'[a-z0-9]', char):
                print(char, buffer)
                if len(buffer) > 0:
                    if self.dissectBuffer(''.join(buffer)) == 1:
                        self.error()
                if char is '':
                    # End of file
                    break
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
                    pass
                elif re.match(lexemes['ASSIGN_OP']['pattern'], char):
                    next = self.code[self.pos+1]
                    if re.match(lexemes['ASSIGN_OP']['pattern'], next):
                        token = Token('ASSIGN_OP', '==', self.line, self.col)
                        self.__tokens.append(token)
                        self.logToken(token)
                        self.pos += 1
                        self.col += 1
                elif isComment:
                    pass
                elif re.match(symbols, char):
                    for lexeme in lexemes:
                        if re.match(lexemes[lexeme]['pattern'], char):
                            token = Token(lexeme,char, self.line, self.col)
                            self.__tokens.append(token)
                            self.logToken(token)

                 # print(char, buffer)

                self.col += 1
                self.pos += 1
                self.prev_pos = self.pos
                # print(char)

            else:
                self.pos += 1


    
    def dissectBuffer(self, buffer):
        temp_col = self.col - len(buffer)
        longest_match = ['','']

        # print(buffer)
        while len(buffer) > 0:
           
            for lexeme in lexemes:
                if re.match(lexemes[lexeme]['pattern'], buffer):
                    # print(lexeme, buffer)
                    if len(buffer) > len(longest_match[1]):
                        print(lexeme, buffer)
                        longest_match[0] = lexeme
                        longest_match[1] = self.matchLexeme(lexeme, buffer)
                        
                        if lexemes[longest_match[0]]['priority'] > lexemes[lexeme]['priority']:
                            longest_match[0] = lexeme
                            longest_match[1] = self.matchLexeme(lexeme, buffer)

            token = Token(longest_match[0], longest_match[1], self.line, temp_col)
            self.__tokens.append(token)
            self.logToken(token)
            temp_col += len(longest_match[1])
            buffer = buffer[len(longest_match[1]):]
        return 0

    def matchLexeme(self, lexeme, buffer):
        match = ''
        if lexeme is 'DIGIT' or lexeme is 'ID':
            match = buffer[:0]
        elif lexeme is 'TYPE':
            if re.match(r'^int$', buffer):
                match = 'int'
            elif re.match(r'^string$', buffer):
                match = 'string'
            elif re.match(r'^boolean$', buffer):
                match = 'boolean'
        elif lexeme is 'BOOLEAN':
            if re.match(r'^true$', buffer):
                match = 'true'
            elif re.match(r'^false$', buffer):
                match = 'false'
        else:
            match = lexeme.lower()
        return match