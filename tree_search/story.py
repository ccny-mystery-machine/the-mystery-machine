from functools import partial
from copy import deepcopy

from methods import Method, METHODS, POSSIBLE_METHODS


def multiply_ba(newaction_b, story_b):
    story_b = story_b * newaction_b

class Story:
    """
    Story - A path along the tree
    """
    def __init__(self, final_node):
        """
        Shallow Copy Here
        """
        self.methods_list = []
        curr_edge = final_node.parent_edge
        while curr_edge:
            self.methods_list.append(curr_edge.method)
            curr_edge = curr_edge.prev_node.parent_edge
        self.methods_list.reverse()

    def create_story_text(self):
        story_text = ""
        for method in self.methods_list:
            story_text += method.sentence
        return story_text
