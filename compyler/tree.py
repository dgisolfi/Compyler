#!/usr/bin/python3
# 2019-2-26
# Daniel Nicolas Gisolfi

from node import Node
from treelib import Node as Leaf
from treelib import Tree as Plant


class Tree:
    def __init__(self, printmode):
        self.__root = None
        # Create a 'Empty Object' to initialize
        # the current node
        self.__current_node = Node(None, None, None, None, None, None)
        self.__tree = ''
        self.__printmode = printmode

        # Keeps track of number of 
        # nodes to have unuiqe ids for each
        self.__nodes = 0
        self.__plant = Plant()

    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.__printmode:
            # pptree.print_tree(self.__root)
            self.__plant.show()
        else:
            self.traverse(self.__root, 0)
            print(self.__tree)
        
        return ''

    @property
    def current_node(self):
        return self.__current_node

    # Removes the current Node from the Tree
    def delCurNode(self):
        parent = self.__current_node.parent
        parent.children.pop()
        self.__current_node = parent

    @property
    def root(self):
        return self.__root

    def traverse(self, node, depth):
        for i in range(0, depth):
            self.__tree += '-'

        if len(node.children) is 0:
            # Leaf Node
            self.__tree += f'[ {node.name} ]\n'
        else:
            # Branch Node
            self.__tree += f'<{node.name}>\n'

            for i in range(0, len(node.children)):
                self.traverse(node.children[i], depth+1)
    
    def addNode(self, name, kind, **kwargs):
        line = kwargs.get('line', None)
        pos = kwargs.get('pos', None)
        
        # Create a new Node
        node = Node(name, Node(None, None, None, None, None, None), 
        self.__nodes, kind, line, pos)
        # Is this the root node??
        if self.__root is None or not self.__root:
            # This is the root node
            self.__root = node
            self.__plant.create_node(node.name, node.nid)
            
        else:
            # We a child, make the parent the cur node
            node.setParent = self.__current_node
            # Make sure our parent knows were there kid!
            self.__current_node.children.append(node)

            self.__plant.create_node(node.name, node.nid, parent=self.__current_node.nid)

        # Check if we are a branch node
        if kind is 'branch':
            # Update the current node
            self.__current_node = node

        self.__nodes += 1


    # Was trying to make it sound better than ending a child like alan did. 
    # Now its like your kicking your 30 y/old child out of the house!
    def cutOffChildren(self):
        # Move up to the parent node if possible
        if self.__current_node.parent is not None and self.__current_node.parent.name is not None:
            self.__current_node = self.__current_node.parent
        else:
            fact = 'BIG OOF. This should never happen!'