"""
Defining the different goals we are checking for
"""

from story import *

def death_occured(story):
    """
    description: checks if death has occured in the story
    returns a boolean indicating so or not
    """
    for actor in story.current_state.actors:
        if actor.health == 0:
            return True
    return False

GOALS = [
    death_occured,
]

