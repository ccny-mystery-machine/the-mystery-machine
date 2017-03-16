"""
Test file for the different methods related to the story tree
"""
from copy import deepcopy

from setup import State, ACTORS, PLACES, ITEMS
from tree import TreeNode, TreeEdge, expand_edge, expand_all_edges

class TestNode:
    """
    Test class for the node class
    """
    def test_edges_empty_when_initialized(self):
        """
        Tests if the children are empty when story node is initialized
        """
        root = State(ACTORS, PLACES, ITEMS)
        node = TreeNode(root, possible_methods = True)
        assert len(node.edges) == 0

    def test_expand_edge(self):
        """
        Tests if expand child adds a story node to children
        """
        root = State(ACTORS, PLACES, ITEMS)
        node = TreeNode(root, possible_methods = True)
        expand_edge(node)
        assert len(node.edges) == 1

    def test_expand_all_edges(self):
        """
        Tests if expand all children adds all story nodes
        """
        root = State(ACTORS, PLACES, ITEMS)
        node = TreeNode(root, possible_methods = True)
        num_total_actions = len(node.possible_methods)
        expand_all_edges(node)
        assert len(node.edges) == num_total_actions

class TestEdge:
    """
    Test class for the edge class
    """

    def test_edges_point_to_new_node(self):
        """
        Tests if expanded edges point to new nodes
        """
        root = State(ACTORS, PLACES, ITEMS)
        node = TreeNode(root, possible_methods = True)
        expand_all_edges(node)
        for edge in node.edges:
            assert len(edge.method.sentence) > 0
