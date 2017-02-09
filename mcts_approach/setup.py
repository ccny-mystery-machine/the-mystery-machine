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
    "OUTSIDE": {
        "name": "outside",
        "items": [],
    },
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


class StoryNode:
    """
    Node in our story tree
    """
    def __init__(actors, items, places, sentence, believability):
        this.actors = actors
        this.items = items
        this.places = places
        this.believability = believability
        this.sentence = sentence
        this.children = []
        this.possible_actions = []

        # MOVE - actor, place
        for _, actor in actors.items():
            for _, place in places.items():
                this.possible_actions.append(partial(METHODS["MOVE"], actor, place))

        # STEAL - actor, actor
        for _, actor_a in actors.items():
            for _, actor_b in actors.items():
                this.possible_actions.append(partial(METHODS["STEAL"], actor_a, actor_b))

        # PLAY - actor, actor
        for _, actor_a in actors.items():
            for _, actor_b in actors.items():
                this.possible_actions.append(partial(METHODS["PLAY"], actor_a, actor_b))

        # KILL - actor, actor
        for _, actor_a in actors.items():
            for _, actor_b in actors.items():
                this.possible_actions.append(partial(METHODS["KILL"], actor_a, actor_b))

    def expand_next(self):
        child = new StoryNode()


"""
Defining possible methods below
methods return the new state
"""


def move(actor_key, place_key, state):
    """
    description: actor moves to place
    actor_key, place_key: string keywords
    precondition: place is not actor's current location
    postcondition: actor's current place is set to place
    """
    new_state = deepcopy(state)
    actor = new_state.actors[actor_key]
    place = new_state.places[place_key]
    if actor["place"] == place["name"]:
        return ("Nonsense sentence.", 0)

    actor["place"] = place
    return (actor["name"] + " went to " + place["name"] + ". ", 1)


def steal(actor_a, actor_b):
    """
    description: actor_a steals an item from actor_b
    precondition: actor_a must be alive, actor_b must
        have items that can be stolen
    postcondition: actor_b loses a random item and actor_a gains it, actor_b
        becomes angrier at actor_a
    """

    if actor_a["health"] <= 0:
        return ("Nonsense sentence.", 0)

    if actor_a["place"] != actor_b["place"] or len(actor_b["items"]) == 0:
        return ("Nonsense sentence.", 0)

    rand_idx = randint(0, len(actor_b["items"]) - 1)
    actor_b_item = actor_b["items"].pop(rand_idx)
    actor_a["items"].append(actor_b_item)

    actor_b_name = actor_b["name"]
    if actor_b_name in actor_a["anger"]:
        actor_a["anger"][actor_b_name] += 1
    else:
        actor_a["anger"][actor_b_name] = 1
    sentence = (actor_a["name"] + " stole " + actor_b_item["name"] + " from " +
                actor_b["name"] + ". ")
    return (sentence, actor_b_item["value"])


def play(actor_a, actor_b):
    """
    description: actor_a plays with actor_b
    precondition: actor_a and actor_b must be alive and in the same location
    postcondition: actor_a and actor_b becomes less angry with eachother
    """

    if (actor_a["place"] != actor_b["place"] or
            actor_a["health"] <= 0 or
            actor_b["health"] <= 0):
        return ("Nonsense sentence.", 0)

    actor_a_name = actor_a["name"]
    actor_b_name = actor_b["name"]

    if actor_b_name in actor_a["anger"]:
        actor_a["anger"][actor_b_name] -= 1
    else:
        actor_a["anger"][actor_b_name] = -1

    if actor_a_name in actor_b["anger"]:
        actor_b["anger"][actor_a_name] -= 1
    else:
        actor_b["anger"][actor_a_name] = -1

    return (actor_a_name + " plays with " + actor_b_name + ". ", 1)


def kill(actor_a, actor_b):
    """
    description: actor_a kills actor_b
    precondition: actor_a and actor_b must be alive and in the same location
    postcondition: actor_b's health goes to 0
    """
    if actor_a["place"] != actor_b["place"]:
        return ("Nonsense sentence.", 0)

    actor_b["health"] = 0
    actor_b_name = actor_b["name"]
    believability = 0.1
    if actor_b_name in actor_a["anger"]:
        if actor_a["anger"][actor_b_name] > 0:
            believability = 1.0
    return (actor_a["name"] + " killed " + actor_b["name"] + ". ",
            believability)

METHODS = {
    "MOVE": move,
    "STEAL": steal,
    "PLAY": play,
    "KILL": kill,
}


print(ACTORS)
print(ITEMS)
print(PLACES)
