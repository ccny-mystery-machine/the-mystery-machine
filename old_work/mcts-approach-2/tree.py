"""
Tree Class
"""
from goal import *

class Tree:
    """
    Tree - Itself 

    """
    def __init__(self):
        global METHODS
        self.root = State();
        self.list_of_stories = [];
        self.list_of_stories.append(Story(self.root))
        self.list_of_stories[0].set_believability_accumulator(multiply_ba)
        self.story_index = 0
        self.state_index = 0
    
    def addNode(self, story_index, state_index, method_class):
       new_story = Story(self.list_of_stories[story_index], state_index)
       self.purgeLeaf(new_story[state_index])
       new_story.addMethodandState(method_class)
       self.list_of_stories.append(new_story)

    def purgeLeaf(self, state):
        i = 0
        while (i < len(self.list_of_stories)):
            story = self.list_of_stories[i]
            if (story.current_state == state)
                self.list_of_stories.remove(story)
                i = i - 1

    def purge(self, state, state_index):
        i = 0
        while (i < len(self.list_of_stories)):
            story = self.list_of_stories[i]
            if (len(story.state_list) > state_index):
                if (story[state_index] == state): 
                    self.list_of_stories.remove(story)
                    i = i - 1

    def searchState(self, state):
        i = self.story_index
        j = self.state_index
        while (i > len(self.list_of_stories)):
            while (j > len(self.list_of_stories[i])):
                if (self.list_of_stories[i][j] == state):
                    self.story_index = i
                    self.state_index = j
                    return (i, j)
        return False
