"""
Classes related to the Tree representation of the story
"""
from copy import deepcopy
from random import randint, random

from methods import Method, METHODS, create_possible_methods

POSSIBLE_METHODS = []

class TreeNode:
    """
    Node in our story tree
    """
    def __init__(self, state, parent_edge = None, possible_methods = False):
        global POSSIBLE_METHODS
        self.state = state
        if possible_methods:
            POSSIBLE_METHODS = create_possible_methods(state)
        self.parent_edge = parent_edge
        self.edges = []
        self.height = 0
        self.believability = 1
        self.value = 0 
        self.visits = 0

        # stores indices of all possible actions
        self.possible_methods = list(range(0, len(POSSIBLE_METHODS)))

class TreeEdge:
    """
    Edge in our story tree
    """
    def __init__(self, method):
        self.method = Method(method)
        self.prev_node = None
        self.next_node = None

    def __call__(self, node):
        self.method(node.state)
        self.prev_node = node
        self.next_node = TreeNode(self.method.next_state, self)

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
        return new_edge

    return False

def expand_rand_edge(node):
    """
    Expands random edge of the node
    Returns True if successful, False if not
    """
    poss_meth = node.possible_methods
    if poss_meth:
        new_method_idx = poss_meth.pop(randint(0, len(poss_meth) - 1))
        new_method = POSSIBLE_METHODS[new_method_idx]
        new_edge = TreeEdge(new_method)
        new_edge(node)
        node.edges.append(new_edge)
        return new_edge

    return False

def initialize_prob_dist():
    prob_dist = {}
    for methods in POSSIBLE_METHODS:
        prob_dist[methods.func.__name__] = 1
    return prob_dist


def expand_heuristic_edge(node, prob_dist):
    """
    Expands an edge based off of heuristic
    """
    poss_meth = node.possible_methods
    if poss_meth:
        while True:        
            while True:
                new_method_idx = poss_meth[randint(0, len(poss_meth) - 1)]
                new_method = POSSIBLE_METHODS[new_method_idx]
                rand_num = random()
                prob_method = prob_dist[new_method.func.__name__]
                if rand_num <= prob_method:
                    break
        
            new_edge = TreeEdge(new_method)
            new_edge(node)
        
            if new_edge.method.believability != 0:
                break

        for p in prob_dist:
            prob_dist[p] *= 1.4
        prob_dist[new_method.func.__name__] /= 2
        node.edges.append(new_edge)
        return new_edge

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
