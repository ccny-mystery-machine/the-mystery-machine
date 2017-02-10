"""
Implementation of various search methods for story generation
"""

from queue import Queue

# too memory exhaustive
def bfs(state, goal):
    q = Queue()
    q.put(state)
    while not q.empty():
        s = q.get()
        if s.believability == 0:
            continue
        if goal(s) or len(s.story) > 150:
            return s.story
        s.expand_all_children()
        for child in s.children:
            q.put(child)

# iterative depth first search to relax memory
def idfs(state, goal):
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
        story = dfs(state, depth)
        if story:
            return story
