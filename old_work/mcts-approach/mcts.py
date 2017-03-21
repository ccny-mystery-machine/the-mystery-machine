"""
Monte Carlo Tree Search
"""

from setup import *
from random import *


ACTORS2 = ACTORS[:]
PLACES2 = PLACES[:]
ITEMS2 = ITEMS[:]

def initStory():
    """
    Initial State of the Actors - just printed
    """
    print("Alice is in Alice's house")
    print("Bob is in Bob's house")
    print("Charlie is in Charlie's house")


def getAction(actorIndex, actionIndex, objIndex):
    """
    Given three numbers, perform an action
    """
    global ACTORS2
    global PLACES2
    global ITEMS2
    if (actionIndex == 0):
        return ACTORS2[actorIndex].move(PLACES2[objIndex])
    elif (actionIndex == 1):
        return ACTORS2[actorIndex].steal(ACTORS2[objIndex])
    elif (actionIndex == 2):
        return ACTORS2[actorIndex].play(ACTORS2[objIndex])
    else:
        return ACTORS2[actorIndex].kill(ACTORS2[objIndex])


def randomAction():
    """
    Picks a random action to do
    Keeps sampling until it finds valid action
    """
    global ACTORS2
    global PLACES2
    global ITEMS2
    while(True):
        actorIndex = randint(3)
        actionIndex = randint(4)
        if(actionIndex == 0):
            objIndex = randint(4)
            res = ACTORS2[actorIndex].move(PLACES2[objIndex])
        elif(actionIndex == 1):
            objIndex = randint(3)
            res = ACTORS2[actorIndex].steal(ACTORS2[objIndex])
        elif(actionIndex == 2):
            objIndex = randint(3)
            res = ACTORS2[actorIndex].play(ACTORS2[objIndex])
        else:
            objIndex = randint(3)
            res = ACTORS2[actorIndex].kill(ACTORS2[objIndex])
        if (res != False):
            #print(res[0])
            return res[1]
        
def nextAction():
    """
    Run Through All Actions
    """
    global ACTORS
    global PLACES
    for actor in range(3):
        for obj in range(4):
            res = ACTORS[actor].move(PLACES[obj])
            if (res != False)
                
            if (obj != 3):
                ACTORS[actor].steal(ACTORS[obj])
                ACTORS[actor].play(ACTORS[obj])
                ACTORS[actor].kill(ACTORS[obj])
                   

