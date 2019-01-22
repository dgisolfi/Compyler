#!/usr/bin/env python
# 2019-1-22

import os
import sys
from termcolor import colored
from ShellCommand import ShellCommand

class Shell:
    def __init__(self):
        self.ver = '0.0.1'
        self.command_list = []
        self.enabled = True
        self.prompt = '❯'
   

    def createCommandList(self):
        sc = ShellCommand(self.help,
            command='help',
            description='Prints a list of available commands and their description'
        )
        self.command_list.append(sc)

        sc = ShellCommand(self.exit,
            command='exit',
            description='Exits the Compiler Shell'
        )
        self.command_list.append(sc)

        sc = ShellCommand(self.compile,
            command='compile',
            description='Given a file path will compile the file and output the results'
        )
        self.command_list.append(sc)



    def handleInput(self):
        self.start()
        try:
            while self.enabled:
                cmd = input(f'{self.prompt} ')
                fn, args, cmd = self.parseInput(cmd)
                if fn == 'not_found':
                    print(f"Command Not Found, type {colored('help', 'blue')} for valid commands")
                else:
                    cmd = cmd.strip
                    self.execute(fn, args, cmd)
        except KeyboardInterrupt:
            self.exit()
            print('\Compiler CLI exited...Goodbye')

    def parseInput(self, user_input):
        # Trim leading and trailing white spaces
        user_input = user_input.strip() 
        # Break down users input by word
        words = user_input.split(' ')
        # All Commands are 1 word, the first word is the command
        user_commad = words[0]
        args = words
        del args[0] 
        name = ''
        found = False
        fn = None
        for cmd in self.command_list:
            if cmd.command == user_commad:
                found = True
                fn = cmd.fn
                name = cmd.command
        
        if found == False:
            return 'not_found', args, name
        else:
            return fn, args, name

    def execute(self, fn, args, cmd):
        try:
            if args == []:
                fn()
            else:
                fn(args)
        except:
            raise ValueError(f"{colored('Error:', 'red')} args list length: {len(args)} not appropriate for function:{cmd}")
        

    #####################
    # Command Functions #
    #####################
    def start(self):
        print('\n\t'+ f"{colored('Compiler', 'blue')} v{self.ver}")
        print(f"type {colored('help', 'blue')} for command list")

    def help(self):
        for cmd in self.command_list:
            print(f"{colored(cmd.command, 'blue')} - {cmd.description}")

    def exit(self):
        self.enabled = False

    def compile(self, file):
        file = file[0]
        # open the file and read the lines
        try:
            user_code = open(file)
            lines = user_code.read().splitlines()
        except IOError:
            print(
                f"{colored('Error:', 'red')} The file: {file} could not be opened " +
                'please ensure the path is correct or use and absolute path'
            )
        
        # Run Lex on the source code
        



if __name__ == "__main__":
    shell = Shell()
    shell.createCommandList()
    shell.handleInput()