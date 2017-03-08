#from isSubset import isSubset
#from whatEvents import whatEvents
#from eventHappens import eventHappens
from stories import stories

#isSubset("aaabacadaeafagahai", "aaabahai", "")

file1 = open("events.txt", "r")
file2 = open("stories.txt", "a")
stories("aa", "aa", "ae", file1, file2, "")
file1.close()
file2.close()
