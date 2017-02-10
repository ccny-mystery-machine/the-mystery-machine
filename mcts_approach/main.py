# actors, items, places
from setup import ACTORS, ITEMS, PLACES, METHODS, GOALS
from search import *

def goals_satisfied(state):
    for goal in GOALS:
        if not goal(state):
            return False
    return True



if __name__ == "__main__":
    print("Called")
