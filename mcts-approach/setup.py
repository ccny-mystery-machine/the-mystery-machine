"""
Setup of the initial actors, places, items
"""
from random import randint


class Actor:
    """
    Class for a basic actor in the story
    """

    def __init__(self, name):
        self.name = name
        self.place = {
            "name": name + "'s house"
        }
        self.health = 10
        self.items = []
        self.anger = {}  # dictionary of other actors to their anger value

    # methods return a pair, the sentence and its believability

    def move(self, place):
        """
        description: actor moves to place
        precondition: place is not actor's current location
        postcondition: actor's current place is set to place
        """

        if self.place == place["name"]:
            return False

        self.place = place
        return (self.name + " went to " + place["name"] + ". ", 1)

    def steal(self, other_actor):
        """
        description: actor steals an item from other_actor
        precondition: actor must be alive and in other_actor's home,
            other_actor must have items that can be stolen
        postcondition: other_actor loses a random item and actor gains it,
            other_actor becomes angrier at actor
        """

        if self.health <= 0:
            return False

        b_house = other_actor + "'s house"
        if self.place["name"] != b_house or len(other_actor.items) == 0:
            return False

        other_actor_item = other_actor.items.pop(
            randint(0, len(other_actor.items))
        )
        self.items.append(other_actor.item)

        if other_actor.name in self.anger:
            self.anger[other_actor.name] += 1
        else:
            self.anger[other_actor.name] = 1
        sentence = (self.name + " stole " + other_actor_item["name"] +
                    " from " + other_actor["name"] + ". ")
        return (sentence, other_actor_item["value"])

    def play(self, other_actor):
        """
        description: actor plays with other_actor
        precondition: actor and other_actor must be alive and in same location
        postcondition: actor and other_actor becomes less angry with eachother
        """

        if (self.place != other_actor["place"] or
                self.health <= 0 or
                other_actor.health <= 0):
            return False

        if other_actor.name in self.anger:
            self.anger[other_actor.name] -= 1
        else:
            self.anger[other_actor.name] = -1

        if self.name in other_actor.anger:
            other_actor.anger[self.name] -= 1
        else:
            other_actor.anger[self.name] = -1
        return (self.name + " plays with " + other_actor.name + ". ", 1)

    def kill(self, other_actor):
        """
        description: actor kills other_actor
        precondition: actor and other_actor must be alive and in same location
        postcondition: other_actor's health goes to 0
        """
        if self.place != other_actor["place"]:
            return False

        other_actor.health = 0
        other_actor.name = other_actor["name"]
        if other_actor.name in self.anger:
            if self.anger[other_actor.name] > 0:
                believability = 1.0
            else:
                believability = 0.1
        return (self.name + " killed " + other_actor["name"] + ". ",
                believability)


ACTORS = [
    Actor("Alice"),
    Actor("Bob"),
    Actor("Charlie"),
]

ITEMS = [
    {
        "name": "gun",
        "value": .6
    },
    {
        "name": "vase",
        "value": .9,
    },
    {
        "name": "baseball bat",
        "value": .2,
    },
]

PLACES = [
    {
        "name": "outside",
    },
    {
        "name": "Alice's house",
    },
    {
        "name": "Bob's house",
    },
    {
        "name": "Charlie's house",
    },
]


"""
Defining the different goals we are checking for
"""


def death_occured(state):
    """
    description: checks if death has occured in the story
    returns a boolean indicating so or not
    """
    for actor in state.actors:
        if actor.health == 0:
            return True
    return False

GOALS = [
    death_occured,
]

#print(ACTORS)
#print(ITEMS)
#print(PLACES)
