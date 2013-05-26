from my_mpi import *
from access_monitor import *
from utils import *


class AccessManager():
    monitor = Monitor()
    type = None
    req_id = None
    req_state = 'outside'
    state = 'idle'
    queue_free_func = empty_func
    access_func = empty_func
    get_in_delay = 0
    exit_func = empty_func
    get_out_delay = 0

    def __init__(self, name, type, monitor):
        self.name = name
        self.confirmations_num = 0
        self.type = type
        self.monitor = monitor

    def mk_msg(self, cmd):
        rank = mpi_rank()
        data = {'cmd': cmd, 'rank': rank, 'name': self.name, 'tool': 'manager'}
        if cmd == 'request':
            data['id'] = self.req_id
            data['type'] = self.type
            data['state'] = self.req_state
        return data

    def get_in(self):
        say("Requesting ", self.name)
        (entry, id) = self.monitor.get_access(self.type)
        self.req_state = 'entering'
        if entry:
            say("Waiting for ", self.name, " confirm")
            self.req_id = id
            self.send_request()
        else:
            say("Waiting for ", self.name, " free")
            self.state = 'requesting'

    def get_out(self):
        self.req_state = 'exiting'
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
        if self.req_state == 'entering':
            say(">>Entering ", self.name, " ", self.req_id)
            self.monitor.get_in(self.req_id, self.type)
            self.req_state = 'inside'
            self.queue_free_func()
            exec_later(self.get_in_delay, self.access_func)
        elif self.req_state == 'exiting':
            say(">>Exiting ", self.name, " ", self.req_id)
            self.monitor.get_out(self.req_id)
            self.req_state = 'outside'
            exec_later(self.get_out_delay, self.exit_func)
            #mpi_send(mpi_rank(), self.mk_msg('job_done'))
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
            self.monitor.get_in(data['id'], data['type'])
        elif op == 'exiting':
            self.monitor.get_out(data['id'])

        self.send_confirmation(sender)

        if self.state == 'requesting':
            self.get_in()