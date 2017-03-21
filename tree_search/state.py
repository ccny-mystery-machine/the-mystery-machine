from random import random, randint
from copy import deepcopy

from setup import OUT_PLACES, NAME_BANK, ACTOR_TEMPLATE, PLACE_TEMPLATE, ITEMS, RELATIONSHIPS

class State:
    """
    State of the Story - Nodes in the tree """   
    
    def __init__(self, actors, places, items):
        self.actors = deepcopy(actors)
        self.places = deepcopy(places)
        self.items = deepcopy(items)


def random_state():
    num_characters = randint(3, 5)
    if num_characters > len(NAME_BANK):
        raise IndexError("Number of character exceeds name bank")
    rand_state = State({}, OUT_PLACES, ITEMS)
    seen_idx = []
    for _ in range(num_characters):
        while True:
            ridx = randint(0,len(NAME_BANK)-1)
            if ridx not in seen_idx:
                seen_idx.append(ridx)
                break
        name, gender = NAME_BANK[ridx]
        up_name = name.upper()
        up_place = up_name + "S_HOUSE"

        rand_state.places[up_place] = deepcopy(PLACE_TEMPLATE)
        place = rand_state.places[up_place]
        place["name"] = name + "'s house"
        place["items"] = []

        rand_state.actors[up_name] = deepcopy(ACTOR_TEMPLATE)
        actor = rand_state.actors[up_name]
        places = rand_state.places
        actor["name"] = name
        actor["home"] = places[up_place]
        actor["place"] = places[up_place]
        actor["health"] = 1
        actor["attractiveness"] = random() 
        actor["grief"] = 0


    for source in rand_state.actors:
        for target in rand_state.actors:
            if source == target:
                continue
            rand_state.actors[source]["kill_desire"][target] = 0
            rand_state.actors[source]["affection"][target] = [0, RELATIONSHIPS["STRANGER"]]
                                           
    return rand_state

