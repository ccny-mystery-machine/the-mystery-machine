from methods import *

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
        self.set_ba = False

    def __init__(self):
        """
        Shallow Copy Here
        """
        self.current_state = State()
        self.state_list = []
        self.methods_list = []
        self.state_list.append(self.current_state)
        self.story_believability = 1
        self.set_ba = False

    def __init__(self, story, state_index):
        self.state_list = story.state_list[0:state_index+1]
        self.methods_list = story.methods_list[0:state_index]
        self.set_ba = story.set_ba
        self.ba = story.ba
        if (self.set_ba == True):
            self.story_believability = 1
            for i in range(state_index)
                self.ba(story.methods_list[i], self.story_believability)
    
    def set_believability_accumulator(self, ba):
        self.ba = ba
        self.set_ba = True

    def addMethodandState(self, method_class):
        """
        Add (Already Initialized)Method and associated next state to lists
        """
        if (self.set_ba == True):
            self.methods_list.append(method_class)
            method_class.call(self.current_state)
            self.current_state = method_class.after_state
            self.state_list.append(self.current_state)
            self.ba(method_class.believability, self.story_believability)
        else:
            print("Set Believability_Accumulator first!")

