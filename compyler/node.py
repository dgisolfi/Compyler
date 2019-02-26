#!/usr/bin/python3
# 2019-2-12

class Node:
    def __init__(self, name, parent):
       self.__name = name
       self.__children = []
       self.__parent = parent

    # Getters for all attributes
    @property
    def name(self):
        return self.__name
    
    # @property
    # def data(self):
    #     return self.__data

    @property
    def children(self):
        return self.__children

    @property
    def parent(self):
        return self.__parent

    # @property
    # def depth(self):
    #     return self.__depth

    # Setters
    @parent.setter
    def setParent(self, parent):
        self.__parent = parent

    @children.setter
    def append(self, child):
        self.__children.append(child)

    # or not self.__root