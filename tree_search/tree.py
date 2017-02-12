from methods import Method, METHODS, POSSIBLE_METHODS

class StoryNode:
    """
    Node in our story tree
    """
    def __init__(self, state):
        self.state = state
        self.pre_method = None
        self.children = []

        # stores indices of all possible actions
        self.possible_methods = range(0, len(POSSIBLE_METHODS))

class StoryTree:
    """
    Tree representation of story
    """
    def __init__(self, state):
        self.root = StoryNode(state)

    def expand_child(node):
        """
        Expands another child of the node - in reverse order
        Returns True if successful, False if not
        """
        if node.possible_actions:
            new_action = node.possible_actions.pop()
            node.children.append(new_action())
            return True

        return False

    def expand_all_children(node):
        """
        Expands all possible actions
        """
        if node.possible_actions:
            for _ in range(0, len(node.possible_actions)):
                node.expand_child()
            return True

        return False
