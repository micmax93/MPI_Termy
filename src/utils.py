from threading import Thread
import time


def __func_execution(delay, function, args=()):
    time.sleep(delay)
    Thread(target=function, args=args).start()


def exec_later(delay, function, args=()):
    thread = Thread(target=__func_execution, args=[delay, function, args])
    thread.start()