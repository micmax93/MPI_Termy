from globals import *
from random import randint


class LockersMonitor:
    """
    Locker monitor keeps locker room's states and enabled to retrieve them.
    """
    lockers = []

    def __init__(self):
        self.lockers = [[SEX_FEMALE, 0], [SEX_FEMALE, 0], [SEX_FEMALE, 0]]  # ladies first ;)

    # Enter the locker room #num by person of given #sex
    def locker_in(self, num, sex):
        if self.is_locker_empty(num):
            self.lockers[num][0] = sex
        self.lockers[num][1] += 1

    # Leave the locker room #num
    def locker_out(self, num):
        self.lockers[num][1] -= 1

    # Test if locker #num is full
    def is_locker_full(self, num):
        if self.lockers[num][1] == GLOBAL_LOCKER_CAPACITY:
            return True
        return False

    # Test if locker #num is empty
    def is_locker_empty(self, num):
        if self.lockers[num][1] == 0:
            return True
        return False

    # Check if locker room #num is empty or has same sex
    def check_locker_sex(self, num, sex):
        if self.lockers[num][0] == sex or self.is_locker_empty(num):
            return True
        return False

    # Test if person of #sex can enter locker room #num
    def check_enter(self, num, sex):
        if self.lockers[num][1] < GLOBAL_LOCKER_CAPACITY and self.check_locker_sex(num, sex):
            return True
        return False

    # Find optimal locker room according to #sex
    def propose_best(self, sex):
        best = []
        best_val = -1
        for l in range(3):
            lck = self.lockers[l]
            if self.check_locker_sex(l, sex) and (not self.is_locker_full(l)):
                if lck[1] > best_val:
                    best_val = lck[1]
                    best = [l]
                elif lck[1] == best_val:
                    best.append(l)
        if len(best) == 1:
            return True, best[0]
        elif len(best) > 1:
            return True, best[randint(0, len(best)-1)]
        else:
            return False, -1


# if __name__ == '__main__':
#     monitor = LockersMonitor()
#     monitor.locker_in(0, SEX_FEMALE)
#     monitor.locker_in(1, SEX_MALE)
#     monitor.locker_in(1, SEX_MALE)
#     monitor.locker_in(1, SEX_MALE)
#     monitor.locker_in(1, SEX_MALE)
#     monitor.locker_in(2, SEX_FEMALE)
#     monitor.locker_in(2, SEX_FEMALE)
#     monitor.locker_in(2, SEX_FEMALE)
#
#     result = monitor.propose_best(SEX_FEMALE)
#
#     print(monitor.lockers)
#     print(result)