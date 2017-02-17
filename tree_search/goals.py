"""
Defining the different goals we are checking for
"""


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


GOALS = [
    possible,
    death_occured,
]


def goals_satisfied(node, goals):
    for goal in goals:
        if not goal(node):
            return False
    return True
