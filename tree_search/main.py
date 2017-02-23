"""
Main file to generate the stories
"""

from tree import TreeNode
from setup import State, ACTORS, PLACES, ITEMS
from goals import goals_satisfied
from search import bfs, idfs
from methods import POSSIBLE_METHODS

if __name__ == "__main__":
    root_state = State(ACTORS, PLACES, ITEMS)
    root_node = TreeNode(root_state)
    found_story = idfs(root_node, goals_satisfied)
    print(found_story)
