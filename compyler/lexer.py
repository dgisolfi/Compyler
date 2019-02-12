#!/usr/bin/python3
# 2019-1-22

import sys
import re
from error import Error
from lex import Lex
from termcolor import colored

class Lexer:
    def __init__(self, code, verbose):
        self.code = code
        self.verbose = verbose
        self.__tokens = []
        self.programs = self.code.split('$')
        self.main()
       
    @property
    def tokens(self):
        return self.__tokens

    def main(self):
        program = 0
        while len(self.programs) > 0:
            program += 1
            code = self.programs.pop(0)
            if code is not '':
                code = self.removeComments(code)
                code = self.replaceTabs(code)
                program_tokens = Lex(code, self.verbose, program)
                self.__tokens.append(program_tokens)
        print(colored(f'Lexical Analysis Completed', 'blue'))

    def removeComments(self, code):
        code = re.sub(r'\/\*[^\*]*\*\/', '', code)
        return code

    def replaceTabs(self, code):
        code = re.sub(r'\t', '   ', code)
        return code


    def checkForEOP(self):
        if self.code.find('$') != len(self.programs):
            print('MISSING EOP')

    def programExit(self, program_number):
        print(colored(f'LEXER ❯ Lexed Program: {program_number}', 'cyan'))