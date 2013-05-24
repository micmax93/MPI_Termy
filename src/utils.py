from threading import Thread
import time
from globals import *
from random import randint, random


def __func_execution(delay, function, args=()):
    time.sleep(delay)
    function(*args)


def exec_later(delay, function, args=()):
    thread = Thread(target=__func_execution, args=[delay, function, args])
    thread.start()


def get_rand_gender():
    rd = randint(0, 1)
    if rd == 0:
        return GENDER_FEMALE
    else:
        return GENDER_MALE


def get_rand_locker_timeout():
    return  LOCKER_TIMEOUT[0] + (random() * LOCKER_TIMEOUT[1])