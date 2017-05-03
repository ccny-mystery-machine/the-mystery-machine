"""
Setup of all global variables
"""

NAME_BANK = [
    ("Alice", "female"),
    ("Bob", "male"),
    ("Charlie", "male"),
    ("Daphne", "female"),
    ("Eve", "female"),
    ("Fred", "male"),
]

ITEMS = {
    "GUN": {
        "name": "gun",
        "value": 1,
        "lethality": 1,
        "drop_believability": 0.2,
    },
    "VASE": {
        "name": "vase",
        "value": 1,
        "lethality": 0.6,
        "drop_believability": 0.3,
    },
    "BASEBALL_BAT": {
        "name": "baseball bat",
        "value": 0.3,
        "lethality": 0.7,
        "drop_believability": 0.5
    },
    "TREE_BRANCH": {
        "name": "tree branch",
        "value": 0.2,
        "lethality": 0.5,
        "drop_believability": 0.5
    },
    "KNIFE": {
        "name": "knife",
        "value": 1,
        "lethality": 1,
        "drop_believability": 0.6
    },
    "PEN": {
        "name": "pen",
        "value":0.1 ,
        "lethality": 0.4,
        "drop_believability": 0.9,
    },
    "CANDLE": {
        "name": "candle",
        "value": 0.2,
        "lethality": 0.3,
        "drop_believability": 0.7
    },
    "SEASHELL": {
        "name": "seashell",
        "value": 0.1,
        "lethality": 0.4,
        "drop_believability": 0.9
    }
}

OUT_PLACES = {
    "LIBRARY": {
        "name": "library",
        "items": [ITEMS["PEN"],],
    },
    "PARK": {
        "name": "park",
        "items": [ITEMS["TREE_BRANCH"],],
    },
    "STORE": {
        "name": "store",
        "items": [ITEMS["GUN"], ITEMS["KNIFE"],],
    },
    "ALLEYWAY": {
        "name": "alleyway",
        "items": [ITEMS["BASEBALL_BAT"],], 
    },
    "WAREHOUSE": {
        "name": "warehouse",
        "items": [ITEMS["VASE"],]
    },
}

PLACE_TEMPLATE = {
    "name": None,
    "items": [],
}

ACTOR_TEMPLATE = {
    "name": None,
    "home": None,
    "place": None,
    "health": None,
    "items": [], # Array of items
    "kill_desire": {},  # dictionary of other actors to their kill_desire value
    "gender": None,
}


ACTOR_PLACES = {
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
    "DAPHNES_HOUSE": { 
            "name": "Daphne's house",
            "items": [],
        },
}

PLACES = { **ACTOR_PLACES, **OUT_PLACES }

ACTORS = {
    "ALICE": {
        "name": "Alice",
        "home": PLACES["ALICES_HOUSE"],
        "place": PLACES["ALICES_HOUSE"],
        "health": 1,
        "items": [],
        "kill_desire": {
            "BOB": 0,
            "CHARLIE": 0,
            "DAPHNE": 0,
        },  
        "gender": "female",
    },
    "BOB": {
        "name": "Bob",
        "home": PLACES["BOBS_HOUSE"],
        "place": PLACES["BOBS_HOUSE"],
        "health": 1,
        "items": [],
        "kill_desire": {
            "ALICE": 0,
            "CHARLIE": 0,
            "DAPHNE": 0,
        },  
        "gender": "male",
    },
    "CHARLIE": {
        "name": "Charlie",
        "home": PLACES["CHARLIES_HOUSE"],
        "place": PLACES["CHARLIES_HOUSE"],
        "health": 1,
        "items": [],
        "kill_desire": {
            "ALICE": 0,
            "BOB": 0,
            "DAPHNE": 0,
        },  
        "gender": "male",
    },
    "DAPHNE": {
        "name": "Daphne",
        "home": PLACES["DAPHNES_HOUSE"],
        "place": PLACES["DAPHNES_HOUSE"],
        "health": 1,
        "items": [],
        "kill_desire": {
            "ALICE": 0,
            "BOB": 0,
            "CHARLIE": 0,
        },  
        "gender": "female",
    },
}
