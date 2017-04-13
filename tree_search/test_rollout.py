"""
Test file for MCTS rollout
"""
from setup import ACTORS, PLACES, ITEMS
from state import *
from tree import POSSIBLE_METHODS, TreeNode
from search import *

def rollout_test(num):
    root_state = random_state()
    root_node = TreeNode(root_state, parent_edge=None, possible_methods=True)
    return rollout_story_3(root_node, num)

def loop_rollout_test(num, total):
    good = 0
    for _ in range(total):
        if rollout_test(num) != 0:
            good += 1
    print(good/total)

