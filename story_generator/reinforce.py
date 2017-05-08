# Tabulation of States
# 4 - number of actors

# 2 - alive or dead
# 2 - kill_desire or no kill_desire with someone in location
# 2 - In same location with another actor or not 
# 2 - Has item or not

# 93 - number of actions/methods
from setup import ACTORS, PLACES, ITEMS
from state import State
from tree import TreeNode, expand_rand_edge, expand_all_believable_edges, choose_q_edge, choose_max_q_edge
from goals import percent_goals_satisfied, GOALS
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
    edge = None
    depth = 0
    counter = 0
    while True:
        if depth >= 15:
            depth = 0
            current_node = root_node
            counter += 1
            if counter % 100 == 0:
                print("Counter - " + str(counter) + " - Dumping To File")
                with open("tree.pickle", "wb") as treefile:
                    pickle.dump(root_node, treefile, protocol=pickle.HIGHEST_PROTOCOL)         
            continue
        if not current_node.edges:
            expand_all_believable_edges(node=current_node, debug=False) 
        next_edge = choose_q_edge(node=current_node, epsilon=0.2)             
        best_edge = choose_max_q_edge(node=current_node)             
        if edge != None:
            reward = percent_goals_satisfied(current_node, GOALS)
            edge.qval = edge.qval  + 0.1*(reward + 0.9*(best_edge.qval) - edge.qval)
        edge = next_edge
        depth += 1
        current_node = edge.next_node

def make_table():
    with open("tree.pickle", "rb") as treefile:
        root_node = pickle.load(treefile) 
    table = [0]*65536
    update_table(root_node, table)
    print(table) 
    with open("table.pickle", "wb") as tablefile:
        pickle.dump(table, tablefile, protocol=pickle.HIGHEST_PROTOCOL)
          
def update_table(root_node, table):
    if root_node.edges:
        update_table_with_node(root_node, table)
        for edge in root_node.edges:
            update_table(edge.next_node, table)

def update_table_with_node(node, table):
    max_q = node.edges[0].qval
    for edge in node.edges:
        if edge.qval > max_q:
            max_q = edge.qval
    index = state_index_number(node.state)
    if max_q > table[index]:
        table[index] = max_q 

if __name__ == "__main__":
    #qlearn(True)
    make_table()

