"""
Defining possible methods below
methods return the new state
"""

from random import randint
from copy import deepcopy
from functools import partial

from setup import ACTORS, PLACES, ITEMS


METHOD_CONSTANTS = {
    "MOVE_IF_SAME_PLACE": 0,
    "MOVE_IF_DEAD": 0,
    "MOVE_IF_DIFFERENT_PLACE": 1,
    
    "MUG_IF_DEAD": 0,
    "MUG_IF_YOURSELF": 0,
    "MUG_IF_DIFFERENT_PLACE": 0,
    "MUG_ANGER_INC": 3, 
    "MUG_AFFECTION": -1,   

    "TALK_IF_DEAD": 0,
    "TALK_IF_DIFFERENT_PLACE": 0,
    "TALK_IF_NORMAL": 1,
    "TALK_ANGER_DEC": 5,
    
    "KILL_NOT_ANGRY": 0.1,
    "KILL_ANGER_THRES": 0,
    "KILL_ANGRY": 0.9,
    "KILL_IF_DEAD": 0,
    "KILL_IF_DIFFERENT_PLACE": 0,
    
}


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
        self.sentence = ""
        self.believability = 1

    def __call__(self, state):
        self.prev_state = state
        self.next_state = deepcopy(state)
        self.sentence, self.believability = self.method(self.next_state)


def move(actor_key, place_key, state):
    """
    description: actor moves to place
    actor_key, place_key: string keywords
    precondition: place is not actor's current location
    postcondition: actor's current place is set to place
    """

    actor = state.actors[actor_key]
    place = state.places[place_key]
   
    sentence = actor["name"] + " went to " + place["name"] + ". "

    if (actor["health"] <= 0):
        believability = METHOD_CONSTANTS[ "MOVE_IF_DEAD" ]
        return (sentence, believability)

   
    if (actor["place"]["name"] == place["name"]):
        believability = METHOD_CONSTANTS[ "MOVE_IF_SAME_PLACE" ]
        return (sentence, believability)

    actor["place"] = place

    believability = METHOD_CONSTANTS[ "MOVE_IF_DIFFERENT_PLACE" ]
    return (sentence, believability)


def mug(actor_a_key, actor_b_key, state):
    """
    description: actor_a mugs an item from actor_b
    precondition: actor_a must be alive, actor_b must
        have items that can be stolen
    postcondition: actor_b loses a random item and actor_a gains it, actor_b
        becomes angrier at actor_a
    """

    actor_a = state.actors[actor_a_key]
    actor_b = state.actors[actor_b_key]
 
    if (len(actor_b["items"]) == 0): 
        sentence = "Nonsense Sentence. "
        believability = 0
        return (sentence, believability)

    rand_idx = randint(0, len(actor_b["items"]) - 1)
    actor_b_item = actor_b["items"].pop(rand_idx)
    actor_a["items"].append(actor_b_item)
    if actor_a_key in actor_b["kill_desire"]:
        actor_b["kill_desire"][actor_a_key] += METHOD_CONSTANTS[ "MUG_ANGER_INC" ]
    else:
        actor_b["kill_desire"][actor_a_key] = METHOD_CONSTANTS[ "MUG_ANGER_INC" ]
    
    actor_b["affection"][actor_a_key] = METHOD_CONSTANTS[ "MUG_AFFECTION" ]

    sentence = (actor_a["name"] + " mugs " + actor_b["name"] + " and stole " +
                actor_b_item["name"] + " from " + actor_b["gender"] + )
    
    if (actor_a["health"] <= 0): 
        believability = METHOD_CONSTANTS[ "MUG_IF_DEAD" ]
        return (sentence, believability)
    if (actor_a["name"] == actor_b["name"]): 
        believability = METHOD_CONSTANTS[ "MUG_IF_YOURSELF" ]
        return (sentence, believability)
    if (actor_a["place"] != actor_b["place"]):
        believability = METHOD_CONSTANTS[ "MUG_IF_DIFFERENT_PLACE" ]
        return (sentence, believability)
   
    
    believability = actor_b_item["value"]
    return (sentence, believability)


def talk(actor_a_key, actor_b_key, state):
    """
    description: actor_a talks with actor_b
    precondition: actor_a and actor_b must be alive and in the same location
    postcondition: actor_a and actor_b becomes less angry with eachother
    """

    actor_a = state.actors[actor_a_key]
    actor_b = state.actors[actor_b_key]

    sentence = actor_a["name"] + " talked with " + actor_b["name"] + ". "
    
    if (actor_a["health"] <= 0 or actor_b["health"] <= 0):
        believability = METHOD_CONSTANTS[ "TALK_IF_DEAD" ]
        return (sentence, believability)           

    if actor_b_key in actor_a["anger"]:
        actor_a["anger"][actor_b_key] -= METHOD_CONSTANTS[ "TALK_ANGER_DEC" ]
    else:
        actor_a["anger"][actor_b_key] = -METHOD_CONSTANTS[ "TALK_ANGER_DEC" ]

    if actor_a_key in actor_b["anger"]:
        actor_b["anger"][actor_a_key] -= METHOD_CONSTANTS[ "TALK_ANGER_DEC" ]
    else:
        actor_b["anger"][actor_a_key] = -METHOD_CONSTANTS[ "TALK_ANGER_DEC" ]
    
    if (actor_a["place"] != actor_b["place"]):
        believability = METHOD_CONSTANTS[ "TALK_IF_DIFFERENT_PLACE" ]
        return (sentence, believability)           
    if (actor_a["name"] == actor_b["name"]):
        sentence = "Nonsense sentence. "
        believability = 0
        return (sentence, believability)

    believability = METHOD_CONSTANTS[ "TALK_IF_NORMAL" ]
    return (sentence, believability)


def kill(actor_a_key, actor_b_key, state):
    """
    description: actor_a kills actor_b
    precondition: actor_a and actor_b must be alive and in the same location
                  actor_a must have anger > 0 towards actor_b
    postcondition: actor_b's health goes to 0
    """

    actor_a = state.actors[actor_a_key]
    actor_b = state.actors[actor_b_key]

    sentence = actor_a["name"] + " killed " + actor_b["name"] + ". "
    
    if (actor_a["health"] <= 0 or actor_b["health"] <= 0):
        believability = METHOD_CONSTANTS[ "KILL_IF_DEAD" ]
        return (sentence, believability)

    actor_b["health"] = 0
    
    if (actor_a["place"] != actor_b["place"]):
        believability = METHOD_CONSTANTS[ "KILL_IF_DIFFERENT_PLACE" ] 
        return (sentence, believability)
    if (actor_a["name"] == actor_b["name"]):
        sentence = "Nonsense sentence. "
        believability = 0
        return (sentence, believability)

    # if anger exists, then we have higher believability
    if (actor_b_key in actor_a["anger"] and actor_a["anger"][actor_b_key] > METHOD_CONSTANTS[ "KILL_ANGER_THRES" ]):
        believability = METHOD_CONSTANTS[ "KILL_ANGRY"  ]
        return (sentence, believability)

    # potential of random murder
    believability = METHOD_CONSTANTS[ "KILL_NOT_ANGRY" ]
    return (sentence, believability)

METHODS = {
    "MOVE": move,
    "MUG": mug,
    "TALK": talk,
    "KILL": kill,
}

POSSIBLE_METHODS = []

# MOVE - actor, place
for key_a in ACTORS:
    for key_p in PLACES:
        POSSIBLE_METHODS.append(
            partial(move, key_a, key_p)
        )

# MUG - actor, actor
for key_a in ACTORS:
    for key_b in ACTORS:
        if key_a != key_b:
            POSSIBLE_METHODS.append(
                partial(mug, key_a, key_b)
            )

# TALK - actor, actor
for key_a in ACTORS:
    for key_b in ACTORS:
        if key_a != key_b:
            POSSIBLE_METHODS.append(
                partial(talk, key_a, key_b)
            )

# KILL - actor, actor
for key_a in ACTORS:
    for key_b in ACTORS:
        if key_a != key_b:
            POSSIBLE_METHODS.append(
                partial(kill, key_a, key_b)
            )
