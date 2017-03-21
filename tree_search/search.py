"""
Implementation of various search methods for story generation
"""

from queue import Queue
from math import log, sqrt
from random import randint

from goals import GOALS, goals_satisfied, percent_goals_satisfied 
from tree import TreeNode, expand_edge, expand_all_edges, expand_rand_edge
from story import Story

# memory exhaustive
def bfs(node, goal):
    q = Queue()
    q.put(node)
    while not q.empty():
        s = q.get()
        if s.believability == 0:
            continue
        if goal(s, GOALS) or s.height > 3:
            return Story(s)
        expand_all_edges(s)
        for edge in s.edges:
            q.put(edge.next_node)

# iterative deepening depth first search to relax memory
def idfs(node, goal):
    def dfs(current, depth):
        if current.believability == 0:
            return
        if depth == 0:
            if goal(current, GOALS):
                return Story(current)
            return
        expand_all_edges(current)
        for edge in current.edges:
            story = dfs(edge.next_node, depth - 1)
            if story:
                return story

    for depth in range(0,10):
        story = dfs(node, depth)
        if story:
            return story

def select_func(node, C):
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
    best_node = node.edges[0].next_node        
    best_score = select_func(best_node, C)
    for edge in node.edges:
        curr_node = edge.next_node
        curr_score = select_func(curr_node, C)
        if (curr_score > best_score):
            best_node = curr_node
            best_score = curr_score
    return best_node
     
def uct_selection(node, C, thres):
    while node.believability > 0 and node.visits > thres:
        new_edge = expand_edge(node)
        # print("Expanded edge?")
        if new_edge:
            # print("Expanded edge!")
            return new_edge.next_node
        else:
            # print("Didn't expand edge!")
            node = best_child(node, C)
    return node

def rollout_policy_1(node):
    print("Before expand")
    expand_all_edges(node)
    print("After expand")
    node.edges = [edge for edge in node.edges if edge.method.believability > 0]
    ridx = randint(0, len(node.edges) - 1)
    node.edges = [node.edges[ridx]]
    return node.edges[0].next_node

def rollout_policy_2(node):
    while True:
        expand_rand_edge(node)
        if node.edges[-1].next_node.believability != 0:
            break
    return node.edges[-1].next_node

def rollout_policy_3(node):
    expand_rand_edge(node)
    return node.edges[-1].next_node

def rollout_story(node, max_simlength):
    root = TreeNode(node.state)
    curr_node = root
    numsims = 0
    while (numsims < max_simlength and not goals_satisfied(curr_node, GOALS)):
        curr_node = rollout_policy_3(curr_node)    
        if curr_node.believability == 0:
            curr_node.believability = 0.001
            break
        #print( curr_node.believability )
        #print( str(numsims) + " " + str(max_simlength) )
        numsims += 1
    value = curr_node.believability * percent_goals_satisfied(curr_node, GOALS)
    #print(  percent_goals_satisfied(curr_node, GOALS) )
    #print( value )
    #return Story(curr_node)
    return value

def update_node_value(node, value):
    prev_value = node.value
    node.value = ((node.visits-1)*prev_value + value) / node.visits

def backpropogate(node, value):
    while node.parent_edge:
        node.visits += 1
        update_node_value(node, value)
        node = node.parent_edge.prev_node 
    node.visits += 1
    update_node_value(node, value)

def most_visited_child(node): 
    # print("Edge Length - most visited child:", len(node.edges))
    best_node = node.edges[0].next_node        
    for edge in node.edges:
        curr_node = edge.next_node
        if (curr_node.visits > best_node.visits):
            best_node = curr_node
    return best_node

def delete_children(node, chosen):
    node.edges = [chosen.parent_edge]

def mcts(node, max_iter, max_numsim, max_simlength, C, thres):
    for count in range(max_iter):
        print( "Master Iteration Number - " + str(count))
        for numsim in range(max_numsim):
            print( "Simulation Number - " + str(numsim))
            chosen_node = uct_selection(node, C, thres)
            if chosen_node.believability == 0:
                chosen_node.parent_edge.prev_node.edges.pop()
            else:
                sim_value = rollout_story(chosen_node, max_simlength)
                # print("Rollout")
                backpropogate(chosen_node, sim_value)
                # print("Backprop")
        exp_node = most_visited_child(node) 
        delete_children(node, exp_node)
        node = exp_node
    print("\n")
    return (node, Story(node))
