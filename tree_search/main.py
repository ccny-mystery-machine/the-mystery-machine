"""
Main file to generate the stories
"""

from tree import TreeNode, TreeEdge, expand_edge
from setup import ACTORS, PLACES, ITEMS
from state import State, random_state
from search import mcts
from methods import create_possible_methods
from goals import percent_goals_satisfied, GOALS


def print_rollout():
    """
    Prints out the rollout - Assumes rollout function outputs a story
    """
    root_state = random_state()
    root_node = TreeNode(root_state, parent_edge=None, possible_methods=True)
    print( rollout_story(root_node, 10) )


def run_once(debug):
    # Randomly assigns actors, places, and items for story
    root_state = random_state(3,3) 
    
    # Initialize Root Node - Possible Methods boolean MUST BE TRUE 
    root_node = TreeNode(root_state, parent_edge=None, possible_methods=True)

    # Total methods in story
    num_methods = len(root_node.possible_methods)
    
    """
    The following 
        max_numsim = max_expansion * thres

    max_iter : Number of sentances in story = number of story nodes - 1 = number of story edges
    max_expansion : Number of expansions in search
    max_simlength : Maximum length of rollout
    C : Exploration Constant for selection
    thres : Minimum MCTS Visits for node expansion
    """
    # Perform Monte Carlo - returns final node and whole story
    max_expansion = 300
    if max_expansion < len(root_node.possible_methods):
        raise ValueError("Max exp ({}) should be greater than num methods({})".format(max_expansion, len(root_node.possible_methods)))

    max_iter = 15
    max_simlength = 25
    C = 1
    thres = 60
    print("Max iteration: {}\nMax Expansion: {}\nMax simulation length: {}\nC: {}\nThreshold: {}".format(max_iter, max_expansion, max_simlength, C, thres))
    n, s = mcts(root_node, max_iter, max_expansion, max_simlength, C, thres, debug=True) 
    
    # Print out results
    if debug:
        print(s)
        print(n.believability)
        print(n.value)
        print(percent_goals_satisfied(n, GOALS))
    
    return (n,s)
    
if __name__ == "__main__":
    run_once(True)
