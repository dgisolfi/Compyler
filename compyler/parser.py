#!/usr/bin/python3
# 2019-2-12

from tree import Tree

class Parser:
    def __init__(self, tokens):
       self.__tokens = tokens
       self.cst = Tree()

       self.cst.addNode('Root', 'Root', 'BRANCH')
       self.cst.endBranch()

       self.cst.addNode('test', 'test', 'BRANCH')
       
       
       print(self.cst)

    
