#!/usr/bin/python3
# 2019-3-24

class AST:
    def __init__(self, cst, ast):
        self.__cst = cst
        self.__ast = ast
        self.traverseTree()

    @property
    def ast(self):
        return self.__ast

    def traverseTree(self):
        self.traverse(self.__cst.root, 0)

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
            print(self.__ast)
            for i in range(0, len(node.children)):
                self.traverse(node.children[i], depth+1)
            
    
    def traverseAssignmentStatement(self, node):
        self.ast.addNode(node.name, 'branch')
        # now add the ID and the value
        self.ast.addNode(node.children[0].children[0].name, 'leaf')
        self.ast.addNode(node.children[2].children[0].children[0].name, 'leaf')
    
    def traverseVarDecleration(self, node):
        self.ast.addNode(node.name, 'branch')
        # now add the type and the ID
        self.ast.addNode(node.children[0].children[0].name, 'leaf')
        self.ast.addNode(node.children[1].children[0].name, 'leaf')
        self.ast.cutOffChildren()

        
