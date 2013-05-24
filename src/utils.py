from threading import Thread
import time


def __func_execution(delay, function, args=()):
    time.sleep(delay)
    function(*args)


def exec_later(delay, function, args=()):
    thread = Thread(target=__func_execution, args=[delay, function, args])
    thread.start()


def empty_func():
    pass