#!/usr/bin/python3
# 2019-3-24
# Daniel Nicolas Gisolfi

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

        if len(node.children) == 0:
            # We need to be traversing things with children, so unless
            # this is the root move back up the tree as this branch is done
            if self.__ast.root.name == self.__ast.current_node.name:
                self.__ast.cutOffChildren()
        
        else:
            # If this is not epsilon then every StmtList is a combo
            # of statement followed by another statement list
            self.traverseStmt(node.children[0].children[0])
            if len(node.children) > 1:
                self.traverseStmtList(node.children[1])

         


    def traverseStmt(self, node):

        if node.name == 'Block':
            self.traverseBlock(node)
        elif node.name == 'AssignmentStatement':
            self.traverseAssignmentStatement(node)
        elif node.name == 'VarDecleration':
            self.traverseVarDecleration(node)
        elif node.name == 'PrintStatement':
            self.traversePrintStatement(node)
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

    def traverseAdd(self, node):
        self.__ast.addNode('Add', 'branch')
        leaves = self.findLeaves(node.children[0])

        # add first value
        self.__ast.addNode(leaves[0].name, 'leaf',
        line=leaves[0].line, pos=leaves[0].position)
        # skip the plus sign then add the second value
        if node.children[2].name is 'Expr':
            self.traverseExpr(node.children[2])
        else:
            self.__ast.addNode(node.children[2].name, 'leaf',
            line=node.children[2].line, pos=node.children[2].position)


    def traverseExpr(self, node):
        # Check the Expr kind using the 1st child
        kind = node.children[0].name
        leaves = self.findLeaves(node)

        if kind == 'IntExpr':
            # check for addition stmt
            if len(node.children[0].children) > 1:
                self.traverseAdd(node.children[0])
                self.__ast.cutOffChildren()
            else:
                self.__ast.addNode(leaves[0].name, 'leaf',
                line=leaves[0].line, pos=leaves[0].position)
               
        elif kind == 'Id':
            self.__ast.addNode(leaves[0].name, 'leaf',
            line=leaves[0].line, pos=leaves[0].position)
            
        elif kind == 'StringExpr':
            self.__ast.addNode('CharList', 'branch')
            string = ''
            for leaf in leaves:
                if leaf.name != '\"':
                    string += leaf.name
            self.__ast.addNode(string, 'leaf',
            line=leaves[0].line, pos=leaves[0].position)
            self.__ast.cutOffChildren()
        
        elif kind == 'BooleanExpr':
            if len(node.children[0].children) > 1:
                self.traverseBooleanExprStatement(node.children[0])
            else:
                self.__ast.addNode(leaves[0].name, 'leaf',
                line=leaves[0].line, pos=leaves[0].position)


  
    def traverseAssignmentStatement(self, node):
        self.__ast.addNode(node.name, 'branch')
        # now add the ID and the value
        # Check for Addition statement
        leaves = self.findLeaves(node)
        self.__ast.addNode(leaves[0].name, 'leaf',
        line=leaves[0].line, pos=leaves[0].position)

        self.traverseExpr(node.children[2])
        self.__ast.cutOffChildren()
    
    def traverseVarDecleration(self, node):
        self.__ast.addNode(node.name, 'branch')
        leaves = self.findLeaves(node)
        # now add the type and the ID
        self.__ast.addNode(leaves[0].name, 'leaf',
        line=leaves[0].line, pos=leaves[0].position)
        self.__ast.addNode(leaves[1].name, 'leaf',
        line=leaves[1].line, pos=leaves[1].position)
        self.__ast.cutOffChildren()

    def traversePrintStatement(self, node):
        self.__ast.addNode(node.name, 'branch')
        self.traverseExpr(node.children[2])
        self.__ast.cutOffChildren()

    def traverseWhileStatement(self, node):
        self.__ast.addNode(node.name, 'branch')

        # Get BooleanExpr
        self.traverseBooleanExprStatement(node.children[0])

        if node.children[1].name == 'Block':
            self.traverseBlock(node.children[1])

        self.__ast.cutOffChildren()

    def traverseIfStatement(self, node):
        self.__ast.addNode(node.name, 'branch')
        
         # Get BooleanExpr
        self.traverseBooleanExprStatement(node.children[0])
        
        if node.children[1].name == 'Block':
            self.traverseBlock(node.children[1])

        self.__ast.cutOffChildren()

       
    def traverseBooleanExprStatement(self, node):
       
        # check for boolean values
        if len(node.children) is 1: 
            leaves = self.findLeaves(node)
            self.__ast.addNode(leaves[0].name, 'leaf',
            line=leaves[0].line, pos=leaves[0].position)
        else:
            leaves = self.findLeaves(node.children[2])
            if leaves[0].name == '==':
                self.__ast.addNode('IsEqual', 'branch')
            elif leaves[0].name == '!=':
                self.__ast.addNode('NotEqual', 'branch')
            # Add first 
            self.traverseExpr(node.children[1])
            # Add second
            self.traverseExpr(node.children[3])
            
            self.__ast.cutOffChildren()