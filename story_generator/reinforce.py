# Tabulation of States
# 4 - number of actors

# 2 - alive or dead
# 2 - kill_desire or no kill_desire with someone in location
# 2 - In same location with another actor or not 
# 2 - Has item or not

# 93 - number of actions/methods
from setup import ACTORS, PLACES, ITEMS
from state import State
from tree import (TreeNode, expand_rand_edge, expand_all_believable_edges, 
                    choose_q_edge, choose_max_q_edge, find_edge_index,
                    expand_heuristic_edge, initialize_prob_dist)
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

# Conditions to check
# Number of alive actors - 3 bits
# Number of places with at least two actors - 2 bits
# Number of angry actors - 3 bit
# Number of actors with items - 3 bits
def state_index_number_2(state):
    actor_list = list(state.actors)

    num_alive = 0
    num_sharing_place = 0
    num_angry = 0
    num_actor_with_items = 0
    
    for idx, actor_key in enumerate(actor_list):
        actor = state.actors[actor_key]
        if actor["health"] > 0:
            num_alive += 1
        place = actor["place"]
        for other_actor_key,other_actor in state.actors.items():
            if actor_key != other_actor_key:
                if other_actor["place"] == place:
                    num_sharing_place += 1
                if actor["kill_desire"][other_actor_key] > 0:
                    num_angry += 1
        if len(actor["items"]) > 0:
            num_actor_with_items += 1
        
    num_sharing_place >>= 1
    index = 0
    index = (num_alive << 2) | num_sharing_place
    index = (index << 3) | num_angry
    index = (index << 3) | num_actor_with_items
    
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
        if depth >= 5:
            depth = 0 
            current_node = root_node
            print(current_node.state.actors["DAPHNE"]["place"])
            counter += 1
            print()
            if counter % 100 == 0:
                print("Counter - " + str(counter) + " - Dumping To File")
                with open("tree.pickle", "wb") as treefile:
                    pickle.dump(root_node, treefile, protocol=pickle.HIGHEST_PROTOCOL)         
            continue
        if not current_node.edges:
            expand_all_believable_edges(node=current_node, debug=True) 
        next_edge = choose_q_edge(node=current_node, epsilon=0.2)             
        best_edge = choose_max_q_edge(node=current_node)             
        if edge != None:
            reward = percent_goals_satisfied(current_node, GOALS)
            edge.qval = edge.qval  + 0.1*(reward + 0.9*(best_edge.qval) - edge.qval)
            print("{} {} {}".format(edge.method.sentence, reward, edge.qval))
        edge = next_edge
        depth += 1
        current_node = edge.next_node

def qlearn2(resume=True):
    root_state = State(ACTORS, PLACES, ITEMS)
    root_node = TreeNode(state=root_state, parent_edge=None, possible_methods=True)
    from tree import POSSIBLE_METHODS 
    num_methods = len(POSSIBLE_METHODS)
    table2 = {}
    eps = 0.2
    if resume:
        with open("table2.pickle", "rb") as table2file:
            table2 = pickle.load(table2file)
    current_node = root_node
    edge = None
    depth = 0
    counter = 0
    while True:
        if depth >= 20:
            depth = 0
            counter += 1
            edge = None
            #print()
            if counter % 100 == 0:
                print("Counter - " + str(counter) + " - Dumping To File")
                with open("table2.pickle", "wb") as table2file:
                    pickle.dump(table2, table2file, protocol=pickle.HIGHEST_PROTOCOL)
            if counter % 2000 == 0:
                print("Tree destroyed")
                root_state = State(ACTORS, PLACES, ITEMS)
                root_node = TreeNode(state=root_state, parent_edge=None, possible_methods=True)
                current_node = root_node         
                if eps > 0.2:
                    eps *= 0.97
            continue
        if not current_node.edges:
            expand_all_believable_edges(node=current_node, debug=True) 
        next_edge = choose_q_edge(node=current_node, epsilon=eps)             
        best_edge = choose_max_q_edge(node=current_node)             
        if edge != None:
            reward = percent_goals_satisfied(current_node, GOALS)
            idx = state_index_number_2(edge.prev_node.state)
            if idx not in table2:
                table2[idx] = [0.1] * num_methods
            idxc = state_index_number_2(current_node.state)
            if idxc not in table2:
                table2[idxc] = [0.1] * num_methods
            #print(idxc)
            #print(idx)
            #print(len(POSSIBLE_METHODS))
            bestqval = table2[idxc][find_edge_index(best_edge)]
            qval = table2[idx][find_edge_index(edge)]
            table2[idx][find_edge_index(edge)] = qval  + 0.1*(reward + 0.9*(bestqval) - qval)
            #print("{} {} {}".format(edge.method.sentence, reward, edge.qval))
        edge = next_edge
        depth += 1
        current_node = edge.next_node

def qlearn3(resume=True):
    root_state = State(ACTORS, PLACES, ITEMS)
    root_node = TreeNode(state=root_state, parent_edge=None, possible_methods=True)
    from tree import POSSIBLE_METHODS 
    num_methods = len(POSSIBLE_METHODS)
    table2 = {}
    eps = 0.2
    if resume:
        with open("table2.pickle", "rb") as table2file:
            table2 = pickle.load(table2file)
    current_node = root_node
    edge = None
    depth = 0
    counter = 0
    prob_dist = initialize_prob_dist()
    while True:
        if depth >= 20:
            depth = 0
            prob_dist = initialize_prob_dist()
            counter += 1
            edge = None
            #print()
            if counter % 100 == 0:
                print("Counter - " + str(counter) + " - Dumping To File")
                with open("table2.pickle", "wb") as table2file:
                    pickle.dump(table2, table2file, protocol=pickle.HIGHEST_PROTOCOL)
            root_state = State(ACTORS, PLACES, ITEMS)
            root_node = TreeNode(state=root_state, parent_edge=None, possible_methods=True)
            current_node = root_node         
            continue
        next_edge = expand_heuristic_edge(current_node, prob_dist)
        expand_all_believable_edges(node=current_node, debug=True) 
        best_edge = choose_max_q_edge(node=current_node)             
        if edge != None:
            reward = percent_goals_satisfied(current_node, GOALS)
            idx = state_index_number_2(edge.prev_node.state)
            if idx not in table2:
                table2[idx] = [0.1] * num_methods
            idxc = state_index_number_2(current_node.state)
            if idxc not in table2:
                table2[idxc] = [0.1] * num_methods
            #print(idxc)
            #print(idx)
            #print(len(POSSIBLE_METHODS))
            bestqval = table2[idxc][find_edge_index(best_edge)]
            qval = table2[idx][find_edge_index(edge)]
            table2[idx][find_edge_index(edge)] = qval  + 0.1*(reward + 0.9*(bestqval) - qval)
            #print("{} {} {}".format(edge.method.sentence, reward, edge.qval))
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
    qlearn3(True)

