"""
Implementation of various search methods for story generation
"""

from queue import Queue

from goals import GOALS
from tree import expand_all_children

# memory exhaustive
def bfs(node, goal):
    q = Queue()
    q.put(node)
    while not q.empty():
        s = q.get()
        if s.believability == 0:
            continue
        if goal(s, GOALS) or len(s.story) > 200:
            return s.story
        s.expand_all_children()
        for child in s.children:
            q.put(child)

# iterative deepening depth first search to relax memory
def idfs(node, goal):
    def dfs(current, depth):
        if current.believability == 0:
            return
        if depth == 0:
            if goal(current):
                return current.story
            return
        current.expand_all_children()
        for child in current.children:
            story = dfs(child, depth - 1)
            if story:
                return story

    for depth in range(0,5):
        story = dfs(node, depth)
        if story:
            return story
