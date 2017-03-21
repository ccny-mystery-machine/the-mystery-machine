wrdsize = 2;

# Check to see if attr2 is a subset of attr1
def isSubset(attr1, attr2, st):
#    print(st + "isSubset Function Call")
    if (len(attr2) > 2):
#        print(st + attr2 + " has more than 2 characters");
        for i in range(0, len(attr2), 2):
#            print(st + attr1 + " and " + attr2[i:i+wrdsize] + " are being compared. - i = " + str(i))
            if (isSubset(attr1, attr2[i:i+wrdsize], st + "\t") == False):
#                print(st + attr2[i:i+wrdsize] + " is not found in " + attr1)
#                print(st + attr2 + " is not found in " + attr1)
                return False
#            print(st + attr2[i:i+wrdsize] + " is found in " + attr1)
#        print(st + attr2 + " is found in " + attr1)
        return True
    elif(len(attr2) == 2):
#        print(st + attr2 + " has exactly 2 characters");
        for j in range(0, len(attr1), 2):
#            print(st + attr1[j:j+wrdsize] + " and " + attr2 + " are being compared.")  
            if (attr1[j:j+wrdsize] == attr2):
#                print(st + attr1[j:j+wrdsize] + " and " + attr2 + " are equal.")  
#                print(st + attr2 + " is found in " + attr1)  
                return True
#            print(st + attr1[j:j+wrdsize] + " and " + attr2 + " are not equal.")  
#        print(st + attr2 + " is not found in " + attr1)  
        return False
    else:
#        print(st + attr2 + " has no characters");
        return True
            
