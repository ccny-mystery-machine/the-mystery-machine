"""
Setup of the initial actors, places, items
"""
from random import randint
from copy import deepcopy

class State:
    """
    State of the Story - Nodes in the tree
    """
    def __init__(self):
        num_characters = randint(3, 5)
        self.places = deepcopy(OUT_PLACES)
        for _ in range(num_characters):
            ridx = randint(0,4)
            names = NAME_BANK[ridx]
            self.actors[names[0]] = deepcopy(ACTOR_TEMPLATE)
            self.actors[names[0]]["name"] = names[1]
            self.places[names[2]] = { "name": names[3], "items": [], }
            self.actors[names[0]]["home"] = self.places[names[2]]
            self.actors[names[0]]["place"] = self.places[names[2]]
            self.actors[names[0]]["health"] = names[4]
            self.actors[names[0]]["attractiveness"] = names[5]
            self.actors[names[0]]["grief"] = names[6]
        self.items = deepcopy(ITEMS)
        self.places["LIBRARY"]["items"].append(self.items["PEN"]) 
        self.places["STORE"]["items"].append(self.items["GUN"]) 
        self.places["STORE"]["items"].append(self.items["KNIFE"]) 
        self.places["PARK"]["items"].append(self.items["TREE_BRANCH"]) 
        self.places["PARK"]["items"].append(self.items["BASEBALL_BAT"]) 
        self.places["WAREHOUSE"]["items"].append(self.items["VASE"]) 
    
    def __init__(self, actors, places, items):
        self.actors = deepcopy(actors)
        self.places = deepcopy(places)
        self.items = deepcopy(items)


NAME_BANK = [
("ALICE", "female"),
("BOB", "male"),
("CHARLIE", "male"),
("DAPHNE", "female"),
("EVE", "female"),
("FRED", "male"),
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
        "lethality": .1,
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
        "lethality": .4
    },
}

OUT_PLACES = {
    "LIBRARY": {
        "name": "Library",
        "items": [],
    },
    "STREET": {
        "name": "Street",
        "items": [],
    },
    "PARK": {
        "name": "Park",
        "items": [],
    },
    "STORE": {
        "name": "Store",
        "items": [],
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
        "items": [], 
    },
    "WAREHOUSE": {
        "name": "Warehouse",
        "items": [],
    }
}


ACTOR_TEMPLATE: {
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

"""
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
"""
