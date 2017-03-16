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
    places = deepcopy(OUT_PLACES)
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

RELATIONSHIPS = {
    "ENEMY": "enemy",
    "STRANGER": "stranger",
    "FRIENDS": "friends",
    "SIGNIFICANT_OTHER": "significant other",
}

ITEMS = {
    "GUN": {
        "name": "gun",
        "value": 0.5,
        "lethality": 0.9,
        "drop_believability": 0.2,
    },
    "VASE": {
        "name": "vase",
        "value": 0.9,
        "lethality": 0.6,
        "drop_believability": 0.5,
    },
    "BASEBALL_BAT": {
        "name": "baseball bat",
        "value": 0.2,
        "lethality": 0.5,
        "drop_believability": 0.4
    },
    "TREE_BRANCH": {
        "name": "tree branch",
        "value": 0.1,
        "lethality": 0.5,
        "drop_believability": 0.4
    },
    "KNIFE": {
        "name": "knife",
        "value": 0.4,
        "lethality": 0.8,
        "drop_believability": 0.7
    },
    "PEN": {
        "name": "pen",
        "value": 0.1,
        "lethality": 0.5,
        "drop_believability": 0.9,
    },
    "CANDLE": {
        "name": "candle",
        "value": 0.6,
        "lethality": 0.3,
        "drop_believability": 0.8
    },
    "SEASHELL": {
        "name": "seashell",
        "value": 0.2,
        "lethality": 0.4,
        "drop_believability": 0.9
    }
}

OUT_PLACES = {
    "LIBRARY": {
        "name": "library",
        "items": [ITEMS["PEN"], ]
    },
    "STREET": {
        "name": "street",
        "items": [],
    },
    "PARK": {
        "name": "park",
        "items": [ITEMS["TREE_BRANCH"]],
    },
    "STORE": {
        "name": "store",
        "items": [ITEMS["GUN"], ITEMS["KNIFE"]],
    },
    "CHURCH": {
        "name": "church",
        "items": [],
    },
    "BEACH": {
        "name": "beach",
        "items": [],
    },
    "ALLEYWAY": {
        "name": "alleyway",
        "items": [ITEMS["BASEBALL_BAT"]], 
    },
    "WAREHOUSE": {
        "name": "warehouse",
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
        "kill_desire": {},  
        "affection": {}, 
        "attractiveness": 0.5, 
        "grief": 0,
        "gender": "female",
    },
    "BOB": {
        "name": "Bob",
        "home": PLACES["BOBS_HOUSE"],
        "place": PLACES["BOBS_HOUSE"],
        "health": 10,
        "items": [ITEMS["VASE"]],
        "kill_desire": {},
        "affection": {},
        "attractiveness": 0.9,
        "grief": 0,
        "gender": "male",
    },
    "CHARLIE": {
        "name": "Charlie",
        "home": PLACES["CHARLIES_HOUSE"],
        "place": PLACES["CHARLIES_HOUSE"],
        "health": 10,
        "items": [ITEMS["BASEBALL_BAT"]],
        "kill_desire": {},
        "affection": {},
        "attractiveness": 0.3,
        "grief": 0,
        "gender": "male",

    },
}
