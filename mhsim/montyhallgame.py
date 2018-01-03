import random
import signal
import multiprocessing

NUM_DOORS = 3


# 'Enum'-like class used to represent either a 'goat' or 'car' door
class Door:
    goat = 1
    car = 2


class MontyHallGame(multiprocessing.Process):

    def __init__(self):
        super(MontyHallGame, self).__init__()

        self.shutdown_flag = False
        signal.signal(signal.SIGTERM, self.shutdown)

        self.switch_wins = multiprocessing.Value('i', 0)
        self.switch_losses = multiprocessing.Value('i', 0)

    def shutdown(self, *args):
        self.shutdown_flag = True

    @staticmethod
    def go_game():

        doors = []
        # The car will be placed at a random index between 0 and NUM_DOORS
        car_index = random.randrange(0, NUM_DOORS)

        # Iterate through the NUM_DOORS and populate each door with either a
        # car or a goat depending on the index of the door
        for door_index in range(NUM_DOORS):
            if door_index == car_index:
                doors.append(Door.car)
            else:
                doors.append(Door.goat)

        # Doors are now populated, have the contestant pick a random door index
        contestant_pick = random.randrange(0, NUM_DOORS)

        # Now that the contestant has picked their door choice, have Monty pick
        # a door that 1) The contestant did not pick AND 2) Does not have a car
        # behind it (Monty knows which door has a car)
        for door_index in range(NUM_DOORS):
            if door_index != contestant_pick and doors[door_index] is not Door.car:
                monty_pick = door_index

        # Now, since this contestant will always switch their choice, iterate
        # through the doors to find the door that neither the contestant nor
        # Monty picked (the door that the contestant would have switched to)
        # and return True if the door contained the car
        for door_index in range(NUM_DOORS):
            if door_index not in [contestant_pick, monty_pick]:
                return (doors[door_index] is Door.car)

    def get_current_results(self):
        return self.switch_wins, self.switch_losses

    def run(self):
        while not self.shutdown_flag:
            if MontyHallGame.go_game():
                with self.switch_wins.get_lock():
                    self.switch_wins.value += 1
            else:
                with self.switch_losses.get_lock():
                    self.switch_losses.value += 1
