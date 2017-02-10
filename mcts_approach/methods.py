"""
Defining possible methods below
methods return the new state
"""

from random import randint

def move(state, actor_key, place_key):
    """
    description: actor moves to place
    actor_key, place_key: string keywords
    precondition: place is not actor's current location
    postcondition: actor's current place is set to place
    """
    new_state = state.__class__(state.actors, state.places, state.items,
                          state.story, state.believability)
    actor = new_state.actors[actor_key]
    place = new_state.places[place_key]

    if actor["health"] <= 0:
        new_state.story += "Nonsense sentence. "
        new_state.believability = 0
        return new_state

    if actor["place"]["name"] == place["name"]:
        new_state.story += "Nonsense sentence. "
        new_state.believability = 0
        return new_state

    actor["place"] = place

    sentence = actor["name"] + " went to " + place["name"] + ". "
    new_state.story += sentence
    return new_state


def steal(state, actor_a_key, actor_b_key):
    """
    description: actor_a steals an item from actor_b
    precondition: actor_a must be alive, actor_b must
        have items that can be stolen
    postcondition: actor_b loses a random item and actor_a gains it, actor_b
        becomes angrier at actor_a
    """
    new_state = state.__class__(state.actors, state.places, state.items,
                          state.story, state.believability)
    actor_a = new_state.actors[actor_a_key]
    actor_b = new_state.actors[actor_b_key]

    if actor_a["health"] <= 0:
        new_state.story += "Nonsense sentence. "
        new_state.believability = 0
        return new_state

    if actor_a["place"] != actor_b["place"] or len(actor_b["items"]) == 0:
        new_state.story += "Nonsense sentence. "
        new_state.believability = 0
        return new_state

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
    new_state.story += sentence
    new_state.believability *= actor_b_item["value"]
    return new_state


def play(state, actor_a_key, actor_b_key):
    """
    description: actor_a plays with actor_b
    precondition: actor_a and actor_b must be alive and in the same location
    postcondition: actor_a and actor_b becomes less angry with eachother
    """
    new_state = state.__class__(state.actors, state.places, state.items,
                          state.story, state.believability)
    actor_a = new_state.actors[actor_a_key]
    actor_b = new_state.actors[actor_b_key]

    if (actor_a["place"] != actor_b["place"] or
            actor_a["health"] <= 0 or
            actor_b["health"] <= 0):
        new_state.story += "Nonsense sentence. "
        new_state.believability = 0
        return new_state

    if actor_b_key in actor_a["anger"]:
        actor_a["anger"][actor_b_key] -= 1
    else:
        actor_a["anger"][actor_b_key] = -1

    if actor_a_key in actor_b["anger"]:
        actor_b["anger"][actor_a_key] -= 1
    else:
        actor_b["anger"][actor_a_key] = -1

    sentence = actor_a["name"] + " played with " + actor_b["name"] + ". "
    new_state.story += sentence
    return new_state


def kill(state, actor_a_key, actor_b_key):
    """
    description: actor_a kills actor_b
    precondition: actor_a and actor_b must be alive and in the same location
    postcondition: actor_b's health goes to 0
    """
    new_state = state.__class__(state.actors, state.places, state.items,
                          state.story, state.believability)
    actor_a = new_state.actors[actor_a_key]
    actor_b = new_state.actors[actor_b_key]

    if actor_a["health"] <= 0 or actor_b["health"] <= 0:
        new_state.story += "Nonsense sentence. "
        new_state.believability = 0
        return new_state

    if actor_a["place"] != actor_b["place"]:
        new_state.story += "Nonsense sentence. "
        new_state.believability = 0
        return new_state

    actor_b["health"] = 0
    if actor_b_key in actor_a["anger"]:
        if actor_a["anger"][actor_b_key] <= 0:
            new_state.believability *= 0.1

    sentence = actor_a["name"] + " killed " + actor_b["name"] + ". "
    new_state.story += sentence
    return new_state

METHODS = {
    "MOVE": move,
    "STEAL": steal,
    "PLAY": play,
    "KILL": kill,
}
