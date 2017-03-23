"""
Main file to generate the stories
"""

from tree import TreeNode, TreeEdge, expand_edge
from setup import ACTORS, PLACES, ITEMS
from state import State, random_state
from search import mcts
from methods import create_possible_methods


def print_rollout():
    """
    Prints out the rollout - Assumes rollout function outputs a story
    """
    root_state = random_state()
    root_node = TreeNode(root_state, parent_edge=None, possible_methods=True)
    print( rollout_story(root_node, 10) )

if __name__ == "__main__":
    root_state = random_state()
    root_node = TreeNode(root_state, parent_edge=None, possible_methods=True)
    num_methods = len(root_node.possible_methods)
    # max_numsim > num_methods * thres
    n, s = mcts(root_node, max_iter=12, max_numsim=10000, max_simlength=50, C=1, thres=40) 
    print(s)
    print(n.believability)
    print(n.value)
