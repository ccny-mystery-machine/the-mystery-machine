def eventHappens(attr, event, eventfile):
    ans = attr[:]
#    print(ans)
    eventstring = eventfile.readline()
#    print("\nEvent String = " + eventstring)
    eventCharacteristics = ""
    while eventstring != "" :
        eventCharacteristics = eventstring.split('/')
#        print("Event Characteristics = ")
#        print(eventCharacteristics)
        if (eventCharacteristics[1] == event):
#            print("Event we are looking for has been found")
            break
        eventstring = eventfile.readline()
#        print("\nEvent String = " + eventstring)
    for i in range(0, len(eventCharacteristics[0]), 2):
#        print("Removing the following - " + eventCharacteristics[0][i:i+2])
        ans = ans.replace(eventCharacteristics[0][i:i+2], "")
#        print("New ans = " + ans)
    ans = eventCharacteristics[2].strip("\n") + ans
#    print("Appended ans = " + ans)
    return ans
