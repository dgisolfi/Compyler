#!/usr/bin/python3
# 2019-2-12
# Daniel Nicolas Gisolfi

class Node:
    def __init__(self, name, parent, nid, kind, line, pos):
        self.__name = name
        self.__children = []
        self.__parent = parent
        # id for treelib to use
        self.__nid = nid 
        # to hold kind of node (leaf or branch)
        self.__kind = kind

        self.__line = line
        self.__position = pos


    # Getters for all attributes
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def children(self):
        return self.__children

    @property
    def parent(self):
        return self.__parent

    @property
    def nid(self):
        return self.__nid
    
    @property
    def kind(self):
        return self.__kind

    @property
    def line(self):
        return self.__line

    @property
    def position(self):
        return self.__position

    # Setters
    @parent.setter
    def setParent(self, parent):
        self.__parent = parent

    @children.setter
    def append(self, child):
        self.__children.append(child)
