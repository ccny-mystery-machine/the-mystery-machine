"""
Main file to generate the stories
"""

from tree import TreeNode
from setup import State, ACTORS, PLACES, ITEMS
from goals import goals_satisfied
from search import bfs, idfs, mcts
from methods import POSSIBLE_METHODS

if __name__ == "__main__":
    root_state = State(ACTORS, PLACES, ITEMS)
    root_node = TreeNode(root_state)
    found_story = mcts(root_node, 5, 100, 10)
    print(found_story)
