"""
Main file to generate the stories
"""

from story import StoryNode
from setup import ACTORS, PLACES, ITEMS
from methods import METHODS
from goals import GOALS, goals_satisfied
from search import bfs, idfs

if __name__ == "__main__":
    root = StoryNode(ACTORS, PLACES, ITEMS, "", 1)
    print(bfs(root,goals_satisfied))
