"""
Setup of the initial actors, places, items
"""
from random import random, randint
from copy import deepcopy

class State:
    """
    State of the Story - Nodes in the tree
    """   
    
    def __init__(self, actors, places, items):
        self.actors = deepcopy(actors)
        self.places = deepcopy(places)
        self.items = deepcopy(items)


def random_state(NAME_BANK):
    num_characters = randint(3, 5)
    places = deepcopy(PLACES)
    actors = {}
    for _ in range(num_characters):
        ridx = randint(0,len(NAME_BANK)-1)
        name, gender = NAME_BANK[ridx]
        up_name = name.upper()
        up_place = up_name + "S_HOUSE"
        place = name + "'s house"
        actors[up_name] = deepcopy(ACTOR_TEMPLATE)
        actor = actor[up_name]
        actor["name"] = name
        places[up_place] = { "name": place, "items": [], }
        actor["home"] = places[up_place]
        actor["place"] = places[up_place]
        actor["health"] = 1
        actor["attractiveness"] = random() 
        actor["grief"] = 0
    items = ITEMS
    return State(actors, places, items)

NAME_BANK = [
("Alice", "female"),
("Bob", "male"),
("Charlie", "male"),
("Daphne", "female"),
("Eve", "female"),
("Fred", "male"),
]

#NAME_BANK = [
    # NAME, name, HOUSE_NAME, house name, health, attractiveness, grief, gender
    #("ALICE", "Alice", "ALICES_HOUSE", "Alice's house", 1, .5, 0, "her" ),
    #("BOB", "Bob", "BOBS_HOUSE", "Bob's house", 1, .3, 0, "him"),
    #("CASSANDRA", "Cassandra", "CASSANDRA_HOUSE", "Cassandra's house", 1, .4, 0, "her"),
    #("DAVID", "David", "DAVIDS_HOUSE", "David's house", 1, .7, 0, "him"),
    #("ED", "Ed", "EDS_HOUSE", "Ed's house", 1, .1, 0, "him"),
#]

ITEMS = {
    "GUN": {
        "name": "gun",
        "value": .5,
        "lethality": .9,
    },
    "VASE": {
        "name": "vase",
        "value": .9,
        "lethality": .6,
    },
    "BASEBALL_BAT": {
        "name": "baseball bat",
        "value": .2,
        "lethality": .5,
    },
    "TREE_BRANCH": {
        "name": "tree branch",
        "value": .1,
        "lethality": .5,
    },
    "KNIFE": {
        "name": "knife",
        "value": .4,
        "lethality": .8,
    },
    "PEN": {
        "name": "pen",
        "value": .1,
        "lethality": .6
    },
    "CANDLE": {
        "name": "candle",
        "value": .6
        "lethality": .3
    },
    "SEASHELL": {
        "name": "seashell"
        "value": .2
        "lethality": .4
    }
}

PLACES = {
    "LIBRARY": {
        "name": "Library",
        "items": [ITEMS["PEN"], ]
    },
    "STREET": {
        "name": "Street",
        "items": [],
    },
    "PARK": {
        "name": "Park",
        "items": [ITEMS["TREE_BRANCH"]],
    },
    "STORE": {
        "name": "Store",
        "items": [ITEMS["GUN"], ITEMS["KNIFE"]],
    },
    "CHURCH": {
        "name": "Church",
        "items": [],
    },
    "BEACH": {
        "name": "Beach",
        "items": [],
    },
    "ALLEYWAY": {
        "name": "Alleyway",
        "items": [ITEMS["BASEBALL_BAT"]], 
    },
    "WAREHOUSE": {
        "name": "Warehouse",
        "items": [ITEMS["VASE"],]
    }
}


ACTOR_TEMPLATE = {
    "name": None,
    "home": None,
    "place": None,
    "health": None,
    "items": [], # Array of items
    "kill_desire": {},  # dictionary of other actors to their kill_desire value
    "affection": {}, # dictionary of other actors to affection value, and relationship value
    "attractiveness": None, # 
    "grief": None,
    "gender": None,
}


ACTORS = {
    "ALICE": {
        "name": "Alice",
        "home": PLACES["ALICES_HOUSE"],
        "place": PLACES["ALICES_HOUSE"],
        "health": 10,
        "items": [ITEMS["GUN"]],
        "anger": {},  # dictionary of other actors to their anger value
        "affection": {}, # dictionary of other actors to affection value, and relationship value
        "attractiveness": 3, # 
        "grief": 0,
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
