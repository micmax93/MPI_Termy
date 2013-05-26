from my_mpi import *
from utils import *


class AccessQueue:
    state = 'idle'
    confirmations_num = 0
    confirmations_tab = [False] * mpi_count()
    waiting_set = []
    get_access_func = empty_func

    def __init__(self, name):
        self.name = name
        pass

    def mk_msg(self, cmd):
        rank = mpi_rank()
        data = {'cmd': cmd, 'rank': rank, 'name': self.name, 'tool': 'queue'}
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
        say(">>Exiting ", self.name, " queue section")
        self.state = 'idle'
        for e in self.waiting_set:
            self.send_confirmation(e)
        self.waiting_set = []
        #mpi_send(mpi_rank(), self.mk_msg('job_done'))

    def critical_section(self):
        #kod sekcji krytycznej
        say(">>Entering ", self.name, " queue section")
        if self.get_access_func is not None:
            self.get_access_func()

    def on_confirmation(self, sender):
        if not self.confirmations_tab[sender]:
            self.confirmations_num += 1
            self.confirmations_tab[sender] = True
        #say(self.name," Confirmation received from ",sender, " - ",self.confirmations_num, ' out of ', mpi_count() - 1)
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