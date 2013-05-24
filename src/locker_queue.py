from algo import *
from lockers_monitor import *
from utils import *


class LockerQueue():
    lockers = LockersMonitor()
    gender = None
    req_locker = None
    locker_state = 'outside'
    state = 'idle'
    name = 'lockers'
    entry_free_func = empty_func
    get_shower_func = empty_func
    locker_in_delay = 0

    def __init__(self, gender):
        self.confirmations_num = 0
        self.gender = gender

    def mk_msg(self, cmd):
        rank = mpi_rank()
        data = {'cmd': cmd, 'rank': rank, 'name': self.name}
        if cmd == 'request':
            data['locker'] = self.req_locker
            data['gender'] = self.gender
            data['state'] = self.locker_state
        return data

    def get_locker(self):
        say("Requesting locker")
        (entry, lid) = self.lockers.propose_best(self.gender)
        self.locker_state = 'entering'
        if entry:
            say("Waiting for locker confirm")
            self.req_locker = lid
            self.send_request()
        else:
            say("Waiting for locker free")
            self.state = 'requesting'

    def leave_locker(self):
        self.locker_state = 'exiting'
        self.send_request()

    def send_request(self):
        self.state = 'waiting'
        data = self.mk_msg('request')
        self.confirmations_num = 0
        mpi_bcast(data)
        #say("Request sent ", data)

    def send_confirmation(self, target):
        data = self.mk_msg('allowed')
        mpi_send(target, data)
        #say("Confirmation sent to ", target)

    def critical_section(self):
        #kod sekcji krytycznej
        if self.locker_state == 'entering':
            say(">>Entering locker ", self.req_locker)
            self.lockers.locker_in(self.req_locker, self.gender)
            self.locker_state = 'inside'
            self.entry_free_func()
            exec_later(self.locker_in_delay, self.get_shower_func)
        elif self.locker_state == 'exiting':
            say(">>Exiting locker ", self.req_locker)
            self.lockers.locker_out(self.req_locker)
            self.locker_state = 'outside'
            mpi_send(mpi_rank(), self.mk_msg('job_done'))
        self.state = 'idle'

    def on_confirmation(self, sender):
        self.confirmations_num += 1
        #say("Locker confirmation received from ", sender, " - ", self.confirmations_num, ' out of ', mpi_count() - 1)
        if self.confirmations_num == mpi_count() - 1:
            self.state = 'active'
            self.critical_section()

    def on_request(self, sender, data):
        #say("Received request from ", sender)
        op = data['state']
        if op == 'entering':
            self.lockers.locker_in(data['locker'], data['gender'])
        elif op == 'exiting':
            self.lockers.locker_out(data['locker'])

        self.send_confirmation(sender)

        if self.state == 'requesting':
            self.get_locker()