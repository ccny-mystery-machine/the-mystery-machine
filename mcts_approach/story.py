from functools import partial

from methods import METHODS

class StoryNode:
    """
    Node in our story tree
    """
    def __init__(self, actors, places, items, story, believability):
        self.actors = actors
        self.places = places
        self.items = items
        self.believability = believability
        self.story = story
        self.children = []
        self.possible_actions = []

        # MOVE - actor, place
        for key_a in actors:
            for key_p in places:
                self.possible_actions.append(
                    partial(METHODS["MOVE"], self, key_a, key_p)
                )

        # STEAL - actor, actor
        for key_a in actors:
            for key_b in actors:
                self.possible_actions.append(
                    partial(METHODS["STEAL"], self, key_a, key_b)
                )

        # PLAY - actor, actor
        for key_a in actors:
            for key_b in actors:
                self.possible_actions.append(
                    partial(METHODS["PLAY"], self, key_a, key_b)
                )

        # KILL - actor, actor
        for key_a in actors:
            for key_b in actors:
                self.possible_actions.append(
                    partial(METHODS["KILL"], self, key_a, key_b)
                )

    def expand_child(self):
        """
        Expands another child of the node - in reverse order
        Returns True if successful, False if not
        """
        if self.possible_actions:
            new_action = self.possible_actions.pop()
            self.children.append(new_action())
            return True

        return False

    def expand_all_children(self):
        """
        Expands all possible actions
        """
        if self.possible_actions:
            for _ in range(0, len(self.possible_actions)):
                self.expand_child()
            return True

        return False
