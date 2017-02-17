"""
Classes related to the Tree representation of the story
"""
from copy import deepcopy

from methods import Method, METHODS, POSSIBLE_METHODS

class TreeNode:
    """
    Node in our story tree
    """
    def __init__(self, state, parent_edge = None):
        self.state = state
        self.parent_edge = parent_edge
        self.edges = []
        self.height = 0
        self.believability = 1

        # stores indices of all possible actions
        self.possible_methods = list(range(0, len(POSSIBLE_METHODS)))

class TreeEdge:
    """
    Edge in our story tree
    """
    def __init__(self, method):
        self.method = Method(method)
        self.sentence = self.method.sentence
        self.believability = self.method.believability

    def __call__(self, node):
        self.prev_node = node
        self.next_node = TreeNode(node.state, self)
        self.method(self.next_node.state)
        self.next_node.believability = (self.prev_node.believability *
                                        self.method.believability)
        self.next_node.height = self.prev_node.height + 1


def expand_edge(node):
    """
    Expands another edge of the node - in reverse order
    Returns True if successful, False if not
    """
    if node.possible_methods:
        new_method_idx = node.possible_methods.pop()
        new_method = POSSIBLE_METHODS[new_method_idx]
        new_edge = TreeEdge(new_method)
        new_edge(node)
        node.edges.append(new_edge)
        return True

    return False


def expand_all_edges(node):
    """
    Expands all possible actions
    """
    if node.possible_methods:
        for _ in range(0, len(node.possible_methods)):
            expand_edge(node)
        return True

    return False
