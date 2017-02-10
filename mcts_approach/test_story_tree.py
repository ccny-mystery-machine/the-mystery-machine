"""
Test file for the different methods related to the story tree
"""
from setup import *
from search import *
from methods import *
from story import StoryNode

class TestStoryNode:
    """
    Test class for the story node class
    """
    def test_children_empty_when_initialized(self):
        """
        Tests if the children are empty when story node is initialized
        """
        node = StoryNode(ACTORS, PLACES, ITEMS, "", 1)
        assert len(node.children) == 0

    def test_expand_child(self):
        """
        Tests if expand child adds a story node to children
        """
        node = StoryNode(ACTORS, PLACES, ITEMS, "", 1)
        node.expand_child()
        assert len(node.children) == 1

    def test_expand_all_children(self):
        """
        Tests if expand all children adds all story nodes
        """
        node = StoryNode(ACTORS, PLACES, ITEMS, "", 1)
        num_total_actions = len(node.possible_actions)
        node.expand_all_children()
        assert len(node.children) == num_total_actions
