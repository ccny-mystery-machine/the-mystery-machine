"""
Classes related to the Tree representation of the story
"""
from copy import deepcopy

from methods import Method, METHODS, POSSIBLE_METHODS

class TreeNode:
    """
    Node in our story tree
    """
    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent
        self.edges = []
        self.believability = 1
        if parent:
            self.believability = parent.believability

        # stores indices of all possible actions
        self.possible_methods = range(0, len(POSSIBLE_METHODS))

class TreeEdge:
    """
    Edge in our story tree
    """
    def __init__(self, method):
        self.method = Method(method)
        self.sentence = method.sentence
        self.believability = method.believability

    def __call__(self, node):
        self.prev_node = node
        self.next_node = TreeNode(node.state, node)
        self.method(self.next_node.state)


def expand_child(node):
    """
    Expands another child of the node - in reverse order
    Returns True if successful, False if not
    """
    if node.possible_methods:
        new_method_idx = node.possible_methods.pop()
        new_method = POSSIBLE_METHODS[new_action_idx]
        new_edge = TreeEdge(new_method)
        new_edge(node)
        node.edges.append(new_edge)
        return True

    return False


def expand_all_children(node):
    """
    Expands all possible actions
    """
    if node.possible_methods:
        for _ in range(0, len(node.possible_methods)):
            node.expand_child()
        return True

    return False

def create_story(node):
    """
    Creates a story object from a given node by traversing up the tree
    """
