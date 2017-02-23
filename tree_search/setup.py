"""
Setup of the initial actors, places, items
"""

from copy import deepcopy

class State:
    """
    State of the Story - Nodes in the tree
    """

    def __init__(self, actors, places, items):
        self.actors = deepcopy(actors)
        self.places = deepcopy(places)
        self.items = deepcopy(items)


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
