"""
Test file for the different functions in search.py
"""
from math import exp

from setup import ACTORS, PLACES, ITEMS
from state import State
from tree import TreeNode, TreeEdge, expand_edge
from search import select_func, best_child, uct_selection, update_node_value, backpropogate, most_visited_child

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
        root_state = State(ACTORS, PLACES, ITEMS)
        root_node = TreeNode(root_state)
        root_node.visits = exp(3)
        edge1 = expand_edge(root_node)
        edge1.next_node.visits = 6
        edge1.next_node.value = 1
        edge2 = expand_edge(root_node)
        edge2.next_node.visits = 6
        edge2.next_node.value = 3
        edge3 = expand_edge(root_node)
        edge3.next_node.visits = 1.5
        edge3.next_node.value = 1

        assert best_child(root_node, 1) == edge2.next_node

    def test_uct_selection(self):
        """
        Test UCT selection
        """
        root_state = State(ACTORS, PLACES, ITEMS)
        root_node = TreeNode(root_state)
        l = len(root_node.possible_methods)
        test_node = uct_selection(root_node, 1, 0)
        for r in range(l-1):
            uct_selection(root_node, 1, 0)
        
        assert uct_selection(root_node, 1, 0) == test_node

    def test_update_node_value(self):
        """
        Test Updating of Node Value
        """
        root_state = State(ACTORS, PLACES, ITEMS)
        root_node = TreeNode(root_state)
        root_node.value = 0
        root_node.visits = 0
        temp1 = 0
        temp2 = 0
        for r in range(10):
            temp1 += 1
            temp2 += r
            root_node.visits += 1
            update_node_value(root_node, r) 
            assert root_node.value == temp2/temp1

    def test_backpropogate(self):
        """
        Test Backpropogation
        """
        root_state = State(ACTORS, PLACES, ITEMS)
        root_node = TreeNode(root_state)
        edge1 = expand_edge(root_node)
        edge2 = expand_edge(edge1.next_node)
        edge3 = expand_edge(edge2.next_node)
        edge4 = expand_edge(edge2.next_node)
        backpropogate(edge3.next_node, 4)
        assert edge3.next_node.value == 4
        assert edge2.next_node.value == 4
        assert edge1.next_node.value == 4
        assert root_node.value == 4
        assert edge4.next_node.value == 0
        backpropogate(edge4.next_node, 8)
        assert edge3.next_node.value == 4
        assert edge2.next_node.value == 6
        assert edge1.next_node.value == 6
        assert root_node.value == 6
        assert edge4.next_node.value == 8

    def test_most_visited_child(self):
        """
        Test the Most Visited Child function
        """
        root_state = State(ACTORS, PLACES, ITEMS)
        root_node = TreeNode(root_state)
        edge1 = expand_edge(root_node)
        edge2 = expand_edge(root_node)
        edge3 = expand_edge(root_node)
        edge4 = expand_edge(root_node)
        edge1.next_node.visits = 3
        edge2.next_node.visits = 4
        edge3.next_node.visits = 5
        edge4.next_node.visits = 4

        assert most_visited_child(root_node) == edge3.next_node

    
