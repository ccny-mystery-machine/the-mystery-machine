# Tabulation of States
# 4 - number of actors

# 2 - alive or dead
# 2 - kill_desire or no kill_desire with someone in location
# 2 - In same location with another actor or not 
# 2 - Has item or not

# 93 - number of actions/methods
from setup import ACTORS, PLACES, ITEMS
from state import State
from tree import TreeNode, expand_rand_edge, expand_q_edge, choose_q_edge
import pickle
import os

def state_index_number(state):
    actor_list = list(state.actors)
    actor_list.sort(reverse=True)
    index = 0
    
    for idx, actor_key in enumerate(actor_list):
        actor = state.actors[actor_key]
        alive = actor["health"] > 0
        with_another = False
        angry_with_another = False 
        place = actor["place"]
        for other_actor_key,other_actor in state.actors.items():
            if actor_key != other_actor_key:
                if other_actor["place"] == place:
                    with_another = True
                    if actor["kill_desire"][other_actor_key] > 0:
                        angry_with_another = True
                        break
        has_item = len(actor["items"]) > 0
        
        idx_part = (alive << 1) | with_another
        idx_part = (idx_part << 1) | angry_with_another
        idx_part = (idx_part << 1) | has_item
        index |= (idx_part << 4*idx)  
    
    return index

def qlearn(resume=True):
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
        if not current_node.edges:
            expand_all_believable_edges(current_node) 
        edge = choose_q_edge()    
                
        depth += 1
        current_node = edge.next_node




if __name__ == "__main__":
    qlearn(False)

    


    
       
