#                       _o_        _o_
#                       /_\         |
#                        X         / \
#+=================+----------+----------+
#|        Waiting: |          |          |
#|-----------------|----------|----------|
#| Locker room #1: |          |          |
#|-----------------|----------|----------|
#| Locker room #2: |          |          |
#|-----------------|----------|----------|
#| Locker room #3: |          |          |
#|-----------------|----------|----------|
#|        Showers: |          |          |
#|-----------------|----------|----------|
#|  Swimming pool: |          |          |
#+=================+==========+==========+

# distributed thermae simulator


from globals import *
from lockers_monitor import LockersMonitor
from shower_monitor import ShowerMonitor


class Console:
    MODE_PRO = 'pro'
    MODE_STD = 'std'

    mode = MODE_STD

    def __init__(self, mode):
        self.mode = mode

    def ffp(self, val):
        """
        Format-field-pro
        :param val: Value to print
        """
        return "    " + '{:6s}'.format(str(val)) + ""

    def count_people(self, lm, sm):
        male_count = 0
        female_count = 0

        for i in range(3):
            if lm.lockers[i][0] == GENDER_FEMALE:
                female_count += lm.lockers[i][1]
            else:
                male_count += lm.lockers[i][1]

        if sm.curr_gender == GENDER_FEMALE:
            female_count += sm.curr_amount
        else:
            male_count += sm.curr_amount

        return female_count, male_count

    def display_global_state(self, lm, sm):
        if self.mode == self.MODE_STD:
            self.display_global_state_std(lm, sm)
        else:
            self.display_global_state_pro(lm, sm)

    def display_global_state_std(self, lm, sm):
        pass

    def display_global_state_pro(self, lm, sm):
        """
        :type sm: ShowerMonitor
        :param sm: ShowerMonitor
        :type lm: LockersMonitor
        :param lm:
        """
        empty10 = " " * 10
        break_line = "   |-----------------|----------|----------|"

        female_count, male_count = self.count_people(lm, sm)
        # TODO use these values ^

        print("                          _o_        _o_    ")
        print("                          /_\         |     ")
        print("                           X         / \    ")
        print("   +=================+----------+----------+")
        print("   |        Waiting: |" + self.ffp(15) + "|" + self.ffp(15) + "|")
        print(break_line)

        for i in range(3):
            if lm.lockers[i][0] == GENDER_FEMALE:
                print("   | Locker room #" + str(i + 1) + ": |" + self.ffp(lm.lockers[i][1]) + "|" + empty10 + "|")
            else:
                print("   | Locker room #" + str(i + 1) + ": |" + empty10 + "|" + self.ffp(lm.lockers[i][1]) + "|")
            print(break_line)

        if sm.curr_gender == GENDER_FEMALE:
            print("   |        Showers: |" + self.ffp(sm.curr_amount) + "|" + empty10 + "|")
        else:
            print("   |        Showers: |" + empty10 + "|" + self.ffp(sm.curr_amount) + "|")

        print(break_line)

        print("   |  Swimming pool: |" + self.ffp(15) + "|" + self.ffp(15) + "|")
        print("   +=================+==========+==========+")


if __name__ == '__main__':
    console = Console(Console.MODE_PRO)
    lm = LockersMonitor()
    lm.get_in(0, GENDER_FEMALE)
    lm.get_in(0, GENDER_FEMALE)
    lm.get_in(1, GENDER_MALE)
    lm.get_in(1, GENDER_MALE)
    lm.get_in(2, GENDER_MALE)
    lm.get_in(2, GENDER_MALE)
    lm.get_in(2, GENDER_MALE)

    sm = ShowerMonitor()
    sm.get_in(0, GENDER_MALE)
    sm.get_in(0, GENDER_MALE)
    sm.get_in(0, GENDER_MALE)
    sm.get_in(0, GENDER_MALE)
    sm.get_in(0, GENDER_MALE)

    console.display_global_state_pro(lm, sm)