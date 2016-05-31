import game
import multiprocessing

NUM_PROCESSES = 8

def main():
    q = multiprocessing.Queue()
    print("in main")

    for index in range(NUM_PROCESSES):
        p = multiprocessing.Process(target=game.go, args=(q,))
        p.start()

    switchWins = 0
    switchLosses = 0
    while True:
        result = q.get()
        if result:
            switchWins = switchWins + 1
        else:
            switchLosses = switchLosses + 1

        print("switchWins : " + str(switchWins) + " switch losses " + str(switchLosses), end='\r')

if __name__ == "__main__":
    # execute only if run as a script
    main()
