"""
Test file for the different functions in search.py
"""
from math import exp

from setup import State, ACTORS, PLACES, ITEMS
from tree import TreeNode, TreeEdge, expand_edge 
from search import select_func

class TestSearch:
    """
    Test class for the function in search.py
    """
    def test_select_func_1(self):
        root_state = State(ACTORS, PLACES, ITEMS)
        root_node = TreeNode(root_state)
        root_node.visits = exp(3)
        test_edge = expand_edge(root_node)
        test_node = test_edge.next_node
        test_node.visits = 6
        test_node.value = 0
        
        assert select_func(test_node, 1) == 1
