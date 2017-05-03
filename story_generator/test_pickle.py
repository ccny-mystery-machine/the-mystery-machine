import pickle;
from state import State
from setup import ACTORS, PLACES, ITEMS
from tree import TreeNode, expand_edge, expand_rand_edge
import os

def pickle_test_1():
    root_state = State(ACTORS, PLACES, ITEMS)
    root_node = TreeNode(root_state, None, True)
    child_node = expand_edge(root_node).next_node
    with open("tree-root.p", "wb") as rootfile:
        pickle.dump(root_node, rootfile, protocol = pickle.HIGHEST_PROTOCOL)
    with open("tree-root.p", "rb") as rootfile:
        pickled_root_node = pickle.load(rootfile)
    os.remove("tree-root.p")
    print(root_node.edges[0].method.sentence)
    print(pickled_root_node.edges[0].method.sentence)

def pickle_test_2():
    root_state = State(ACTORS, PLACES, ITEMS)
    root_node = TreeNode(root_state, None, True)
    child_node = expand_edge(root_node).next_node
    with open("tree-child.p", "wb") as childfile:
        pickle.dump(child_node, childfile, protocol = pickle.HIGHEST_PROTOCOL)
    with open("tree-child.p", "rb") as childfile:
        pickled_child_node = pickle.load(childfile)
    os.remove("tree-child.p")
    print(child_node.parent_edge.prev_node.edges[0].method.sentence)
    print(pickled_child_node.parent_edge.prev_node.edges[0].method.sentence)


def pickle_tree_test(resume=True):
    root_state = State(ACTORS, PLACES, ITEMS)
    root_node = TreeNode(state=root_state, parent_edge=None, possible_methods=True)
    if resume:
        with open("tree.pickle", "rb") as treefile:
            root_node = pickle.load(treefile)
    current_node = root_node
    depth = 0
    counter = 0
    while True:
        if depth >= 15:
            depth = 0
            current_node = root_node
            counter += 1
            if counter % 10 == 0:
                print("Counter - " + str(counter) + " - Dumping To File")
                with open("tree.pickle", "wb") as treefile:
                    pickle.dump(root_node, treefile, protocol=pickle.HIGHEST_PROTOCOL)         
            continue
        edge = expand_rand_edge(current_node)
        if not edge:
            edge = current_node.edges[0]    
        depth += 1
        current_node = edge.next_node

if __name__ == "__main__":
    pickle_test_2()

