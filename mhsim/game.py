import random
from enum import Enum

NUM_DOORS = 3

Door = Enum('Door', 'goat car')

def goGame():
    doors = []
    carIndex = random.randrange(0, NUM_DOORS)
    #print("carindex: " + str(carIndex))
    for index in range(NUM_DOORS):
        if index == carIndex:
            doors.append(Door.car)
        else:
            doors.append(Door.goat)
    #print("doors made: " + str(doors))
    myPick = random.randrange(0, NUM_DOORS)
    #print("i picked: " + str(myPick))
    #print("which is a :" + str(doors[myPick]))

    for index in range(NUM_DOORS):
        if index != myPick and doors[index] is not Door.car:
            montyPick = index

    #print("monty picked: " + str(montyPick))
    #print("which is a :" + str(doors[montyPick]))

    #print("Im switching")
    for index in range(NUM_DOORS):
        if index != myPick and index != montyPick:
            #print("new pick: " + str(index))
            #print("which is a " + str(doors[index]))
            return (doors[index] is Door.car)


def go(q):
    while True:
        q.put(goGame())
