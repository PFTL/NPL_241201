from time import sleep
from threading import Thread
from multiprocessing import Process


def long_running():
    print('Before sleeping')
    sleep(5)
    print('After sleeping')


if __name__ == "__main__":
    print('Before long running')
    t = Process(target=long_running)
    t.start()

    t2 = Thread(target=long_running)
    t2.start()

    print('After long running')