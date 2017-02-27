"""
Implementation of various search methods for story generation
"""

from queue import Queue
from math import log, sqrt
from random import randint

from goals import GOALS, goals_satisfied, percent_goals_satisfied 
from tree import TreeNode, expand_edge, expand_all_edges
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
     
def uct_selection(node):
    while node.believability > 0:
        new_edge = expand_edge(node)
        if new_edge:
            return new_edge.next_node
        else:
           node = best_child(node, 1)
    return node

def rollout_story(node, max_simlength):
    root = TreeNode(node.state)
    curr_node = root
    numsims = 0
    while (numsims < max_simlength or goals_satisfied(curr_node, GOALS)):
        expand_all_edges(curr_node)
        curr_node.edges = [edge for edge in curr_node.edges if edge.method.believability > 0] 
        ridx = randint(0, len(curr_node.edges) - 1)
        curr_node.edges = [curr_node.edges[ridx]]
        curr_node = curr_node.edges[0].next_node    
        numsims += 1
    value = curr_node.believability * percent_goals_satisfied(curr_node, GOALS)
    return value

def update_node_value(node, value):
    prev_value = node.value
    node.value = ((node.visits-1)*prev_value + value) / node.visits

def backpropogate(node, value):
    while node.parent_edge:
        node.visits += 1
        update_node_value(node, value)
        node = node.parent_edge.prev_node  

def most_visited_child(node): 
    best_node = node.edges[0].next_node        
    for edge in node.edges:
        curr_node = edge.next_node
        if (curr_node.visits > best_node.visits):
            best_node = curr_node
    return best_node

def delete_children(node, chosen):
    node.edges = [chosen.parent_edge]

def mcts(node, max_iter, max_numsim, max_simlength):
    for _ in range(max_iter):
        for numsim in range(max_numsim):
            chosen_node = uct_selection(node)
            if chosen_node.believability == 0:
                chosen_node.visits += 1
                chosen_node.value = 0
            else:
                sim_value = rollout_story(chosen_node, max_simlength)
                backpropogate(chosen_node, sim_value)
        exp_node = most_visited_child(node) 
        delete_children(node, exp_node)
        node = exp_node
    return Story(node)
