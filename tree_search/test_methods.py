"""
Test file for the different methods that represent events that occur
"""
from setup import State, ACTORS, PLACES, ITEMS
from methods import METHODS

class TestMove:
    """
    Test class for the move method
    """
    def test_move_works_to_different_location(self):
        """
        Tests if actor's place changes to specified location
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["ALICES_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {},
            },
        }

        test_state = State(ACTORS,PLACES,ITEMS)
        METHODS["MOVE"]("ALICE", "BOBS_HOUSE",test_state)

        assert test_state.actors["ALICE"]["place"]["name"] == PLACES["BOBS_HOUSE"]["name"]
      
    def test_move_work_believability(self):
        """
        Tests if actor's move believability is 1 if the move is good
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["ALICES_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {},
            },
        }

        test_state = State(ACTORS,PLACES,ITEMS)
        sent, bel = METHODS["MOVE"]("ALICE", "BOBS_HOUSE",test_state)

        assert bel == 1
      
        
    def test_move_to_same_place(self):
        """
        Tests if believability is 0 when moving to same location
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["ALICES_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
        }

        test_state = State(ACTORS,PLACES,ITEMS)
        sentence, believability = METHODS["MOVE"]("ALICE",
                                                  "ALICES_HOUSE",
                                                  test_state)
        assert believability == 0

    def test_move_when_dead(self):
        """
        Tests if believability is 0 when moving while dead
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["ALICES_HOUSE"],
                "health": 0,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
        }

        test_state = State(ACTORS,PLACES,ITEMS)
        sentence, believability = METHODS["MOVE"]("ALICE",
                                                  "BOBS_HOUSE",
                                                  test_state)
        assert believability == 0


class TestMug:
    """
    Test class for the mug method
    """
    def test_mug_works(self):
        """
        Tests if mug successfully transfers items from actor_b to actor_a
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {},
            },
        }
        test_state = State(ACTORS,PLACES,ITEMS)
        METHODS["MUG"]("ALICE", "BOB", test_state)
        a_items = test_state.actors["ALICE"]["items"]
        b_items = test_state.actors["BOB"]["items"]
        assert (len(b_items) == 0 and
                len(a_items) == 2 and
                a_items[1] == ITEMS["VASE"])

    def test_mug_adds_properly(self):
        """
        Tests if mug successfully transfers items from actor_b to actor_a
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {},
            },
        }
        test_state = State(ACTORS,PLACES,ITEMS)
        METHODS["MUG"]("ALICE", "BOB", test_state)
        assert test_state.actors["BOB"]["anger"]["ALICE"] == 3

    def test_mug_believability_works(self):
        """
        Tests if mug outputs proper believability
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {},
            },
        }
        test_state = State(ACTORS,PLACES,ITEMS)
        sentence, believability = METHODS["MUG"]("ALICE", "BOB", test_state)
        a_items = test_state.actors["ALICE"]["items"]
        b_items = test_state.actors["BOB"]["items"]
        assert believability == ITEMS["VASE"]["value"]

    def test_mug_on_no_items(self):
        """
        Tests if believability is 0 when victim has no items
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [],
                "anger": {},
            },
        }
        test_state = State(ACTORS,PLACES,ITEMS)
        sentence, believability = METHODS["MUG"]("ALICE", "BOB", test_state)
        assert believability == 0

    def test_mug_when_dead(self):
        """
        Tests if believability is 0 when mugger is dead
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 0,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [],
                "anger": {},
            },
        }
        test_state = State(ACTORS,PLACES,ITEMS)
        sentence, believability = METHODS["MUG"]("ALICE", "BOB", test_state)
        assert believability == 0

    def test_mug_from_dead(self):
        """
        Tests if items can be stolen from dead actor
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 0,
                "items": [ITEMS["VASE"]],
                "anger": {},
            },
        }
        test_state = State(ACTORS,PLACES,ITEMS)
        METHODS["MUG"]("ALICE", "BOB", test_state)
        a_items = test_state.actors["ALICE"]["items"]
        b_items = test_state.actors["BOB"]["items"]
        assert (len(b_items) == 0 and
                len(a_items) == 2 and
                a_items[1] == ITEMS["VASE"])

    def test_mug_when_different_locations(self):
        """
        Tests if believability is 0 when actors are in different locations
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["ALICES_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {"BOB": 3},
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {"ALICE": -1},
            },
        }
        test_state = State(ACTORS,PLACES,ITEMS)
        sentence, believability = METHODS["MUG"]("ALICE", "BOB", test_state)

        assert believability == 0

    def test_mug_anger_values(self):
        """
        Tests if believability is 0 when actors are in different locations
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {"BOB": 3},
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {"ALICE": -1},
            },
        }
        test_state = State(ACTORS,PLACES,ITEMS)
        sentence, believability = METHODS["MUG"]("ALICE", "BOB", test_state)

        assert test_state.actors["BOB"]["anger"]["ALICE"] == 2


class TestTalk:
    """
    Test class for the talk method
    """
    def test_talk_works_when_empty(self):
        """
        Tests if talk creates new entries in the anger dictionary and assigns
        appropriate values
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {},
            },
        }
        test_state = State(ACTORS,PLACES,ITEMS)
        METHODS["TALK"]("ALICE", "BOB", test_state)

        assert (test_state.actors["ALICE"]["anger"]["BOB"] == -5 and
                test_state.actors["BOB"]["anger"]["ALICE"] == -5)

    def test_talk_works_with_values(self):
        """
        Tests if talk assigns appropriate values when already in place
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {"BOB": 3},
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {"ALICE": -1},
            },
        }
        test_state = State(ACTORS,PLACES,ITEMS)
        METHODS["TALK"]("ALICE", "BOB", test_state)

        assert (test_state.actors["ALICE"]["anger"]["BOB"] == -2 and
                test_state.actors["BOB"]["anger"]["ALICE"] == -6)

    def test_talk_when_different_locations(self):
        """
        Tests if believability is 0 when actors are in different locations
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["ALICES_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {"BOB": 3},
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {"ALICE": -1},
            },
        }
        test_state = State(ACTORS,PLACES,ITEMS)
        sentence, believability = METHODS["TALK"]("ALICE", "BOB", test_state)

        assert believability == 0


class TestKill:
    """
    Test class for the kill method
    """
    def test_kill_works(self):
        """
        Tests if actor_b gets killed
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {},
            },
        }

        test_state = State(ACTORS,PLACES,ITEMS)
        METHODS["KILL"]("ALICE", "BOB", test_state)
        assert test_state.actors["BOB"]["health"] == 0

    def test_kill_believability_one(self):
        """
        Tests kill believability when no anger
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {},  # dictionary of other actors to their anger value
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {},
            },
        }

        test_state = State(ACTORS,PLACES,ITEMS)
        sentence, believability = METHODS["KILL"]("ALICE", "BOB", test_state)
        assert believability == 0.1

    def test_kill_believability_two(self):
        """
        Tests kill believability when angry
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {"BOB": 1},  # dictionary of other actors to their anger value
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {},
            },
        }

        test_state = State(ACTORS,PLACES,ITEMS)
        sentence, believability = METHODS["KILL"]("ALICE", "BOB", test_state)
        assert believability == 0.9

    def test_kill_believability_three(self):
        """
        Tests kill believability
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {"BOB": -1},  # dictionary of other actors to their anger value
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {},
            },
        }

        test_state = State(ACTORS,PLACES,ITEMS)
        sentence, believability = METHODS["KILL"]("ALICE", "BOB", test_state)
        assert believability == 0.1


    def test_kill_when_different_locations(self):
        """
        Tests if believability is 0 when actors are in different locations
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["ALICES_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {"BOB": 3},
            },
            "BOB": {
                "name": "Bob",
                "home": PLACES["BOBS_HOUSE"],
                "place": PLACES["BOBS_HOUSE"],
                "health": 10,
                "items": [ITEMS["VASE"]],
                "anger": {"ALICE": -1},
            },
        }
        test_state = State(ACTORS,PLACES,ITEMS)
        sentence, believability = METHODS["KILL"]("ALICE", "BOB", test_state)

        assert believability == 0

    def test_kill_self(self):
        """
        Tests if believability is 0 when actors kill themselves
        """
        ACTORS = {
            "ALICE": {
                "name": "Alice",
                "home": PLACES["ALICES_HOUSE"],
                "place": PLACES["ALICES_HOUSE"],
                "health": 10,
                "items": [ITEMS["GUN"]],
                "anger": {"BOB": 3},
            },
        }
        test_state = State(ACTORS,PLACES,ITEMS)
        sentence, believability = METHODS["KILL"]("ALICE", "ALICE", test_state)

        assert believability == 0
