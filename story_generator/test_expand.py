from setup import ACTORS, PLACES, ITEMS
from state import State
from tree import TreeNode, expand_all_believable_edges


def expand_all_believable_edges_test():
    root_state = State(ACTORS, PLACES, ITEMS)
    root_node = TreeNode(root_state, parent_edge=None, possible_methods=True )
    expand_all_believable_edges(root_node, False)
    for edge in root_node.edges:
        print(edge.method.sentence)
    
if __name__ == "__main__":
    expand_all_believable_edges_test() 
