from eventHappens import eventHappens
from whatEvents import whatEvents
from isSubset import isSubset

def stories(story_so_far, prev_attr, goal_attr, eventfile, storyfile, st):
    if (len(story_so_far) > 100):
        return
    elif (isSubset(prev_attr, goal_attr, st)):
        storyfile.write(story_so_far + "\n")
        return
    else:
        print(st + "Story So Far = " + story_so_far)
        print(st + "Getting possible events for " + prev_attr)    
        eventfile.seek(0)
        possibleEvents = whatEvents(prev_attr, eventfile)
        print(st + "PossibleEvents = " + possibleEvents)
        for c in range(0, len(possibleEvents), 2):
            print(st + "Pursuing Story for " + possibleEvents[c:c+2])
            story_extend = story_so_far + possibleEvents[c:c+2]
            eventfile.seek(0)
            curr_attr = eventHappens(prev_attr, possibleEvents[c:c+2], eventfile)
            story_extend += curr_attr
            stories(story_extend, curr_attr, goal_attr, eventfile, storyfile, st + "\t")
        return
