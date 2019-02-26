#!/usr/bin/python3
# 2019-2-26

import pptree 
from node import Node

class Tree:
    def __init__(self):
        self.__root = None
        # Create a 'Empty Object' to initialize
        # the current node
        self.current_node = Node(None, None)
        self.__tree = ''

    def __repr__(self):
        return str(self)

    def __str__(self):
        # self.traverse(self.__root, 0)
        # print(self.__tree)
        pptree.print_tree(self.__root)
        return ''

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
    
    def addNode(self, name, kind):
        # Create a new Node
        node = Node(name, Node(None, None))
        # Is this the root node??
        if self.__root is None or not self.__root:
            # This is the root node
            self.__root = node
            # Leaf(node.name)
        else:
            # We a child, make the parent the cur node
            node.setParent = self.current_node
            # Make sure our parent knows were there kid!
            self.current_node.children.append(node)

        # Check if we are a branch node
        if kind is 'branch':
            # Update the current node
            self.current_node = node


    # Was trying to make it sound better than ending a child like alan did. 
    # Now its like your kicking your 30 y/old child out of the house!
    def cutOffChildren(self):
        # Move up to the parent node if possible
        if self.current_node.parent is not None and self.current_node.parent.name is not None:
            self.current_node = self.current_node.parent
        else:
            print('BIG OOF. This should never happen')