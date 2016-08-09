from __future__ import print_function

import multiprocessing
import signal
import traceback
import time

import montyhallgame

NUM_PROCESSES = multiprocessing.cpu_count()

class MontyHallSim:

    def __init__(self):
        self.shutdown_flag = False
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        print("Number of processes: {0}, simulation starting...".format(NUM_PROCESSES))

    def shutdown(self, *args):
        for game in self.games:
            game.terminate()

        self.shutdown_flag = True

    # For the number of processes defined, start a worker process that will
    # continually run a simulation of the Montly Hall Game
    def start_workers(self):
        self.games = []

        for _ in range(NUM_PROCESSES):
            game = montyhallgame.MontyHallGame()
            game.start()
            self.games.append(game)

    def collect_results(self):

        while not self.shutdown_flag:

            collective_switch_wins = 0
            collective_switch_losses = 0

            for game in self.games:
                switch_wins, switch_losses = game.get_current_results()

                with switch_wins.get_lock():
                    collective_switch_wins += switch_wins.value
                with switch_losses.get_lock():
                    collective_switch_losses += switch_losses.value

            print("Switch Wins: {0}, Switch Losses: {1}".format(collective_switch_wins, collective_switch_losses), end = "\r")

if __name__ == "__main__":
    # execute only if run as a script
    try:
        sim = MontyHallSim()
        sim.start_workers()
        sim.collect_results()
    except:
        traceback.print_exc()
