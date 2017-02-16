from functools import partial
from copy import deepcopy

from methods import Method, METHODS, POSSIBLE_METHODS


def multiply_ba(newaction_b, story_b):
    story_b = story_b * newaction_b

class Story:
    """
    Story - A path along the tree
    """
    def __init__(self, node):
        """
        Shallow Copy Here
        """
        self.methods_list = []
        
