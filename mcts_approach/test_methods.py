"""
Test file for the different methods that represent events that occur
"""
from setup import PLACES, ITEMS, move, steal, play, kill


class TestMove:
    """
    Test class for the move method
    """
    def test_move_works(self):
        """
        Tests if actor's place changes to specified location
        """
        test_actor_a = {
            "name": "Alice",
            "home": PLACES["ALICES_HOUSE"],
            "place": PLACES["ALICES_HOUSE"],
            "health": 10,
            "items": [ITEMS["GUN"]],
            "anger": {},
        }
        move(test_actor_a, PLACES["BOBS_HOUSE"])
        assert test_actor_a["place"]["name"] == PLACES["BOBS_HOUSE"]["name"]


class TestSteal:
    """
    Test class for the steal method
    """
    def test_steal_works(self):
        """
        Tests if steal successfully transfers items from actor_b to actor_a
        """
        test_actor_a = {
            "name": "Alice",
            "home": PLACES["ALICES_HOUSE"],
            "place": PLACES["BOBS_HOUSE"],
            "health": 10,
            "items": [ITEMS["GUN"]],
            "anger": {},
        }
        test_actor_b = {
            "name": "Bob",
            "home": PLACES["BOBS_HOUSE"],
            "place": PLACES["BOBS_HOUSE"],
            "health": 10,
            "items": [ITEMS["VASE"]],
            "anger": {},
        }
        steal(test_actor_a, test_actor_b)
        a_items = test_actor_a["items"]
        b_items = test_actor_b["items"]
        assert (len(b_items) == 0 and
                len(a_items) == 2 and
                a_items[1] == ITEMS["VASE"])


class TestPlay:
    """
    Test class for the play method
    """
    def test_play_works(self):
        """
        Tests if play creates new entries in the anger dictionary and assigns
        appropriate values
        """
        test_actor_a = {
            "name": "Alice",
            "home": PLACES["ALICES_HOUSE"],
            "place": PLACES["BOBS_HOUSE"],
            "health": 10,
            "items": [ITEMS["GUN"]],
            "anger": {},
        }
        test_actor_b = {
            "name": "Bob",
            "home": PLACES["BOBS_HOUSE"],
            "place": PLACES["BOBS_HOUSE"],
            "health": 10,
            "items": [ITEMS["VASE"]],
            "anger": {},
        }
        play(test_actor_a, test_actor_b)
        assert (test_actor_a["anger"]["Bob"] == -1 and
                test_actor_b["anger"]["Alice"] == -1)


class TestKill:
    """
    Test class for the kill method
    """
    def test_kill_works(self):
        """
        Tests if actor_b gets killed
        """
        test_actor_a = {
            "name": "Alice",
            "home": PLACES["ALICES_HOUSE"],
            "place": PLACES["BOBS_HOUSE"],
            "health": 10,
            "items": [ITEMS["GUN"]],
            "anger": {},
        }
        test_actor_b = {
            "name": "Bob",
            "home": PLACES["BOBS_HOUSE"],
            "place": PLACES["BOBS_HOUSE"],
            "health": 10,
            "items": [ITEMS["VASE"]],
            "anger": {},
        }
        kill(test_actor_a, test_actor_b)
        assert test_actor_b["health"] == 0
