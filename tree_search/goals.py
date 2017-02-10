"""
Defining the different goals we are checking for
"""

def possible(state):
    return state.believability > 0

def death_occured(state):
    """
    description: checks if death has occured in the story
    returns a boolean indicating so or not
    """
    for _, actor in state.actors.items():
        if actor["health"] <= 0:
            return True
    return False

GOALS = [
    possible,
    death_occured,
]

def goals_satisfied(state):
    for goal in GOALS:
        if not goal(state):
            return False
    return True
