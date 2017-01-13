"""
Setup of the initial actors, places, items, and actions that can be performed
"""
from random import randint

ACTORS = [
    {
        "name" : "Alice",
        "place": "Alice's house",
        "health": 10,
        "items": [],
        "anger": {}, # dictionary of other actors to their anger value
    },
    {
        "name": "Bob",
        "place": "Bob's house",
        "health": 10,
        "items": [],
        "anger": {},
    },
    {
        "name": "Charlie",
        "place": "Charlie's house",
        "health": 10,
        "items": [],
        "anger": {},
    },
]

ITEMS = [
    {
        "name": "gun",
        "value": .6
    },
    {
        "name": "vase",
        "value": .9,
    },
    {
        "name": "baseball bat",
        "value": .2,
    },
]

PLACES = [
    {
        "name": "outside",
    },
    {
        "name": "Alice's house",
    },
    {
        "name": "Bob's house",
    },
    {
        "name": "Charlie's house",
    },
]

# Defining possible methods
# methods return a pair, the sentence and its believability
def move(actor, place):
    """
    description: actor moves to place
    precondition: place is not actor's current location
    postcondition: actor's current place is set to place
    """

    if actor["place"] == place["name"]:
        return False

    actor["place"] = place
    return (actor["name"] + " went to " + place + ". ", 1)

def steal(actor_a, actor_b):
    """
    description: actor_a steals an item from actor_b
    precondition: actor_a must be alive and in actor_b's home, actor_b must have
        items that can be stolen
    postcondition: actor_b loses a random item and actor_a gains it, actor_b
        becomes angrier at actor_a
    """

    if actor_a["health"] <= 0:
        return False

    b_house = actor_b + "'s house"
    if actor_a["place"] != b_house or len(actor_b["items"]) == 0:
        return False

    actor_b_item = actor_b["items"].pop(randint(0, len(actor_b["items"])))
    actor_a["items"].append(actor_b["item"])

    actor_b_name = actor_b["name"]
    if actor_b_name in actor_a["anger"]:
        actor_a["anger"][actor_b_name] += 1
    else:
        actor_a["anger"][actor_b_name] = 1
    sentence = (actor_a["name"] + " stole " + actor_b_item["name"] + " from "
                + actor_b["name"] + ". ")
    return (sentence, actor_b_item["value"])

def play(actor_a, actor_b):
    """
    description: actor_a plays with actor_b
    precondition: actor_a and actor_b must be alive and in the same location
    postcondition: actor_a and actor_b becomes less angry with eachother
    """

    if actor_a["place"] != actor_b["place"] or actor_a["health"] <= 0 or actor_b["health"] <= 0:
        return False

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
    return (actor_a["name"] + " plays with " + actor_b["name"] + ". ", 1)

def kill(actor_a, actor_b):
    """
    description: actor_a kills actor_b
    precondition: actor_a and actor_b must be alive and in the same location
    postcondition: actor_b's health goes to 0
    """
    if actor_a["place"] != actor_b["place"]:
        return False

    actor_b["health"] = 0
    actor_b_name = actor_b["name"]
    if actor_b_name in actor_a["anger"]:
        if actor_a["anger"][actor_b_name] > 0:
            believability = 1.0
        else:
            believability = 0.1
    return (actor_a["name"] + " killed " + actor_b["name"] + ". ", believability)

print(ACTORS)
print(ITEMS)
print(PLACES)
