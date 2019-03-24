
#!/usr/bin/python3
# 2019-3-24

from tree import Tree
from error import Error
from termcolor import colored

class SemanticAnalyser:
    def __init__(self, verbose, printmode, program, cst):
        self.ast = Tree(printmode)
        self.cst = cst
        self.warnings = 0
        self.errors = 0
        self.program = program     
        self.verbose = verbose
        self.buildAST()
        self.analyze()

    def buildAST(self):
        self.depthFirstTraversal(self.cst.root, 0)

    def depthFirstTraversal(self, node, depth):
        stuff = ['Block', 'AssignmentStatement', 'VarDecleration']
        # for i in range(0, depth):
        #     self.__tree += '-'

        if len(node.children) is 0:
            # Leaf Node
            pass
            # print({node.name})
        else:
            # Branch Node
            if node.name in stuff:
                self.ast.addNode(node.name, 'branch')
                print(self.ast)

            for i in range(0, len(node.children)):
                self.depthFirstTraversal(node.children[i], depth+1)
        

    def analyze(self):
        pass