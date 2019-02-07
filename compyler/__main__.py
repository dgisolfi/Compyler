#!/usr/bin/python3
# 2019-1-22

ver='0.0.1'
package='compyler'

import sys
from termcolor import colored
from error import Error
from lexer import Lexer

def main():

    del sys.argv[0]
    # check for required file arg
    if len(sys.argv) < 1:
        Error('main', 'No source file Provided, please provide a path to the file to be compiled.') 

    file = sys.argv[0]

    print(colored(f'\n{package} v{ver}', 'blue'))
    
    # Attempt to open the file for compilation
    source_code = getFile(file)

    try:
        # Begin Lexing
        print(colored('Beginning Lexical Analysis', 'blue'))
        lex = Lexer(source_code)
        # tokens = lex.tokens()
    
    except KeyboardInterrupt:
        print(colored('KeyboardInterrupt', 'red'))
   



def getFile(file):
    # open the file and read the lines
    try:
        user_code = open(file)
        lines = user_code.read()
        return lines
    except IOError:
        Error('main', f'File: {file} could not be opened please ensure the path is correct or use and absolute path')


if __name__ == "__main__":
    main()