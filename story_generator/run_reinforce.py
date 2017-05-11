from setup import ACTORS, PLACES, ITEMS
from state import State
from tree import TreeNode, expand_index_edge
from random import random, randint
from reinforce import state_index_number_2
from story import Story
from copy import deepcopy
import pickle
import math

def softmax(arr):
    sftm_array = [ math.exp(x - max(arr)) for x in arr ]
    normalized_sftm_array = [ x / sum(sftm_array) for x in sftm_array ]
    return normalized_sftm_array
    
def prob_index(prob_arr):
    r = random()
    accum = 0
    for i, val in enumerate(prob_arr):
        accum += val
        if r < accum:
            return i 
    return False

def run_reinforce(depth = 15):
    with open("table2.pickle","rb") as table2file:
        table2 = pickle.load(table2file)
    root_state = State(ACTORS, PLACES, ITEMS)
    root_node = TreeNode(root_state, parent_edge = None, possible_methods = True)
    current_node = root_node
    
    for _ in range(depth):
        qvals = deepcopy(table2[state_index_number_2(current_node.state)])
        pidx = prob_index(softmax(qvals))
        edge = expand_index_edge(current_node, pidx)
        while edge.method.believability == 0:
            qvals.pop(pidx)
            pidx = prob_index(softmax(qvals))
            edge = expand_index_edge(current_node, pidx)
        current_node = edge.next_node
            
    return Story(current_node)


if __name__ == "__main__":
    print(run_reinforce(15))  
