"""
Setup of the initial actors, places, items
"""
from random import randint
from functools import partial

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

ACTORS = [
    {
        "name": "Alice",
        "home": PLACES["ALICES_HOUSE"],
        "place": PLACES["ALICES_HOUSE"],
        "health": 10,
        "items": [ITEMS["GUN"]],
        "anger": {},  # dictionary of other actors to their anger value
    },
    {
        "name": "Bob",
        "home": PLACES["BOBS_HOUSE"],
        "place": PLACES["BOBS_HOUSE"],
        "health": 10,
        "items": [ITEMS["VASE"]],
        "anger": {},
    },
    {
        "name": "Charlie",
        "home": PLACES["CHARLIES_HOUSE"],
        "place": PLACES["CHARLIES_HOUSE"],
        "health": 10,
        "items": [ITEMS["BASEBALL_BAT"]],
        "anger": {},
    },
]

"""
Defining the different goals we are checking for
"""


def death_occured(state):
    """
    description: checks if death has occured in the story
    returns a boolean indicating so or not
    """
    for actor in state["actors"]:
        if actor["health"] == 0:
            return True
    return False

GOALS = [
    death_occured,
]


"""
Defining possible methods below
methods return a pair, the sentence and its believability
"""


def move(actor, place):
    """
    description: actor moves to place
    precondition: place is not actor's current location
    postcondition: actor's current place is set to place
    """

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

METHODS = [
    move,
    steal,
    play,
    kill,
]


print(ACTORS)
print(ITEMS)
print(PLACES)
print(METHODS)
