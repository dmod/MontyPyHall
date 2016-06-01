import multiprocessing
import signal
import traceback

import montyhallgame

NUM_PROCESSES = 8

class MontyHallSim:

    def __init__(self):
        self.shutdownFlag = False
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

    def shutdown(self, *args):
        for game in self.games:
            game.shutdown()

        self.shutdownFlag = True

    # For the number of processes defined, start a worker process that will
    # continually run a simulation of the Montly Hall Game
    def startWorkers(self):
        self.resultsQueue = multiprocessing.Queue()

        self.games = []

        for i in range(NUM_PROCESSES):
            game = montyhallgame.MontyHallGame(self.resultsQueue)

            workerProcess = multiprocessing.Process(target=game.start)
            workerProcess.start()
            self.games.append(workerProcess)

    def collectResults(self):
        switchWins = 0
        switchLosses = 0

        while not self.shutdownFlag:
            result = self.resultsQueue.get()
            if result:
                switchWins = switchWins + 1
            else:
                switchLosses = switchLosses + 1

            print("switchWins : " + str(switchWins) + " switch losses " + str(switchLosses), end='\r')


if __name__ == "__main__":
    # execute only if run as a script
    try:
        sim = MontyHallSim()
        sim.startWorkers()
        sim.collectResults()
    except:
        traceback.print_exc()
