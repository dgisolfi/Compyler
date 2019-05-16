#!/usr/bin/python3
# 2019-1-22
# Daniel Nicolas Gisolfi

ver='0.4.0'
package='compyler'

import re
import sys
import click
from termcolor import colored
from error import Error
from lexer import Lexer
from parser import Parser
from semantics import SemanticAnalyser
from codegen import CodeGenerator


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
@click.option(
    '--optimize', '-o', is_flag=True,
    help='Implements optimizations for source code.'
)
def main(path, verbose, prettytree, optimize):
    
    # Given the path of a Alan++ source file to be compiled, generated code will be returned
    # Gotta include the emoji just because Alan said not to
    print(colored(f'\n{package} v{ver} 🐍', 'blue', attrs=['bold']))

    source_code = getFile(path)

    # Remove all Comments and replace tab characters
    source_code = removeComments(source_code)
    source_code = replaceTabs(source_code)
    
    programs = source_code.split('}$')

    try:
        program = 0
        errors = 0
        warnings = 0
        # Check if this is the last program
        if programs[(len(programs)-1)] is '':
            programs[(len(programs)-2)] += '}$'
            del programs[(len(programs)-1)]

        while program <= (len(programs)-1):
            code = programs[program]
            
            # Add the dollar sign back to the program
            if program is not (len(programs)-1):
                code += '}$'
           
            # Begin Lexing(add one to the program count 
            # cuz it I dont want it to start at 0 But the array needs 
            # to be accessed at 0)
            lex = Lexer(code, verbose, program+1)
            if lex.errors is not 0:
                print(colored(f'Skipping Parse for Program {lex.program}. Lex Failed\n', 'cyan', attrs=['bold']))
                program += 1
                continue

            tokens = lex.tokens
            errors += lex.errors
            warnings += lex.warnings

            # Parse the tokens
            parse = Parser(tokens,verbose, prettytree, program+1)
           
            if parse.errors is not 0:
                print(colored(f'Skipping CST Output for Program {parse.program}. Parse Failed\n', 'magenta', attrs=['bold']))
                program += 1
                continue

            if verbose:
                print(colored(f'CST for Program {parse.program}.\n', 'magenta', attrs=['bold']))
                print(parse.cst)
            
            errors += parse.errors
            warnings += parse.warnings
            semanticAnalyser = SemanticAnalyser(verbose, prettytree, program+1, parse.cst)
           
            if semanticAnalyser.errors is not 0:
                print(colored(f'Skipping AST and Symbol Table Output for Program {semanticAnalyser.program}. Semantic Analysis Failed\n', 'white', attrs=['bold']))
                program += 1
                continue

            if verbose:
                print(colored(f'\nAST for Program {program+1}.', 'green', attrs=['bold']))
                print(semanticAnalyser.ast)
                print(colored(f'Symbol Table for Program {program+1}.', 'green', attrs=['bold']))
                print(semanticAnalyser.symbol_table)
            
            errors += semanticAnalyser.errors
            warnings += semanticAnalyser.warnings

            codeGenerator = CodeGenerator(verbose, program+1, semanticAnalyser.ast,semanticAnalyser.symbol_table)

            if codeGenerator.errors is not 0:
                print(colored(f'Skipping Machine Code output for Program {codeGenerator.program}. Code Generatoration Failed\n', 'white', attrs=['bold']))
                program += 1
                continue

            print(colored(f'Machine Code for Program {program+1}.', 'blue', attrs=['bold']))
            print(codeGenerator)
            
            errors += codeGenerator.errors
            warnings += codeGenerator.warnings

            print(colored(f'Program {program+1} compiled with {errors} errors and {warnings} warnings.', 'white', attrs=['bold']))
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