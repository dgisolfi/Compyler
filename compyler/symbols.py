#!/usr/bin/python3
# 2019-4-09

from beautifultable import BeautifulTable

class SymbolTable:
    def __init__(self, scope, **kwargs):
        # HashMap -- Python dictionaries are hashmaps
        self.__table = {};
        self.__scope = scope
        self.__inner_block = kwargs.get('inner_block', None)
        self.pretty_table = BeautifulTable()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        # table.column_headers = ['value', 'type', 'scope', 'line']
        print(self.__table)
        return ''

    # @property
    # def table(self):
    #     return self.__table
        
    @property
    def scope(self):
        return self.__scope

    @property
    def symbol(self, key):
        return self.__table[key]
    
    @symbol.setter
    def add(self, key, value):
        self.__table[key] = value


    def append(self, var, type):
        self.__table[var] = type
