"""
Implementation of various search methods for story generation
"""

from queue import Queue

def bfs(state, goal):
    q = Queue()
    q.put(state)
    while q.not_empty():
        s = q.get()
        if goal(s):
            return s.story
        s.expand_all_children()
