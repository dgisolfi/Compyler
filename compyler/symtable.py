#!/usr/bin/python3
# 2019-4-09

from beautifultable import BeautifulTable

class SymbolTable:
    def __init__(self, parent, scope):
        # HashMap -- Python dictionaries are hashmaps
        self.__table = {};
        self.__parent = parent
        self.__children = []
        self.__scope = scope
        self.pretty_table = BeautifulTable()
        self.count = 0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        self.pretty_table.column_headers = ['Symbol', 'Type', 'Scope', 'Line']
        self.__printTable(self)
        print(self.pretty_table)
        return ''

    def __printTable(self, symbol_table):
        self.__buildTable(symbol_table)

        for child in symbol_table.children:
            if len(child.children) is not 0:
                self.__printTable(child)
            else:
                self.__buildTable(child)
    
    def __buildTable(self, symbol_table):
        for var in symbol_table.table:
            var_details = symbol_table.table[var]
            self.pretty_table.append_row([var, var_details[0], symbol_table.scope, var_details[1]])

    @property
    def table(self):
        return self.__table

    @property
    def children(self):
        return self.__children
        
    @property
    def scope(self):
        return self.__scope

    @property
    def parent(self):
        return self.__parent

    def get(self, key):
        return self.__table.get(key)
    
    # @symbol.setter
    def add(self, symbol, type, line):
        # type, line, is_initialized, is_used
        self.__table[symbol] = [type, line, False, False]

    def update(self, key, val):
        self.__table[key] = val

    def addChild(self, child):
        self.__children.append(child)
