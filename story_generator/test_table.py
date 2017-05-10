import pickle
from setup import ACTORS, PLACES, ITEMS
from state import State
from reinforce import state_index_number, state_index_number_2

def table_test():
    with open("table.pickle", "rb") as tablefile:
        table = pickle.load(tablefile)
    root_state = State(ACTORS, PLACES, ITEMS)
    root_state.actors["BOB"]["place"] = PLACES["ALICES_HOUSE"]
    root_state.actors["BOB"]["kill_desire"]["ALICE"] = 1
    root_state.actors["ALICE"]["health"] = 0
    print(table[state_index_number(root_state)])

def table2_test(): 
    with open("table2.pickle", "rb") as table2file:
        table2 = pickle.load(table2file)
    root_state = State(ACTORS, PLACES, ITEMS)
    print(table2)

if __name__ == "__main__":
    table2_test()
