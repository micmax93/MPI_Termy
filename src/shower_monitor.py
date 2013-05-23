from globals import *


class ShowerMonitor:
    def __init__(self):
        self.curr_amount = 0
        self.curr_sex = SEX_FEMALE

    def shower_in(self, sex):
        if self.curr_amount == 0:
            self.curr_sex = sex
        self.curr_amount += 1

    def shower_out(self, ):
        self.curr_amount -= 1

    def check_enter(self, sex):
        if self.curr_amount == 0:
            return True
        elif self.curr_amount < GLOBAL_LOCKER_CAPACITY and self.curr_sex == sex:
            return True
        else:
            return False