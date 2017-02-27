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
    root_node.visits = 1000 
    test_edge = expand_edge(root_node)
    test_node = test_edge.next_node
    test_node.visits = 100
    val = select_func(test_node, 1)
    #found_story = idfs(root_node, goals_satisfied)
    #found_story = mcts(root_node, 5, 100, 10)
    print(val)
    #print(found_story)
