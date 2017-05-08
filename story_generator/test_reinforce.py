from reinforce import state_index_number, state_index_number_2
from state import State
from setup import ACTORS, PLACES, ITEMS

class TestReinforce:

    def test_state_index_number_1(self):
        """
        Basic Test
        """
        root_state = State(ACTORS, PLACES, ITEMS) 
        assert state_index_number(root_state) == 0b1000100010001000

    def test_state_index_number_2(self):
        """
        Basic Test - test for items
        """
        root_state = State(ACTORS, PLACES, ITEMS)
        root_state.actors["ALICE"]["items"].append(ITEMS["GUN"])
        assert state_index_number(root_state) == 0b1001100010001000

    def test_state_index_number_3(self):
        """
        Basic Test - test for same place
        """
        root_state = State(ACTORS, PLACES, ITEMS)
        root_state.actors["CHARLIE"]["place"] = PLACES["DAPHNES_HOUSE"]
        assert state_index_number(root_state) == 0b1000100011001100
    
    def test_state_index_number_4(self):
        """
        Basic Test - test for death
        """
        root_state = State(ACTORS, PLACES, ITEMS)
        root_state.actors["CHARLIE"]["health"] = 0
        assert state_index_number(root_state) == 0b1000100000001000

    def test_state_index_number_5(self):
        """
        Basic Test - test for same place and angry
        """
        root_state = State(ACTORS, PLACES, ITEMS)
        root_state.actors["CHARLIE"]["place"] = PLACES["DAPHNES_HOUSE"]
        root_state.actors["CHARLIE"]["kill_desire"]["DAPHNE"] = 1
        assert state_index_number(root_state) == 0b1000100011101100

    def test_state_index_number_2_1(self):
        """
        Basic Test
        """
        root_state = State(ACTORS, PLACES, ITEMS) 
        assert state_index_number_2(root_state) == 0b10000000000

    def test_state_index_number_2_2(self):
        """
        Basic Test - test for items
        """
        root_state = State(ACTORS, PLACES, ITEMS)
        root_state.actors["ALICE"]["items"].append(ITEMS["GUN"])
        assert state_index_number_2(root_state) == 0b10000000001

    def test_state_index_number_2_3(self):
        """
        Basic Test - test for same place
        """
        root_state = State(ACTORS, PLACES, ITEMS)
        root_state.actors["CHARLIE"]["place"] = PLACES["DAPHNES_HOUSE"]
        assert state_index_number_2(root_state) == 0b10001000000
    
    def test_state_index_number_2_4(self):
        """
        Basic Test - test for death
        """
        root_state = State(ACTORS, PLACES, ITEMS)
        root_state.actors["CHARLIE"]["health"] = 0
        assert state_index_number_2(root_state) == 0b01100000000

    def test_state_index_number_2_5(self):
        """
        Basic Test - test for anger
        """
        root_state = State(ACTORS, PLACES, ITEMS)
        root_state.actors["CHARLIE"]["kill_desire"]["DAPHNE"] = 1
        assert state_index_number_2(root_state) == 0b10000001000
