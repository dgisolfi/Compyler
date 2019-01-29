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
        for char in self.code:
            self.pos += 1

            # Check for new line
            if re.match('\n', char):
                self.line += 1
            if re.match('\s', char):
                continue

            # Check for comment Start
            if re.match('/\\*$', self.buffer):
                self.buffer = ''
                comment = True
            if comment:
                if re.match('\*', char) or re.match('\\/', char):
                    print(char, self.buffer)
                    self.buffer += char
   
                if re.match('\\*/$', self.buffer):
                    comment = False
                    print('Done')
                    
            # print(self.line, self.pos,char, self.buffer)
            # This hasnt formed a token yet, add to the buffer
            self.buffer += char
    