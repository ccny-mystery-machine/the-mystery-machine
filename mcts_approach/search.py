"""
Implementation of various search methods for story generation
"""

from copy import deepcopy

from setup import ACTORS, ITEMS, PLACES, METHODS, GOALS


class StoryNode:
    """
    Node in our story tree
    """
    def __init__(actors, items, places, believability, story):
        this.actors = actors
        this.items = items
        this.places = places
        this.believability = believability
        this.story = story
        this.children = []
        this.possible_actions = []

        # MOVE - actor, place
        for key_actor, actor in actors.items():
            for key_place, place in places.items():
                this.possible_actions.append((METHODS["MOVE"], key_actor, key_place))

        # STEAL - actor, actor
        for key_a, actor_a in actors.items():
            for key_b, actor_b in actors.items():
                this.possible_actions.append((METHODS["STEAL"], key_a, key_b))

        # PLAY - actor, actor
        for key_a, actor_a in actors.items():
            for key_b, actor_b in actors.items():
                this.possible_actions.append((METHODS["PLAY"], key_a, key_b))

        # KILL - actor, actor
        for key_a, actor_a in actors.items():
            for key_b, actor_b in actors.items():
                this.possible_actions.append((METHODS["KILL"], key_a, key_b))

    def expand_next(self):
        actors = deepcopy(this.actors)
        items = deepcopy(this.actors)
        places = deepcopy(this.places)

        action_tuple = this.possible_actions.pop()
        action = action_tuple[0]
        action_args = []

        child = StoryNode()
