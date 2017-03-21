from functools import partial
from copy import deepcopy

from methods import Method, METHODS


def multiply_ba(newaction_b, story_b):
    return story_b * newaction_b

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
        self.state_list = []
        if len(self.methods_list) > 0:
            self.state_list.append(self.methods_list[0].prev_state)
        self.believability = 1
        for method in self.methods_list:
            self.state_list.append(method.next_state)
            self.believability = multiply_ba(method.believability,
                                             self.believability)

    def __str__(self):
        story_text = ""
        for method in self.methods_list:
            story_text += method.sentence
            story_text += '\n'
        return story_text
