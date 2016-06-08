import random
import signal
import multiprocessing
from enum import Enum

NUM_DOORS = 3

Door = Enum('Door', 'goat car')

class MontyHallGame(multiprocessing.Process):

    def __init__(self):
        super(MontyHallGame, self).__init__()

        self.shutdownFlag = False
        signal.signal(signal.SIGTERM, self.shutdown)

        self.switchWins = multiprocessing.Value('i', 0)
        self.switchLosses = multiprocessing.Value('i', 0)

    def shutdown(self, *args):
        self.shutdownFlag = True

    def goGame(self):

        doors = []
        # The car will be placed at a random index between 0 and NUM_DOORS
        carIndex = random.randrange(0, NUM_DOORS)

        # Iterate through the NUM_DOORS and populate each door with either a
        # car or a goat depending on the index of the door
        for doorIndex in range(NUM_DOORS):
            if doorIndex == carIndex:
                doors.append(Door.car)
            else:
                doors.append(Door.goat)

        # Doors are now populated, have the contestant pick a random door index
        contestantPick = random.randrange(0, NUM_DOORS)

        # Now that the contestant has picked their door choice, have Monty pick
        # a door that 1) The contestant did not pick AND 2) Does not have a car
        # behind it (Monty knows which door has a car)
        for doorIndex in range(NUM_DOORS):
            if doorIndex != contestantPick and doors[doorIndex] is not Door.car:
                montyPick = doorIndex

        # Now, since this contestant will always switch their choice, iterate
        # through the doors to find the door that neither the contestant nor
        # Monty picked (the door that the contestant would have switched to)
        # and return True if the door contained the car
        for doorIndex in range(NUM_DOORS):
            if doorIndex != contestantPick and doorIndex != montyPick:
                return (doors[doorIndex] is Door.car)

    def getCurrentResults(self):
        return (self.switchWins, self.switchLosses)

    def run(self):
        while not self.shutdownFlag:
            if self.goGame():
                with self.switchWins.get_lock():
                    self.switchWins.value += 1
            else:
                with self.switchLosses.get_lock():
                    self.switchLosses.value += 1
