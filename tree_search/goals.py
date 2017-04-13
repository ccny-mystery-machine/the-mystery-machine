"""
Defining the different goals we are checking for
"""

from functools import partial

def possible(node):
    return node.believability > 0


def death_occurred(num_deaths, node):
    """
    description: checks if num_deaths deaths occurred
    returns a boolean indicating so or not
    """
    num_dead = 0
    for _, actor in node.state.actors.items():
        if actor["health"] <= 0:
            num_dead += 1
    return num_dead >= num_deaths

def everyone_dies(node):
    """
    description: checks if everyone died in the story
    returns a boolean indicating so or not
    """
    for _, actor in node.state.actors.items():
        if actor["health"] > 0:
            return False
    return True

GOALS = [
    # possible,
    partial(death_occurred, 1),
    partial(death_occurred, 2),
    partial(death_occurred, 3),
    everyone_dies
]


def goals_satisfied(node, goals):
    for goal in goals:
        if not goal(node):
            return False
    return True

def percent_goals_satisfied(node, goals):
    count = 0
    for goal in goals:
        if goal(node):
            count += 1
    return count / len(goals)

