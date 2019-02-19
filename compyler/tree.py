#!/usr/bin/python3
# 2019-2-12

from node import Node

class Tree:
    def __init__(self):
       self.__root = None
       self.cur_node = Node('Root', 'Root', [], {}, 0)

    def __str__(self):
        return self.traverse(self.__root, 0)

    def traverse(self, node, depth):
        tree = ''
        for i in range(0, depth):
            tree += '\t'

        # check for children
        if len(node.children) is not 0:
            # There are children so we will have to traverse deeper

            for child in len(node.children):
                self.traverse(node.children[child], depth+1)

        # There are no children, add the node and end the branch there
        else:
            tree += f'{node.name}\n'

        return tree

    # Return the root of the tree
    @property
    def root(self):
        return self.__root

    def endBranch(self):
        if self.cur_node.parent is not None and self.cur_node.name is not None:
            self.cur_node = self.cur_node.parent

    # Add a node to the tree
    def addNode(self, name, value, kind):
        node = Node(name, value, [], {}, 0)

        # Check if root needs to be updated
        if self.__root is None:
            self.__root = node
        # This is a child node
        else:
            # node.setParent(self.cur_node)
            node.setParent(self.cur_node)
            # add the child node into the current nodes known children
            self.cur_node.children.append(node)
        
        # check if the current node is a branch and update the current node
        if kind is 'Branch':
            self.cur_node = node
