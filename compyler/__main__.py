#!/usr/bin/python3
# 2019-1-22

ver='0.2.0'
package='compyler'

import re
import sys
import click
from termcolor import colored
from .error import Error
from .lexer import Lexer
from .parser import Parser


# Remove those pesky comments before even lexing
def removeComments(code):
    code = re.sub(r'\/\*[^\*]*\*\/', '', code)
    return code

# In case someone dares use tabs we will avoid errors
def replaceTabs(code):
    code = re.sub(r'\t', '   ', code)
    return code

@click.command()
@click.argument('path', type=click.Path())
@click.option(
    '--verbose', '-v', is_flag=True,
    help='Will provide details on the steps the compiler is taking.'
)
@click.option(
    '--prettytree', '-p', is_flag=True,
    help='Outputs CST and AST in a fancier form.'
)
def main(path, verbose, prettytree):
    # Overwrite the flag for verbose until alan is sick of seeing it
    verbose = True
    
    # Given the path of a Alan++ source file to be compiled, generated code will be returned
    # Gotta include the emoji just because Alan said not to
    print(colored(f'\n{package} v{ver} 🐍', 'blue'))

    source_code = getFile(path)

    # Remove all Comments and replace tab characters
    source_code = removeComments(source_code)
    source_code = replaceTabs(source_code)
    
    programs = source_code.split('$')

    try:
        program = 0
        # Check if this is the last program
        if programs[(len(programs)-1)] is '':
            programs[(len(programs)-2)] += '$'
            del programs[(len(programs)-1)]

        while program <= (len(programs)-1):
            code = programs[program]
            
            # Add the dollar sign back to the program
            if program is not (len(programs)-1):
                code += '$'
           
            # Begin Lexing(add one to the program count 
            # cuz it I dont want it to start at 0 But the array needs 
            # to be accessed at 0)
            lex = Lexer(code, verbose, program+1)
            if lex.errors is not 0:
                print(colored(f'Skipping Parse for Program {lex.program}. Lex Failed\n', 'blue'))
                program += 1
                continue

            tokens = lex.tokens
            # Parse the tokens
            parse = Parser(tokens,verbose, prettytree, program+1)
           
            if parse.errors is not 0:
                print(colored(f'Skipping CST Output for Program {parse.program}. Parse Failed\n', 'blue'))
                program += 1
                continue

            if verbose:
                print(parse.cst)
            
           
            program += 1
           
    
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