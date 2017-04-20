"""
Implementation of various search methods for story generation
"""
from queue import Queue
from math import log, sqrt
from random import randint

from goals import GOALS, goals_satisfied, percent_goals_satisfied 
from tree import (TreeNode, expand_edge, expand_all_edges, expand_rand_edge, 
                  expand_heuristic_edge, initialize_prob_dist, POSSIBLE_METHODS)
from story import Story

def uct_func(node, C):
    parent = node.parent_edge.prev_node
    if (node.visits == 0 and parent.visits == 0):
        return 0
    if (node.visits == 0):
        if (C < 0):
            return float("-inf")
        elif (C > 0): 
            return float("inf")
        else:
            return 0
    return node.value + C*sqrt(2*log(parent.visits)/node.visits)

def best_child(node, C):

    # Start with the selection function of first node
    best_node = node.edges[0].next_node        
    best_score = uct_func(best_node, C)
    
    # Compare with other node's selection function score 
    for edge in node.edges:
        curr_node = edge.next_node
        curr_score = uct_func(curr_node, C)
        if (curr_score > best_score):
            best_node = curr_node
            best_score = curr_score

    # Return the best child
    return best_node
     
def selection(node, C, thres):
    """
    Uses selection function to select most "promising" node on story tree
    """
    # Expand edge only if these conditions are satisfied
    while node.believability > 0:
        # If successful, returns expanded edge, if not, return False
        new_edge = expand_edge(node)
        if new_edge:
            # If new edge exists, return child node
            return new_edge.next_node
        else:
            # If all children are expanded, return best child
            node = best_child(node, C)
    return node

def rollout_value(believability, percent_goals_satisfied):
    return sqrt(believability) * percent_goals_satisfied

def rollout_story(node, max_simlength):
    root = TreeNode(node.state)
    curr_node = root
    numsims = 0
    while numsims < max_simlength and not goals_satisfied(curr_node, GOALS):
        expand_rand_edge(curr_node)
        curr_node = curr_node.edges[-1].next_node
        if curr_node.believability == 0:
            p_believability = curr_node.parent_edge.prev_node.believability
            curr_node.believability = p_believability * (numsims+1) / max_simlength
            break
        numsims += 1
    return rollout_value(curr_node.believability, percent_goals_satisfied(curr_node, GOALS))

def rollout_story_2(node, max_simlength):
    root = TreeNode(node.state)
    curr_node = root
    numsims = 0
    while numsims < max_simlength and not goals_satisfied(curr_node, GOALS):
        expand_rand_edge(curr_node)
        curr_node = curr_node.edges[-1].next_node
        if curr_node.believability == 0:
            curr_node = curr_node.parent_edge.prev_node
            continue
        numsims += 1
    print(Story(curr_node))
    return rollout_value(curr_node.believability, percent_goals_satisfied(curr_node, GOALS))

def rollout_story_3(node, max_simlength):
    # Create a new tree
    root = TreeNode(node.state)
    curr_node = root
    numsims = 0

    # Have probability distribution for each edge
    prob_dist = initialize_prob_dist()

    # Keep rolling out until max_simlength or goals satisfied
    while numsims < max_simlength:# and not goals_satisfied(curr_node, GOALS):
        
        # Choose edge based on prob_dist
        expand_heuristic_edge(curr_node, prob_dist)
        
        # Reassign current node to current node's child
        curr_node = curr_node.edges[-1].next_node
        
        # Update the simulation depth
        numsims += 1
    return rollout_value(curr_node.believability, percent_goals_satisfied(curr_node, GOALS))


def update_node_value(node, value):
    # Average value is updated
    node.value = ((node.visits-1)*node.value + value) / node.visits

def backpropogate(node, value):
    while node.parent_edge:
        node.visits += 1
        update_node_value(node, value)
        node = node.parent_edge.prev_node 
    node.visits += 1
    update_node_value(node, value)

def most_visited_child(node): 
    # Start with first node
    best_node = node.edges[0].next_node
    # Compare visits among all children
    for edge in node.edges:
        curr_node = edge.next_node
        if curr_node.visits > best_node.visits:
            best_node = curr_node
    # Return most visited child
    return best_node

def delete_children(node, chosen):
    node.edges = [chosen.parent_edge]

def mcts(node, max_iter, max_expansion, max_simlength, C, thres, debug):
    # Loop for every line in story 
    for count in range(max_iter):
        
        if debug:
            print("Master Iteration Number - " + str(count))
        
        # Loop for every simulation constructing story tree
        for num_expansion in range(max_expansion):
            
            if debug:
                print("Expansion Number - " + str(num_expansion))
         
            # Choose a node in the story tree
            chosen_node = selection(node, C, thres)
            # If the chosen node has a believability of 0, break it from the tree
            if chosen_node.believability == 0:
                chosen_node.parent_edge.prev_node.edges.pop()
            elif count > 0 and chosen_node.parent_edge.method.method == node.parent_edge.method.method:
                chosen_node.parent_edge.prev_node.edges.pop()
            elif count > 1 and (chosen_node.parent_edge.method.method == 
                                node.parent_edge.prev_node.parent_edge.method.method):   
                chosen_node.parent_edge.prev_node.edges.pop()
            else:
                # Simuluate if thres number of times
                for _ in range(thres):
                    sim_value = rollout_story_3(chosen_node, max_simlength)
                    backpropogate(chosen_node, sim_value)
        # Choose most visited node
        exp_node = most_visited_child(node) 
        # Remove all other edges from the tree - focus on most visited node subtree
        delete_children(node, exp_node)
        # Switch root to exp_node
        node = exp_node
    print("\n")
    return (node, Story(node))
