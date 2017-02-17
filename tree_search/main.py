"""
Main file to generate the stories
"""

from tree import TreeNode
from setup import State, ACTORS, PLACES, ITEMS
from goals import goals_satisfied
from search import bfs, idfs

if __name__ == "__main__":
    root_state = State(ACTORS, PLACES, ITEMS)
    root_node = TreeNode(root_state)
    found_story = bfs(root_node, goals_satisfied)
    print(found_story.create_story_text())
