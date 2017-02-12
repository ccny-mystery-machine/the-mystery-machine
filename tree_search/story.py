from functools import partial
from copy import deepcopy

from methods import Method, METHODS, POSSIBLE_METHODS


def multiply_ba(newaction_b, story_b):
    story_b = story_b * newaction_b

class Story:
    """
    Story - A path along the tree
    """
    def __init__(self, state):
        """
        Shallow Copy Here
        """
        self.current_state = state
        self.state_list = []
        self.methods_list = []
        self.state_list.append(self.current_state)
        self.story_believability = 1

    def set_believability_accumulator(self, ba):
        self.ba = ba

    def addMethodandState(self, method_class):
        """
        Add (Already Initialized)Method and associated next state to lists
        """
        self.methods_list.append(method_class)
        method_class.call(self.current_state)
        self.current_state = method_class.after_state
        self.state_list.append(self.current_state)
        self.ba(method_class.believability, self.story_believability)
