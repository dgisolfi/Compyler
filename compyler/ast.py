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

    def findLeaves(self, node):
        self.__leaves = []
        self.__findLeaves(node)
        return self.__leaves
    
    def __findLeaves(self, node):
        if node.kind == 'leaf':
            self.__leaves.append(node)
            return node
        else:
            leaves = []
            for child in node.children:
                leaves = self.__findLeaves(child)
            return leaves

    def traverseTree(self):
        # The root will always be "program"
        # so get the block
        node = self.__cst.root.children[0]
        self.traverseStmt(node)

    def traverseStmtList(self, node):
        # Check wether this node has branches or leaves
        if len(node.children) is 0:
            # We need to be traversing things with children, so unless
            # this is the root move back up the tree as this branch is done
            if self.__ast.root.name == self.__ast.current_node.name:
                self.__ast.cutOffChildren()
        
        else:
            # If this is not epsilon then every StmtList is a combo
            # of statement followed by another statement list
            self.traverseStmt(node.children[0].children[0])
            self.traverseStmtList(node.children[1])


        
        # [print(i.name) for i in statement_list.children]

    def traverseStmt(self, node):

        if node.name == 'Block':
            self.traverseBlock(node)
        elif node.name == 'AssignmentStatement':
            self.traverseAssignmentStatement(node)
        elif node.name == 'VarDecleration':
            self.traverseVarDecleration(node)
        elif node.name == 'PrintStatement':
            pass
        elif node.name == 'WhileStatement':
            self.traverseWhileStatement(node)
        elif node.name == 'IfStatement':
            self.traverseIfStatement(node)
        else:
            # Epsilon
            pass

    def traverseBlock(self, node):
        self.__ast.addNode(node.name, 'branch')
        self.traverseStmtList(node.children[1])
  
    def traverseAssignmentStatement(self, node):
        self.__ast.addNode(node.name, 'branch')
        print(node.children)
        # now add the ID and the value
        # Check for Addition statement
        leaves = self.findLeaves(node)
        self.__ast.addNode(leaves[0].name, 'leaf')
        self.__ast.addNode(leaves[2].name, 'leaf')
        self.__ast.cutOffChildren()
    
    def traverseVarDecleration(self, node):
        self.__ast.addNode(node.name, 'branch')
        leaves = self.findLeaves(node)
        # now add the type and the ID
        self.__ast.addNode(leaves[0].name, 'leaf')
        self.__ast.addNode(leaves[1].name, 'leaf')
        self.__ast.cutOffChildren()

    def traverseWhileStatement(self, node):
        self.__ast.addNode(node.name, 'branch')
        
        # Get BooleanExpr
        self.traverseBooleanExprStatement(node.children[0])
        
        if node.children[1].name == 'Block':
            self.__ast.addNode('Block', 'branch')
            
        leaves = self.findLeaves(node.children[1])
        # [print(i.name) for i in leaves]
        self.__ast.cutOffChildren()

    def traverseIfStatement(self, node):
        self.__ast.addNode(node.name, 'branch')
        
        # Get BooleanExpr
        self.traverseBooleanExprStatement(node.children[0])
        
        if node.children[1].name == 'Block':
            self.__ast.addNode('Block', 'branch')
            
        leaves = self.findLeaves(node.children[1])
        # [print(i.name) for i in leaves]
        self.__ast.cutOffChildren()
       
    def traverseBooleanExprStatement(self, node):
        leaves = self.findLeaves(node)
        if leaves[2].name == '==':
            self.__ast.addNode('IsEqual', 'branch')
        elif leaves[2].name == '!=':
            self.__ast.addNode('NotEqual', 'branch')
        # Add first 
        self.__ast.addNode(leaves[1].name, 'leaf')
        # Add second
        self.__ast.addNode(leaves[3].name, 'leaf')
        self.__ast.cutOffChildren()


        
