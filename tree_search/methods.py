"""
Defining possible methods below
methods return the new state
"""

from random import randint
from copy import deepcopy
from functools import partial

from setup import ACTORS, PLACES, ITEMS


class Method:
    """
    Actions in the story - Edges in the tree
    """
    def __init__(self, method):
        self.method = method
        self.function = method.func
        self.args = method.args
        self.before_state = None
        self.after_state = None
        self.sentence = None
        self.believability = None

    def __call__(self, state):
        self.before_state = state
        self.after_state = deepcopy(state)
        self.sentence, self.believability = self.method(self.after_state)


def move(actor_key, place_key, state):
    """
    description: actor moves to place
    actor_key, place_key: string keywords
    precondition: place is not actor's current location
    postcondition: actor's current place is set to place
    """

    actor = state.ACTORS[actor_key]
    place = state.PLACES[place_key]

    if (actor["health"] <= 0 or
            actor["place"]["name"] == place["name"]):
        sentence = "Nonsense sentence. "
        believability = 0
        return (sentence, believability)

    actor["place"] = place

    sentence = actor["name"] + " went to " + place["name"] + ". "
    believability = 1
    return (sentence, believability)


def steal(actor_a_key, actor_b_key, state):
    """
    description: actor_a steals an item from actor_b
    precondition: actor_a must be alive, actor_b must
        have items that can be stolen
    postcondition: actor_b loses a random item and actor_a gains it, actor_b
        becomes angrier at actor_a
    """

    actor_a = state.ACTORS[actor_a_key]
    actor_b = state.ACTORS[actor_b_key]

    if (actor_a["health"] <= 0 or
            actor_a["name"] == actor_b["name"] or
            actor_a["place"] != actor_b["place"] or
            len(actor_b["items"]) == 0):
        sentence = "Nonsense sentence. "
        believability = 0
        return (sentence, believability)

    rand_idx = randint(0, len(actor_b["items"]) - 1)
    actor_b_item = actor_b["items"].pop(rand_idx)
    actor_a["items"].append(actor_b_item)

    if actor_b["name"] in actor_a["anger"]:
        actor_b["anger"][actor_a_key] += 3
    else:
        actor_b["anger"][actor_a_key] = 3

    sentence = (actor_a["name"] + " stole " + actor_b_item["name"] + " from " +
                actor_b["name"] + ". ")
    believability = actor_b_item["value"]
    return (sentence, believability)


def play(actor_a_key, actor_b_key, state):
    """
    description: actor_a plays with actor_b
    precondition: actor_a and actor_b must be alive and in the same location
    postcondition: actor_a and actor_b becomes less angry with eachother
    """

    actor_a = state.ACTORS[actor_a_key]
    actor_b = state.ACTORS[actor_b_key]

    if (actor_a["place"] != actor_b["place"] or
            actor_a["health"] <= 0 or
            actor_b["health"] <= 0 or
            actor_a["name"] == actor_b["name"]):
        sentence = "Nonsense sentence. "
        believability = 0
        return (sentence, believability)

    if actor_b_key in actor_a["anger"]:
        actor_a["anger"][actor_b_key] -= 1
    else:
        actor_a["anger"][actor_b_key] = -1

    if actor_a_key in actor_b["anger"]:
        actor_b["anger"][actor_a_key] -= 1
    else:
        actor_b["anger"][actor_a_key] = -1

    sentence = actor_a["name"] + " played with " + actor_b["name"] + ". "
    believability = 1
    return (sentence, believability)


def kill(actor_a_key, actor_b_key, state):
    """
    description: actor_a kills actor_b
    precondition: actor_a and actor_b must be alive and in the same location
    postcondition: actor_b's health goes to 0
    """

    actor_a = state.ACTORS[actor_a_key]
    actor_b = state.ACTORS[actor_b_key]

    if (actor_a["health"] <= 0 or
            actor_b["health"] <= 0 or
            actor_a["place"] != actor_b["place"] or
            actor_a["name"] == actor_b["name"]):
        sentence = "Nonsense sentence. "
        believability = 0
        return (sentence, believability)

    actor_b["health"] = 0
    # if anger exists, then we have higher believability
    if actor_b_key in actor_a["anger"] and actor_a["anger"][actor_b_key] > 0:
        sentence = actor_a["name"] + " killed " + actor_b["name"] + ". "
        believability = 1
        return (sentence, believability)

    # potential of random murder
    sentence = actor_a["name"] + " killed " + actor_b["name"] + ". "
    believability = 0
    return (sentence, believability)

METHODS = {
    "MOVE": move,
    "STEAL": steal,
    "PLAY": play,
    "KILL": kill,
}

POSSIBLE_METHODS = []

# MOVE - actor, place
for key_a in ACTORS:
    for key_p in PLACES:
        POSSIBLE_METHODS.append(
            partial(move, key_a, key_p)
        )

# STEAL - actor, actor
for key_a in ACTORS:
    for key_b in ACTORS:
        if key_a != key_b:
            POSSIBLE_METHODS.append(
                partial(steal, key_a, key_b)
            )

# PLAY - actor, actor
for key_a in ACTORS:
    for key_b in ACTORS:
        if key_a != key_b:
            POSSIBLE_METHODS.append(
                partial(play, key_a, key_b)
            )

# KILL - actor, actor
for key_a in ACTORS:
    for key_b in ACTORS:
        if key_a != key_b:
            POSSIBLE_METHODS.append(
                partial(kill, key_a, key_b)
            )
