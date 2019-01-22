#!/usr/bin/env python
# 2019-1-22

class ShellCommand:
    def __init__(self, *args, **kwargs):
        self.fn = args[0]
        self.command = kwargs.pop('command', '')
        self.description = kwargs.pop('description', '')
        
        err, msg = self.checkNewCommand()
        if err == 1:
            raise ValueError(msg)

    def checkNewCommand(self):
        if self.command == '':
            self.__del__()
            return 1, 'Command Not Provided'
        elif self.description == '':
            self.__del__()
            return 1, 'Command Description Not Provided'
        else:
            return 0, 'Command Creation Approved'

    def __str__(self):
        return str(self.fn)

    def __repr__(self):
        return self.__str__()

    def __del__(self):
        return f'Deleted Shell Command: {self.command}'