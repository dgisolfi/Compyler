#!/usr/bin/python3
# 2019-4-09

from beautifultable import BeautifulTable

class SymbolTable:
    def __init__(self, scope, **kwargs):
        # HashMap -- Python dictionaries are hashmaps
        self.__table = {};
        self.__scope = scope
        self.__inner_blocks = []
        if kwargs.get('inner_block', None) is not None:
            self.__inner_blocks.append(kwargs.get('inner_block'))
        self.pretty_table = BeautifulTable()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        # table.column_headers = ['value', 'type', 'scope', 'line']
        print(self.__table)
        return ''

    @property
    def children(self):
        return self.__inner_blocks
        
    @property
    def scope(self):
        return self.__scope


    def get(self, key):
        return self.__table.get(key)
    
    # @symbol.setter
    def add(self, key, value):
        print(f'TABLE: {key}, {value}')
        self.__table[key] = value
