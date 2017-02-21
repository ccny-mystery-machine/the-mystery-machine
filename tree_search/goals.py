"""
Defining the different goals we are checking for
"""

from functools import partial

def possible(node):
    return node.believability > 0


def death_occured(node):
    """
    description: checks if death has occured in the story
    returns a boolean indicating so or not
    """
    for _, actor in node.state.actors.items():
        if actor["health"] <= 0:
            return True
    return False

def story_length_greater_than(length, node):
    return node.height > length

GOALS = [
    possible,
    death_occured,
    partial(story_length_greater_than, 4)
]


def goals_satisfied(node, goals):
    for goal in goals:
        if not goal(node):
            return False
    return True
