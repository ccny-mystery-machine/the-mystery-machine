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

