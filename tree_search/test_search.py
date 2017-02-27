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
        """
        Test for the select_func function
        """
        root_state = State(ACTORS, PLACES, ITEMS)
        root_node = TreeNode(root_state)
        root_node.visits = exp(3)
        test_edge = expand_edge(root_node)
        test_node = test_edge.next_node
        test_node.visits = 6
        test_node.value = 0
        
        for C in range(0, 10):
            assert select_func(test_node, C) == C

        test_node.visits = 0
        assert select_func(test_node, 1) == float("inf")
        
        root_node.visits = 0
        assert select_func(test_node, 1) == 0

    def test_best_child_1(self):
        """
        Test for the best_child function
        """
#        root_state = State(ACTORS, PLACES, ITEMS)
#        root_node = TreeNode(root_state)
#        root_node.visits = exp(3)
#        expand
       
