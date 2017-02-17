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
        current.expand_all_edges()
        for edge in current.edges:
            story = dfs(edge.next_node, depth - 1)
            if story:
                return story

    for depth in range(0,5):
        story = dfs(node, depth)
        if story:
            return story
