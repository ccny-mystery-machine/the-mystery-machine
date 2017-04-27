
from main import run_once


if __name__ == "__main__":
    counter = 1
    counter2 = 1
    while True:
        n,s =  run_once(False)
    
        if n.value > 0:
            with open("data/good/" + str(counter) + ".txt", "w") as story_file:
                story_file.write(str(s) + "\nBelievability: " + str(n.believability) + "\nValue: " + str(n.value))
            print("Wrote to Good Folder -" + str(counter))        
            counter += 1
        else: 
            with open("data/bad/" + str(counter2) + ".txt", "w") as story_file:
                story_file.write(str(s) + "\nBelievability: " + str(n.believability) + "\nValue: " + str(n.value))
            print("Wrote to Bad Folder - " + str(counter2))
            counter2 += 1

