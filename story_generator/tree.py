"""
Classes related to the Tree representation of the story
"""
from copy import deepcopy
from random import randint, random

from methods import Method, METHODS, create_possible_methods

POSSIBLE_METHODS = []
METHOD_TO_INDEX = {}

class TreeNode:
    """
    Node in our story tree - Acts as wrapper to state
    """
    def __init__(self, state, parent_edge = None, possible_methods = False):
        
        # Allow global variable to be modified within function         
        global POSSIBLE_METHODS
        global METHOD_TO_INDEX
 
        if possible_methods:
            # Create all partial methods and store them globally
            POSSIBLE_METHODS = create_possible_methods(state)
            for i,val in enumerate(POSSIBLE_METHODS):
                METHOD_TO_INDEX[val] = i
 
        """Tree fields"""
        self.state = state
        # Tree edge that points to the self node and the parent node
        self.parent_edge = parent_edge
        # All potential edges that link to children nodes
        self.edges = []
        # Node depth within tree
        self.height = 0
        # Stores indices of all possible actions
        self.possible_methods = list(range(0, len(POSSIBLE_METHODS)))
        
        """MCTS fields"""
        # Cumulative Believability score of all parent nodes until self node
        self.believability = 1
        # Function of believability and goals completed from MCTS rollouts
        self.value = 0 
        # Number of MCTS visits to self node
        self.visits = 0


class TreeEdge:
    """
    Edge in our story tree - Acts as wrapper to Method
    """
    def __init__(self, method):
        # Initialize Method Object
        self.method = Method(method)
        self.prev_node = None
        self.next_node = None
        self.qval = 0.1

    def __call__(self, node):
        # Connect the method to the state
        self.method(node.state)
        # Connect the edge to the node
        self.prev_node = node
        self.next_node = TreeNode(self.method.next_state, self)
        
        # Increase Height
        self.next_node.height = self.prev_node.height + 1

        # Cummulative Update of Believability
        self.next_node.believability = (self.prev_node.believability * 
                                        self.prev_node.height +
                                        self.method.believability) / self.next_node.height


def expand_edge(node):
    """
    Expands another edge of the node - in reverse order
    Returns True if successful, False if not
    """
    # Check if there are still methods to explore
    if node.possible_methods:
        # Choose last explorable method
        new_method_idx = node.possible_methods.pop()
        new_method = POSSIBLE_METHODS[new_method_idx]
        
        # Construct a tree edge from method
        new_edge = TreeEdge(new_method)
        # Connect edge to node
        new_edge(node)
        node.edges.append(new_edge)
        
        # Return edge
        return new_edge

    # If no explorable methods, return False
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
    # Set all methods to have probability 1
    prob_dist = {}
    for methods in POSSIBLE_METHODS:
        prob_dist[methods.func.__name__] = 1
    return prob_dist


def expand_heuristic_edge(node, prob_dist):
    """
    Expands an edge based off of heuristic
    """
    # Reference to index list
    poss_meth = node.possible_methods
    if poss_meth:
        # Two Do-While Loop
        while True:
            # Choose method
            while True:
                # choose a random method
                new_method_idx = poss_meth[randint(0, len(poss_meth) - 1)]
                new_method = POSSIBLE_METHODS[new_method_idx]
                
                # Accept that method with probability prob_dist(method)
                rand_num = random()
                prob_method = prob_dist[new_method.func.__name__]
                
                if rand_num <= prob_method:
                    break
        
            # Check if believable
            new_edge = TreeEdge(new_method)
            new_edge(node)
        
            if new_edge.method.believability != 0:
                break

        # Change probability distribution
        INC = 1.4
        DEC = 2
        for p in prob_dist:
            prob_dist[p] *= INC
        prob_dist[new_method.func.__name__] /= (DEC*INC) 
        
        # Add and return new edge
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

def expand_all_believable_edges(node, debug):
    if len(node.possible_methods) <= 0:
        return False
    for _ in range(len(node.possible_methods)):
        edge = expand_edge(node)
        if edge.method.believability == 0:
            node.edges.pop()
#            if debug:
#                print("Pruned unbelievable node")
        elif edge.next_node.believability < 0.65:
            node.edges.pop()
#            if debug:
#                print("Pruned unlikely node")
        elif node.height > 1:
            if edge.method.method == node.parent_edge.method.method:
                node.edges.pop()
#                if debug:
#                    print("Pruned repeat-1 node")
                continue
            if node.height > 2:
                parent_node = node.parent_edge.prev_node
                if (edge.method.method == 
                        parent_node.parent_edge.method.method):
                    node.edges.pop()
#                    if debug:
#                        print("Pruned repeat-2 node")
#        elif debug:
#            print('\t' + edge.method.sentence)
    return True

def choose_q_edge(node, epsilon):
    if random() < epsilon:
        return node.edges[ randint(0, len(node.edges) - 1) ]
    return choose_max_q_edge(node)


def choose_max_q_edge(node):
    epsilon = 1e-5
    chosen_edge = node.edges[0]
    candidates = [chosen_edge]
    for edge in node.edges:
        if edge.qval > chosen_edge.qval + epsilon:
            chosen_edge = edge
            candidates = [chosen_edge]
        elif abs(edge.qval - chosen_edge.qval) < epsilon:
            candidates.append(edge) 
    return candidates[randint(0, len(candidates) - 1)]

def find_edge_index(edge):
    return METHOD_TO_INDEX[edge.method.method]
