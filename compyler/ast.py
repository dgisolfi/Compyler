#!/usr/bin/python3
# 2019-3-24

import itertools 

class AST:
    def __init__(self, cst, ast):
        self.__cst = cst
        self.__ast = ast
        self.__leaves = []
        self.traverseTree()

    @property
    def ast(self):
        return self.__ast

    def traverseTree(self):
        self.traverse(self.__cst.root, 0)
        print(self.ast)

    def traverse(self, node, depth):
        if len(node.children) is 0:
            pass
        else:
            if node.name == 'Block':
                self.ast.addNode(node.name, 'branch')
            elif node.name == 'AssignmentStatement':
                self.traverseAssignmentStatement(node)
            elif node.name == 'VarDecleration':
                self.traverseVarDecleration(node)
            elif node.name == 'PrintStatement':
                pass
            elif node.name == 'WhileStatement':
                pass
            elif node.name == 'IfStatement':
                pass

            for i in range(0, len(node.children)):
                self.traverse(node.children[i], depth+1)

    def findLeaves(self, node):
        self.__leaves = []
        leaves = self.__findLeaves(node)
        return self.__leaves
    
    def __findLeaves(self, node):
        if node.kind == 'leaf':
            self.__leaves.append(node)
            return node
        else:
            for child in node.children:
                leaves = self.__findLeaves(child)
            return leaves
            
    def traverseAssignmentStatement(self, node):
        self.ast.addNode(node.name, 'branch')
        print(node.children)
        # now add the ID and the value
        leaves = self.findLeaves(node)
        self.ast.addNode(leaves[0].name, 'leaf')
        self.ast.addNode(leaves[2].name, 'leaf')
        self.ast.cutOffChildren()

    
    def traverseVarDecleration(self, node):
        self.ast.addNode(node.name, 'branch')
        leaves = self.findLeaves(node)
        # now add the type and the ID
        self.ast.addNode(leaves[0].name, 'leaf')
        self.ast.addNode(leaves[1].name, 'leaf')
        self.ast.cutOffChildren()

        
