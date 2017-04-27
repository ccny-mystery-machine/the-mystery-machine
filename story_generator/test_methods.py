"""
Test file for the different methods that represent events that occur
"""
from math import isclose

from setup import ACTORS, PLACES, ITEMS
from state import State
from methods import METHODS

class TestMove:
    """
    Test class for the move method
    """
    def test_move_works_to_different_location(self):
        """
        Tests if actor's place changes to specified location
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        METHODS["MOVE"]("ALICE", "BOBS_HOUSE",test_state)

        assert test_state.actors["ALICE"]["place"]["name"] == PLACES["BOBS_HOUSE"]["name"]
      
    def test_move_work_believability(self):
        """
        Tests if actor's move believability is 1 if the move is good
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        sent, bel = METHODS["MOVE"]("ALICE", "BOBS_HOUSE",test_state)

        assert bel == 1
      
        
    def test_move_to_same_place(self):
        """
        Tests if believability is 0 when moving to same location
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        sentence, believability = METHODS["MOVE"]("ALICE",
                                                  "ALICES_HOUSE",
                                                  test_state)
        assert believability == 0

    def test_move_when_dead(self):
        """
        Tests if believability is 0 when moving while dead
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        test_state.actors["ALICE"]["health"] = 0
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
        test_state = State(ACTORS,PLACES,ITEMS)

        alice = test_state.actors["ALICE"]
        bob = test_state.actors["BOB"]
        alice["items"] = [ITEMS["GUN"]]
        bob["items"] = [ITEMS["VASE"]]
        bob["place"] = PLACES["ALICES_HOUSE"]

        METHODS["MUG"]("ALICE", "BOB", test_state)
        assert (len(bob["items"]) == 0 and
                len(alice["items"]) == 2 and
                alice["items"][1] == ITEMS["VASE"])

    def test_mug_adds_kill_desire_properly(self):
        """
        Tests if mug adds kill_desire properly
        """
        test_state = State(ACTORS,PLACES,ITEMS)

        alice = test_state.actors["ALICE"]
        bob = test_state.actors["BOB"]
        alice["items"] = [ITEMS["GUN"]]
        bob["items"] = [ITEMS["VASE"]]
        bob["place"] = PLACES["ALICES_HOUSE"]

        METHODS["MUG"]("ALICE", "BOB", test_state)
        assert test_state.actors["BOB"]["kill_desire"]["ALICE"] == 0.15

    def test_mug_believability_works(self):
        """
        Tests if mug outputs proper believability
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        alice = test_state.actors["ALICE"]
        bob = test_state.actors["BOB"]
        alice["items"] = [ITEMS["GUN"]]
        bob["items"] = [ITEMS["VASE"]]
        bob["place"] = PLACES["ALICES_HOUSE"]
        sentence, believability = METHODS["MUG"]("ALICE", "BOB", test_state)
        assert believability == ITEMS["VASE"]["value"]

    def test_mug_on_no_items(self):
        """
        Tests if believability is 0 when victim has no items
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        alice = test_state.actors["ALICE"]
        bob = test_state.actors["BOB"]
        alice["items"] = [ITEMS["GUN"]]
        bob["items"] = []
        bob["place"] = PLACES["ALICES_HOUSE"]
        sentence, believability = METHODS["MUG"]("ALICE", "BOB", test_state)
        assert believability == 0

    def test_mug_when_dead(self):
        """
        Tests if believability is 0 when mugger is dead
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        alice = test_state.actors["ALICE"]
        bob = test_state.actors["BOB"]
        alice["items"] = [ITEMS["GUN"]]
        alice["health"] = 0
        bob["items"] = [ITEMS["VASE"]]
        bob["place"] = PLACES["ALICES_HOUSE"]
        test_state.actors["BOB"]["place"] = PLACES["ALICES_HOUSE"]
        sentence, believability = METHODS["MUG"]("ALICE", "BOB", test_state)
        assert believability == 0

    def test_mug_from_dead(self):
        """
        Tests if items can be stolen from dead actor
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        alice = test_state.actors["ALICE"]
        bob = test_state.actors["BOB"]
        alice["items"] = [ITEMS["GUN"]]
        bob["items"] = [ITEMS["VASE"]]
        bob["place"] = PLACES["ALICES_HOUSE"]
        test_state.actors["BOB"]["health"] = 0
        METHODS["MUG"]("ALICE", "BOB", test_state)
        assert (len(alice["items"]) == 2 and
                len(bob["items"]) == 0 and
                alice["items"][1] == ITEMS["VASE"])

    def test_mug_when_different_locations(self):
        """
        Tests if believability is 0 when actors are in different locations
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        alice = test_state.actors["ALICE"]
        bob = test_state.actors["BOB"]
        alice["items"] = [ITEMS["GUN"]]
        bob["items"] = [ITEMS["VASE"]]
        sentence, believability = METHODS["MUG"]("ALICE", "BOB", test_state)
        assert believability == 0

    def test_mug_kill_desire_values(self):
        """
        Tests if mug updates kill_desire values
        """
        test_state = State(ACTORS,PLACES,ITEMS)

        alice = test_state.actors["ALICE"]
        bob = test_state.actors["BOB"]
        alice["items"] = [ITEMS["GUN"]]
        bob["items"] = [ITEMS["VASE"]]
        bob["place"] = PLACES["ALICES_HOUSE"]

        alice["kill_desire"]["BOB"] = 0.3
        bob["kill_desire"]["ALICE"] = -0.1

        sentence, believability = METHODS["MUG"]("ALICE", "BOB", test_state)

        assert isclose(test_state.actors["BOB"]["kill_desire"]["ALICE"],  0.05)


class TestTalk:
    """
    Test class for the talk method
    """
    def test_talk_works(self):
        """
        Tests if talk assigns appropriate values in kill_desire
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        test_state.actors["BOB"]["place"] = PLACES["ALICES_HOUSE"]
        METHODS["TALK"]("ALICE", "BOB", test_state)

        assert (test_state.actors["ALICE"]["kill_desire"]["BOB"] == -0.05 and
                test_state.actors["BOB"]["kill_desire"]["ALICE"] == -0.05)

    def test_talk_when_different_locations(self):
        """
        Tests if believability is 0 when actors are in different locations
        """
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
        test_state = State(ACTORS,PLACES,ITEMS)
        test_state.actors["ALICE"]["items"].append(ITEMS["GUN"])
        test_state.actors["BOB"]["place"] = PLACES["ALICES_HOUSE"]
        METHODS["KILL"]("ALICE", "BOB", test_state)
        assert test_state.actors["BOB"]["health"] == 0

    def test_kill_believability_one(self):
        """
        Tests kill believability when no kill_desire
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        test_state.actors["ALICE"]["items"].append(ITEMS["GUN"])
        test_state.actors["BOB"]["place"] = PLACES["ALICES_HOUSE"]
        sentence, believability = METHODS["KILL"]("ALICE", "BOB", test_state)
        assert believability == 0

    def test_kill_believability_two(self):
        """
        Tests kill believability when angry
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        test_state.actors["ALICE"]["items"].append(ITEMS["GUN"])
        test_state.actors["ALICE"]["kill_desire"]["BOB"] = 0.1
        test_state.actors["BOB"]["place"] = PLACES["ALICES_HOUSE"]
        sentence, believability = METHODS["KILL"]("ALICE", "BOB", test_state)
        assert believability == 1

    def test_kill_believability_three(self):
        """
        Tests kill believability when negative kill desire
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        test_state.actors["ALICE"]["items"].append(ITEMS["GUN"])
        test_state.actors["ALICE"]["kill_desire"]["BOB"] = -0.1
        test_state.actors["BOB"]["place"] = PLACES["ALICES_HOUSE"]
        sentence, believability = METHODS["KILL"]("ALICE", "BOB", test_state)
        assert believability == 0


    def test_kill_when_different_locations(self):
        """
        Tests if believability is 0 when actors are in different locations
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        test_state.actors["ALICE"]["items"].append(ITEMS["GUN"])
        sentence, believability = METHODS["KILL"]("ALICE", "BOB", test_state)
        assert believability == 0

    def test_kill_self(self):
        """
        Tests if believability is 0 when actors kill themselves
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        test_state.actors["ALICE"]["items"].append(ITEMS["GUN"])
        sentence, believability = METHODS["KILL"]("ALICE", "ALICE", test_state)

        assert believability == 0


class TestDropItem:

    def test_drop_item(self):
        """
        Tests if believability is 1 when actor drop item
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        test_state.actors["ALICE"]["items"].append(ITEMS["GUN"])
        sentence, believability = METHODS["DROP_ITEM"]("ALICE",test_state)
        assert believability == ITEMS["GUN"]["drop_believability"]

    def test_drop_item_when_dead(self):
        """
        Tests if believability is 0 when actor is dead and drop item
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        test_state.actors["ALICE"]["items"].append(ITEMS["GUN"])
        test_state.actors["ALICE"]["health"] = 0
        sentence, believability = METHODS["DROP_ITEM"]("ALICE",test_state)
        assert believability == 0

    def test_drop_item_on_no_items(self):
        """
        Tests if believability is 0 when actor has no items to drop
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        alice = test_state.actors["ALICE"]
        alice["items"] = []
        sentence, believability = METHODS["DROP_ITEM"]("ALICE", test_state)
        assert believability == 0

class TestPickUpItem:

    def test_pickup_item(self):
        """
        Tests if that have believability when actor pick up item
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        alice = test_state.actors["ALICE"]
        test_state.actors["ALICE"]["place"] = PLACES["LIBRARY"]
        sentence, believability = METHODS["PICKUP_ITEM"]("ALICE",test_state)
        assert believability == 1


    def test_pickup_item_when_dead(self):
        """
        Tests if believability is 0 when actor is dead and pick up item
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        test_state.actors["ALICE"]["health"] = 0
        sentence, believability = METHODS["PICKUP_ITEM"]("ALICE",test_state)
        assert believability == 0

    def test_pickup_item_when_different_locations(self):
        """
        Tests if believability is 0 when actor pick up item in different locations
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        sentence, believability = METHODS["PICKUP_ITEM"]("ALICE", test_state)
        assert believability == 0

    def test_pickup_item_on_no_items(self):
        """
        Tests if believability is 0 when place has no items to pick
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        alice = test_state.actors["ALICE"]
        test_state.actors["ALICE"]["place"] = PLACES["BOBS_HOUSE"]
        sentence, believability = METHODS["PICKUP_ITEM"]("ALICE", test_state)
        assert believability == 0

class TestCall:
    """
    Test class for the talk method
    """
    def test_call(self):
        """
        Tests if believability is 1 when actors_a call actor_b in different locations
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        alice = test_state.actors["ALICE"]
        bob = test_state.actors["BOB"]
        sentence, believability = METHODS["CALL"]("ALICE", "BOB", test_state)
        assert believability == 1

    def test_call_when_same_locations(self):
        """
        Tests if believability is 0 when actors are in same locations
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        alice = test_state.actors["ALICE"]
        bob = test_state.actors["BOB"]
        bob["place"] = PLACES["ALICES_HOUSE"]
        sentence, believability = METHODS["CALL"]("ALICE", "BOB", test_state)
        assert believability == 0

    def test_call_when_they_are_dead(self):
        """
        Tests if believability is 0 when actors are dead
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        alice = test_state.actors["ALICE"]
        bob = test_state.actors["BOB"]
        alice["health"] = 0
        sentence, believability = METHODS["CALL"]("ALICE", "BOB", test_state)
        assert believability == 0


class TestEvent:

    def test_event_believability(self):
        """
        Tests if believability is 1 when event was happened
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        sentence, believability = METHODS["EVENT"]("BOBS_HOUSE",test_state)
        assert believability == 1
    
    def test_event_works(self):
        """
        Tests if everyone moved to the location
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        sentence, believability = METHODS["EVENT"]("LIBRARY", test_state)
        alice = test_state.actors["ALICE"]
        bob = test_state.actors["BOB"]
        charlie = test_state.actors["CHARLIE"]
        lib = PLACES["LIBRARY"]
        assert (alice["place"] == lib and 
                bob["place"] == lib and 
                charlie["place"] == lib)


class TestFire:

    def test_fire(self):
        """
        Tests if believability is 1 when fire was happened
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        alice = test_state.actors["ALICE"]
        bob = test_state.actors["BOB"]
        sentence, believability = METHODS["FIRE"]("BOBS_HOUSE",test_state)
        assert believability == 0.3

    def test_fire_no_one_in_that_place(self):
        """
        Tests if believability is 1 when fire was happened but no one hurt
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        alice = test_state.actors["ALICE"]
        bob = test_state.actors["BOB"]
        charlie = test_state.actors["CHARLIE"]
        print(alice["health"])
        print(bob["health"])
        #sentence, believability = METHODS["FIRE"]("WAREHOUSE",test_state)
        assert (alice["health"] == 1 and
                bob["health"] == 1)


    def test_fire_people_in_that_place(self):
        """
        Tests if believability is 1 when fire was happened but everyone hurt
        """
        test_state = State(ACTORS,PLACES,ITEMS)
        alice = test_state.actors["ALICE"]
        bob = test_state.actors["BOB"]
        bob["place"] = PLACES["ALICES_HOUSE"]
        sentence, believability = METHODS["FIRE"]("ALICES_HOUSE",test_state)
        assert (alice["health"] == 0 and
                bob["health"] == 0)
 
