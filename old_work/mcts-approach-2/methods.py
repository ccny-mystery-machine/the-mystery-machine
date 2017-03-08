"""
Defining possible methods below
methods return a pair, the sentence and its believability
"""

from setup import *
from copy import deepcopy
from random import randint
from functools import partial

def move(actor_name, place_name, state):
    """
    description: actor moves to place
    precondition: place is not actor's current location
    postcondition: actor's current place is set to place
    """
    
    actor = state.actors[actor_name]
    place = state.places[place_name]
    
    if actor["place"] == place["name"]:
        return ("Nonsense sentence.", 0)

    actor["place"] = place
    return (actor["name"] + " went to " + place["name"] + ". ", 1)


def steal(actor_a_name, actor_b_name, state):
    """
    description: actor_a steals an item from actor_b
    precondition: actor_a must be alive, actor_b must
        have items that can be stolen
    postcondition: actor_b loses a random item and actor_a gains it, actor_b
        becomes angrier at actor_a
    """

    actor_a = state.actors[actor_a_name]
    actor_b = state.actors[actor_b_name]

    if actor_a == actor_b:
        return ("Nonsense sentence.", 0)
    
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


def play(actor_a_name, actor_b_name, state):
    """
    description: actor_a plays with actor_b
    precondition: actor_a and actor_b must be alive and in the same location
    postcondition: actor_a and actor_b becomes less angry with eachother
    """

    actor_a = state.actor[actor_a_name]
    actor_b = state.actor[actor.b_name]

    if actor_a == actor_b:
        return ("Nonsense sentence.", 0)

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


def kill(actor_a_name, actor_b_name, state):
    """
    description: actor_a kills actor_b
    precondition: actor_a and actor_b must be alive and in the same location
    postcondition: actor_b's health goes to 0
    """

    actor_a = state.actor[actor_a_name]
    actor_b = state.actor[actor_b_name]

    if actor_a == actor_b:
        return ("Nonsense sentence.", 0)

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
    partial(move, "ALICE", "OUTSIDE"),
    partial(move, "ALICE", "ALICES_HOUSE"),
    partial(move, "ALICE", "BOBS_HOUSE"),
    partial(move, "ALICE", "CHARLIES_HOUSE"),
    partial(move, "BOB", "OUTSIDE"),
    partial(move, "BOB", "ALICES_HOUSE"),
    partial(move, "BOB", "BOBS_HOUSE"),
    partial(move, "BOB", "CHARLIES_HOUSE"),
    partial(move, "CHARLIE", "OUTSIDE"),
    partial(move, "CHARLIE", "ALICES_HOUSE"),
    partial(move, "CHARLIE", "BOBS_HOUSE"),
    partial(move, "CHARLIE", "CHARLIES_HOUSE"),
    
    partial(steal, "ALICE", "ALICE"),
    partial(steal, "ALICE", "BOB"),
    partial(steal, "ALICE", "CHARLIE"),
    partial(steal, "BOB", "ALICE"),
    partial(steal, "BOB", "BOB"),
    partial(steal, "BOB", "CHARLIE"),
    partial(steal, "CHARLIE", "ALICE"),
    partial(steal, "CHARLIE", "BOB"),
    partial(steal, "CHARLIE", "CHARLIE"),

    partial(play, "ALICE", "ALICE"),
    partial(play, "ALICE", "BOB"),
    partial(play, "ALICE", "CHARLIE"),
    partial(play, "BOB", "ALICE"),
    partial(play, "BOB", "BOB"),
    partial(play, "BOB", "CHARLIE"),
    partial(play, "CHARLIE", "ALICE"),
    partial(play, "CHARLIE", "BOB"),
    partial(play, "CHARLIE", "CHARLIE"),

    partial(kill, "ALICE", "ALICE"),
    partial(kill, "ALICE", "BOB"),
    partial(kill, "ALICE", "CHARLIE"),
    partial(kill, "BOB", "ALICE"),
    partial(kill, "BOB", "BOB"),
    partial(kill, "BOB", "CHARLIE"),
    partial(kill, "CHARLIE", "ALICE"),
    partial(kill, "CHARLIE", "BOB"),
    partial(kill, "CHARLIE", "CHARLIE"),

]

class Method:
    """
    Actions in the story - Edges in the tree
    """
    def __init__(self, method):
        self.method = method
    
    def call(self, state):
        self.before_state = state
        self.after_state = deepcopy(state)
        result = self.method(self.afterstate)
        self.humanUnderstandableSentance = result[0]
        self.believability = result[1]

