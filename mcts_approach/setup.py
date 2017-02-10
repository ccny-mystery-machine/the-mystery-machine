"""
Setup of the initial actors, places, items
"""
from random import randint
from copy import deepcopy

ITEMS = {
    "GUN": {
        "name": "gun",
        "value": .6,
    },
    "VASE": {
        "name": "vase",
        "value": .9,
    },
    "BASEBALL_BAT": {
        "name": "baseball bat",
        "value": .2,
    },
}

PLACES = {
    "ALICES_HOUSE": {
        "name": "Alice's house",
        "items": [],
    },
    "BOBS_HOUSE": {
        "name": "Bob's house",
        "items": [],
    },
    "CHARLIES_HOUSE": {
        "name": "Charlie's house",
        "items": [],
    },
}

ACTORS = {
    "ALICE": {
        "name": "Alice",
        "home": PLACES["ALICES_HOUSE"],
        "place": PLACES["ALICES_HOUSE"],
        "health": 10,
        "items": [ITEMS["GUN"]],
        "anger": {},  # dictionary of other actors to their anger value
    },
    "BOB": {
        "name": "Bob",
        "home": PLACES["BOBS_HOUSE"],
        "place": PLACES["BOBS_HOUSE"],
        "health": 10,
        "items": [ITEMS["VASE"]],
        "anger": {},
    },
    "CHARLIE": {
        "name": "Charlie",
        "home": PLACES["CHARLIES_HOUSE"],
        "place": PLACES["CHARLIES_HOUSE"],
        "health": 10,
        "items": [ITEMS["BASEBALL_BAT"]],
        "anger": {},
    },
}


"""
Defining the different goals we are checking for
"""


def death_occured(state):
    """
    description: checks if death has occured in the story
    returns a boolean indicating so or not
    """
    for actor in state.actors:
        if actor.health == 0:
            return True
    return False

GOALS = [
    death_occured,
]
