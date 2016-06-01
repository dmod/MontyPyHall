import random
import signal
from enum import Enum

NUM_DOORS = 3

Door = Enum('Door', 'goat car')

class MontyHallGame():

    def __init__(self, resultsQueue):
        self.shutdownFlag = False
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

        self.resultsQueue = resultsQueue

    def shutdown(self, *args):
        self.shutdownFlag = True

    def goGame(self):
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


    def start(self):
        while not self.shutdownFlag:
            self.resultsQueue.put(self.goGame())
