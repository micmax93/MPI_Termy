from globals import *


class LockersMonitor:
    """
    Locker monitor keeps locker room's states and enabled to retrieve them.
    """
    SEX_MALE = 'M'
    SEX_FEMALE = 'F'

    lockers = []

    def __init__(self):
        self.lockers = [[self.SEX_FEMALE, 0], [self.SEX_FEMALE, 0], [self.SEX_FEMALE, 0]]

    # Enter the locker room #num by person of given #sex
    def locker_in(self, num, sex):
        if self.lockers[num][0] == 0:
            self.lockers[num][0] = sex
        self.lockers[num][1] += 1

    # Leave the locker room #num
    def locker_out(self, num):
        self.lockers[num][1] -= 1

    # Check if locker room #num is empty or has same sex
    def check_locker_sex(self, num, sex):
        if self.lockers[num][0] == sex or self.lockers[num][1] == 0:
            return True
        return False

    # Test if person of #sex can enter locker room #num
    def check_enter(self, num, sex):
        if self.lockers[num][1] < GLOBAL_LOCKER_CAPACITY and self.check_locker_sex(num, sex):
            return True
        return False