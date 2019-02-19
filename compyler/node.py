#!/usr/bin/python3
# 2019-2-12

class Node:
    def __init__(self, name, data, children, parent, depth):
       self.__name = name
       self.__data = data
       self.__children = children
       self.__parent = parent
       self.__depth = depth

    # Getters for all attributes
    @property
    def name(self):
        return self.__name
    
    @property
    def data(self):
        return self.__data

    @property
    def children(self):
        return self.__children

    @property
    def parent(self):
        return self.__parent

    @property
    def depth(self):
        return self.__depth

    # Setters
    @parent.setter
    def setParent(self, parent):
        self.__parent = parent

    # or not self.__root