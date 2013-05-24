from my_mpi import *
from utils import exec_later


def say(*args):
    print(mpi_rank(), ' : ', *args, sep='')


class LamportQueue:
    def __init__(self, name, critical_section_func=None, section_exit_delay=0):
        self.name = name
        self.confirmations_num = 0
        self.confirmations_tab = [False] * mpi_count()
        self.state = 'idle'
        self.waiting_set = []
        self.critical_section_func = critical_section_func
        self.section_exit_delay = section_exit_delay

    def mk_msg(self, cmd):
        rank = mpi_rank()
        data = {'cmd': cmd, 'rank': rank, 'name': self.name}
        return data

    def send_request(self):
        data = self.mk_msg('request')
        self.state = 'waiting'
        self.confirmations_num = 0
        self.confirmations_tab = [False] * mpi_count()
        mpi_bcast(data)
        #say("Request sent ", data)

    def send_confirmation(self, target):

        data = self.mk_msg('allowed')
        mpi_send(target, data)
        #say("Confirmation sent to ", target)

    def exit_critical(self):
        #say(">>Exiting critical section")
        self.state = 'idle'
        for e in self.waiting_set:
            self.send_confirmation(e)
        self.waiting_set = []
        mpi_send(mpi_rank(), self.mk_msg('job_done'))

    def critical_section(self):
        #kod sekcji krytycznej
        say(">>Entering critical section")
        if self.critical_section_func is not None:
            self.critical_section_func()
        exec_later(self.section_exit_delay, LamportQueue.exit_critical, [self])

    def on_confirmation(self, sender):
        self.confirmations_num += 1
        self.confirmations_tab[sender] = True
        #say("Confirmation received from ", sender, " - ", self.confirmations_num, ' out of ', mpi_count() - 1)
        if self.confirmations_num == mpi_count() - 1:
            self.state = 'active'
            self.critical_section()

    def on_request(self, sender, data):
        #say("Received request from ", sender)
        if self.state == 'idle':
            self.send_confirmation(sender)
        elif self.state == 'waiting':
            if mpi_rank() > sender and not self.confirmations_tab[sender]:
                self.send_confirmation(sender)
            else:
                self.waiting_set.append(sender)
        else:
            self.waiting_set.append(sender)