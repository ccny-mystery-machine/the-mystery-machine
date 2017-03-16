"""
Defining possible methods below
methods return the new state
"""

from random import randint
from copy import deepcopy
from functools import partial

from setup import ACTORS, PLACES, ITEMS, RELATIONSHIPS

def rectadd(a, b):
    ans = a+b
    if ans > 1:
        return 1
    elif ans < -1:
        return -1
    else:
        return ans

METHOD_CONSTANTS = {
    "MOVE_IF_SAME_PLACE": 0,
    "MOVE_IF_DEAD": 0,
    "MOVE_IF_DIFFERENT_PLACE": 1,
    
    "MUG_IF_DEAD": 0,
    "MUG_IF_YOURSELF": 0,
    "MUG_IF_DIFFERENT_PLACE": 0,
    "MUG_KILL_DESIRE_INC": 0.15, 
    "MUG_AFFECTION": -1,   

    "TALK_IF_DEAD": 0,
    "TALK_IF_DIFFERENT_PLACE": 0,
    "TALK_IF_NORMAL": 1,
    "TALK_KILL_DESIRE_DEC": .05,
    "TALK_AFFECTION_INC": 0.05,   

    "KILL_NOT_ANGRY_BELIEVABILITY": 0.1,
    "KILL_DESIRE_THRES": 0,
    "KILL_ANGRY_BELIEVABILITY": 0.9,
    "KILL_IF_DEAD": 0,
    "KILL_IF_DIFFERENT_PLACE": 0,
    
    "BEFRIEND_MIN_THRES": 0,
    "BEFRIEND_MAX_THRES": 0.5,
        
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
        actor_b["kill_desire"][actor_a_key] = rectadd( actor_b["kill_desire"][actor_a_key],  METHOD_CONSTANTS[ "MUG_KILL_DESIRE_INC" ] )
    else:
        actor_b["kill_desire"][actor_a_key] = METHOD_CONSTANTS[ "MUG_KILL_DESIRE_INC" ]
   
    if actor_a_key in actor_b["affection"]:
        actor_b["affection"][actor_a_key][0] = METHOD_CONSTANTS[ "MUG_AFFECTION" ]
    else:
        actor_b["affection"][actor_a_key] = ( METHOD_CONSTANTS[ "MUG_AFFECTION" ], RELATIONSHIPS[ "STRANGER" ] )

    actor_b["grief"] = rectadd( actor_b["grief"], actor_b_item["value"] / 2 )

    actor_b["grief"] = rectadd( actor_b["grief"], actor_b_item["value"] / 2 )

    sentence = (actor_a["name"] + " mugs " + actor_b["name"] + " and stole " +
                actor_b_item["name"] + ". ")
    
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

    if actor_b_key in actor_a["kill_desire"]:
        actor_a["kill_desire"][actor_b_key] = rectadd( actor_a["kill_desire"][actor_b_key], -METHOD_CONSTANTS[ "TALK_KILL_DESIRE_DEC" ] )
    else:
        actor_a["kill_desire"][actor_b_key] = -METHOD_CONSTANTS[ "TALK_KILL_DESIRE_DEC" ]

    if actor_a_key in actor_b["kill_desire"]:
        actor_b["kill_desire"][actor_a_key] = rectadd( actor_b["kill_desire"][actor_a_key], -METHOD_CONSTANTS[ "TALK_KILL_DESIRE_DEC" ] )
    else:
        actor_b["kill_desire"][actor_a_key] = -METHOD_CONSTANTS[ "TALK_KILL_DESIRE_DEC" ]
    
    if actor_b_key in actor_a["affection"]:
        actor_a["affection"][actor_b_key][0] = rectadd( actor_a["affection"][actor_b_key], -METHOD_CONSTANTS[ "TALK_AFFECTION_INC" ] )
    else:
        actor_a["affection"][actor_b_key] = (METHOD_CONSTANTS[ "TALK_AFFECTION_INC" ], RELATIONSHIPS[ "STRANGER" ])  

    if actor_a_key in actor_b["affection"]:
        actor_b["affection"][actor_a_key][0] = rectadd( actor_b["affection"][actor_a_key], -METHOD_CONSTANTS[ "TALK_AFFECTION_INC" ] )
    else:
        actor_b["affection"][actor_a_key] = METHOD_CONSTANTS[ "TALK_AFFECTION_INC" ], RELATIONSHIPS[ "STRANGER" ]) 
    

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
                  actor_a must have kill_desire > 0 towards actor_b
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
        return (sentence, believability)

    # if kill_desire exists, then we have higher believability
    if (actor_b_key in actor_a["kill_desire"] and actor_a["kill_desire"][actor_b_key] > METHOD_CONSTANTS[ "KILL_DESIRE_THRES" ]):
        believability = METHOD_CONSTANTS[ "KILL_ANGRY_BELIEVABILITY"  ]
        return (sentence, believability)

    # potential of random murder
    believability = METHOD_CONSTANTS[ "KILL_NOT_ANGRY_BELIEVABILITY" ]
    return (sentence, believability)


def drop_item(actor_a_key, state):

    actor_a = state.actors[actor_a_key]

    if (len(actor_a["items"]) <= 0):
        sentence = "Nonsense sentence. "
        believability = 0
        return (sentence, believability)

    rand_idx = randint(0, len(actor_a["items"]) - 1)
    actor_a_item = actor_a["items"].pop(rand_idx)
    actor_a["place"]["items"].append(actor_a_item)

    sentence = actor_a["name"] + " dropped " + actor_a_item["name"] + " at " + actor_a["place"]["name"] + ". "
    
    if (actor_a["health"] <= 0):
        believability = 0
        return (sentence, believability)
    
    believability = actor_a_item["drop_believability"]
    return (sentence, believability)
    
def pickup_item(actor_a_key, state):

    actor_a = state.actors[actor_a_key]
    
    if (len(actor_a["place"]["items"]) <= 0):
        sentence = "Nonsense sentence. "
        believability = 0
        return (sentence, believability)
 
    rand_idx = randint(0, len(actor_a["place"]["items"]) - 1)
    place_item = actor_a["place"]["items"].pop(rand_idx)
    actor_a["items"].append(place_item)

    sentence = actor_a["name"] + " picked up " + place_item["name"] + " from " + actor_a["place"]["name"] + ". "
    
    if (actor_a["health"] <= 0):
        believability = 0
        return (sentence, believability)
    
    believability = rectadd(place_item["value"], place_item["lethality"]) 
    return (sentence, believability)


def befriend(actor_a_key, actor_b_key, state):

    actor_a = state.actors[actor_a_key]
    actor_b = state.actors[actor_b_key]

    sentence = actor_a["name"] + " and " + actor_b["name"] +  " became friends. "  
    
    if (actor_a["health"] <= 0 or actor_b["health"] <= 0):
        believability = 0
        return (sentence, believability)
    

    a_b_stranger_or_enemy = actor_a["affection"][actor_b_key][1] == RELATIONSHIP[ "STRANGER" ] or actor_a["affection"][actor_b_key][1] == RELATIONSHIP[ "ENEMY" ]
    b_a_stranger_or_enemy = actor_b["affection"][actor_a_key][1] == RELATIONSHIP[ "STRANGER" ] or actor_b["affection"][actor_a_key][1] == RELATIONSHIP[ "ENEMY" ]

    affection_above_max_thres = (actor_a["affection"][actor_b_key][0] > METHOD_CONSTANTS[ "BEFRIEND_MAX_THRES"] and 
                                 actor_b["affection"][actor_a_key][0] > METHOD_CONSTANTS[ "BEFRIEND_MAX_THRES"]) 

    affection_above_min_thres = (actor_a["affection"][actor_b_key][0] > METHOD_CONSTANTS[ "BEFRIEND_MIN_THRES"] and 
                                 actor_b["affection"][actor_a_key][0] > METHOD_CONSTANTS[ "BEFRIEND_MIN_THRES"]) 

    rng =  METHOD_CONSTANTS[ "BEFRIEND_MAX_THRES"] - METHOD_CONSTANTS[ "BEFRIEND_MIN_THRES"]  
    scaled_affection = (actor_a["affection"][actor_b_key][0] + actor_b["affection"][actor_a_key][0]) / (2 * rng)  


    if (a_b_stranger_or_enemy and b_a_stranger_or_enemy):
        
        if (affection_above_max_thres):
            believability = 1
            return (sentence, believability)
    
        if (affection_above_min_thres):
            believability = scaled_affection
            return (sentence, believability)

    return (sentence, 0)


METHODS = {
    "MOVE": move,
    "MUG": mug,
    "TALK": talk,
    "KILL": kill,
    "DROP_ITEM": drop_item,
    "PICKUP_ITEM": pickup_item,
    "BEFRIEND": befriend
}

POSSIBLE_METHODS = []

    
def create_possible_methods(state)

    # MOVE - actor, place
    for key_a in state.actors:
        for key_p in state.places:
            POSSIBLE_METHODS.append(
                partial(move, key_a, key_p)
            )

    # MUG - actor, actor
    for key_a in state.actors:
        for key_b in state.actors:
            if key_a != key_b:
                POSSIBLE_METHODS.append(
                    partial(mug, key_a, key_b)
                )

    # TALK - actor, actor
    for key_a in state.actors:
        for key_b in state.actors:
            if key_a != key_b:
                POSSIBLE_METHODS.append(
                    partial(talk, key_a, key_b)
                )

    # KILL - actor, actor
    for key_a in state.actors:
        for key_b in state.actors:
            if key_a != key_b:
                POSSIBLE_METHODS.append(
                    partial(kill, key_a, key_b)
            )

    # DROP_ITEM - actor
    for key_a in state.actors:
        POSSIBLE_METHODS.append(
            partial(drop_item, key_a)
        )

    # PICKUP_ITEM - actor
    for key_a in state.actors:
        POSSIBLE_METHODS.append(
            partial(pickup_item, key_a)
        )

    # BEFRIEND - actor, actor
    for key_a in state.actors:
        for key_b in state.actors:
            if key_a != key_b:
                POSSIBLE_METHODS.append(
                    partial(befriend, key_a, key_b)
            )
