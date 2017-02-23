"""
Implementation of various search methods for story generation
"""

from queue import Queue

from goals import GOALS
from tree import expand_all_edges
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

def uct_selection(node):
    # Fill in later
    return None


def rollout_story(node):
    # Fill In later
    return None

def backpropogate(node, value):
    # Fill In later
    return None

def most_visited_child(node):
    # Fill In later
    return None


def mcts(node, max_iter, max_numsim):
    for _ in range(max_iter):
        for numsim in range(max_numsim):
            chosen_node = uct_selection(node)
            sim_value = rollout_story(chosen_node)
            backpropogate(chosen_node, sim_value)
        exp_node = most_visited_child(node) 
        delete_children(node, exp_node)
        node = exp_node
    return Story(node)
