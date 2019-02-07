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
        isComment = False
        isQuote = False
        buffer = ''

        while self.pos < len(self.code):
            char = self.code[self.pos]
            

    def dissectBuffer(self, buffer):
        temp_col = self.col - len(buffer)
        longest_match = ['','']

        # print(buffer)
        while len(buffer) > 0:
           
            for lexeme in lexemes:
                if re.match(lexemes[lexeme]['pattern'], buffer):
                    if len(buffer) > len(longest_match[1]):
                        longest_match[0] = lexeme
                        longest_match[1] = self.matchLexeme(lexeme, buffer)
                        
                    elif len(buffer) == len(longest_match[1]):
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