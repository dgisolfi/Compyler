#!/usr/bin/python3
# 2019-1-22

class Token:
    def __init__(self, kind, value, line, pos):
        self.__kind = kind
        self.__value = value
        self.__line = line
        self.__position = pos

    def __repr__(self):
        return f'{self.__kind}'

    
    @property
    def kind(self):
        return self.__kind

    @property
    def value(self):
        return self.__value

    @property
    def line(self):
        return self.__line
    
    @property
    def position(self):
        return self.__position
    