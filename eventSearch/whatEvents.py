from isSubset import isSubset

def whatEvents(attr, eventfile):
   ansstring = ""
   eventstring = eventfile.readline()
#   print("\n Event String = " + eventstring) 
   while eventstring != "":
        eventCharacteristics = eventstring.split('/')
#        print("Event Characteristics = ")
#        print(eventCharacteristics)
        if isSubset(attr, eventCharacteristics[0], ""):
            ansstring += eventCharacteristics[1]
#            print(eventCharacteristics[0] + " is a subset of " + attr)
#        else:
#            print(eventCharacteristics[0] + " is not a subset of " + attr)
        eventstring = eventfile.readline()
#        print("\n Event String = " + eventstring)
   return ansstring
