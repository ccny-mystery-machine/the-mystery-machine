# Tabulation of States
# 4 - number of actors

# 2 - alive or dead
# 2 - kill_desire or no kill_desire with someone in location
# 2 - In same location with another actor or not 
# 2 - Has item or not

# 93 - number of actions/methods
from state import random_state


def state_index_number(state):
    actor_list = list(state.actors)
    actor_list.sort()
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
    
# Randomly assigns actors, places, and items for story
root_state = random_state(4,4) 

print(state_index_number(root_state))


