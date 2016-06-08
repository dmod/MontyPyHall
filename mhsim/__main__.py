import multiprocessing
import signal
import traceback
import time

import montyhallgame

NUM_PROCESSES = 4

class MontyHallSim:

    def __init__(self):
        self.shutdownFlag = False
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

    def shutdown(self, *args):
        for game in self.games:
            game.terminate()

        self.shutdownFlag = True

    # For the number of processes defined, start a worker process that will
    # continually run a simulation of the Montly Hall Game
    def startWorkers(self):
        self.games = []

        for _ in range(NUM_PROCESSES):
            game = montyhallgame.MontyHallGame()
            game.start()
            self.games.append(game)

    def collectResults(self):

        while not self.shutdownFlag:

            collectiveSwitchWins = 0
            collectiveSwitchLosses = 0

            for game in self.games:
                switchWins, switchLosses = game.getCurrentResults()

                with switchWins.get_lock():
                    collectiveSwitchWins += switchWins.value
                with switchLosses.get_lock():
                    collectiveSwitchLosses += switchLosses.value

            print("Switch Wins: " + str(collectiveSwitchWins) +
                  " Switch Losses: " + str(collectiveSwitchLosses), end='\r')

if __name__ == "__main__":
    # execute only if run as a script
    try:
        sim = MontyHallSim()
        sim.startWorkers()
        sim.collectResults()
    except:
        traceback.print_exc()
