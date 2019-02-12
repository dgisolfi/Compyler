#!/usr/bin/python3
# 2019-1-22

ver='0.1.0'
package='compyler'

import sys
import click
from termcolor import colored
from compyler.error import Error
from compyler.lexer import Lexer

@click.command()
@click.argument('path')
@click.option(
    '--verbose', '-v', is_flag=True,
    help='Will provide details on the steps the compiler is taking.'
)

def main(path, verbose):
    # Given the path of a Alan++ source file to be compiled, generated code will be returned
    # Gotta include the emoji just because Alan said not to
    print(colored(f'\n{package} v{ver} 🐍', 'blue'))
    
    source_code = getFile(path)

    try:
        # Begin Lexing
        lex = Lexer(source_code, verbose)
        tokens = lex.tokens
    
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