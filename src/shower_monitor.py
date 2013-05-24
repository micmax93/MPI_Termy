from globals import *
from access_monitor import *


class ShowerMonitor(Monitor):
    def __init__(self):
        self.curr_amount = 0
        self.curr_gender = GENDER_FEMALE

    def shower_in(self, gender):
        if self.curr_amount == 0:
            self.curr_gender = gender
        self.curr_amount += 1

    def shower_out(self, ):
        self.curr_amount -= 1

    def check_enter(self, gender):
        if self.curr_amount == 0:
            return True
        elif self.curr_amount < GLOBAL_LOCKER_CAPACITY and self.curr_gender == gender:
            return True
        else:
            return False

    def get_in(self, id, type):
        self.shower_in(type)

    def get_out(self, id):
        self.shower_out()

    def get_access(self, type):
        return self.check_enter(type), 1