"""
Main file to generate the stories
"""

from tree import TreeNode, TreeEdge, expand_edge
from setup import State, ACTORS, PLACES, ITEMS
from goals import goals_satisfied
from search import *
from methods import POSSIBLE_METHODS

if __name__ == "__main__":
    root_state = State(ACTORS, PLACES, ITEMS)
    root_node = TreeNode(root_state)
    print( rollout_story(root_node, 10) )
