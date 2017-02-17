"""
Test file for the different methods related to the story tree
"""
from copy import deepcopy

from setup import State, ACTORS, PLACES, ITEMS
from tree import TreeNode, TreeEdge, expand_edge, expand_all_edges

class TestState:
    """
    Test class for the story node class
    """
    def test_children_empty_when_initialized(self):
        """
        Tests if the children are empty when story node is initialized
        """
        root = State(ACTORS, PLACES, ITEMS)
        node = TreeNode(root)
        assert len(node.edges) == 0

    def test_expand_child(self):
        """
        Tests if expand child adds a story node to children
        """
        root = State(ACTORS, PLACES, ITEMS)
        node = TreeNode(root)
        expand_edge(node)
        assert len(node.edges) == 1

    def test_expand_all_children(self):
        """
        Tests if expand all children adds all story nodes
        """
        root = State(ACTORS, PLACES, ITEMS)
        node = TreeNode(root)
        num_total_actions = len(node.possible_methods)
        expand_all_edges(node)
        assert len(node.edges) == num_total_actions
