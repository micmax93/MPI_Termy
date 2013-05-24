from access_manager import *
from access_queue import *


class AccessController:
    def __init__(self, name, type, monitor):
        self.queue = AccessQueue(name)
        self.manager = AccessManager(name, type, monitor)

        self.queue.get_access_func = self.manager.get_in
        self.manager.queue_free_func = self.queue.exit_critical
        #self.manager.access_func = self.exit_func()
        #self.manager.get_in_delay = 0.3

    def set_access_func(self, delay, func):  # shower.in(locker delay) | #shower.out(shower_delay)
        self.manager.access_func = func
        self.manager.get_in_delay = delay

    def set_exit_func(self, delay, func):  # job_done | locker.out(pool delay)
        self.manager.exit_func = func
        self.manager.get_out_delay = delay

    def enter(self):
        self.queue.send_request()

    def exit(self):
        self.manager.get_out

    def on_confirmation(self, sender, data):
        if data['tool'] == 'queue':
            self.queue.on_confirmation(sender)
        elif data['tool'] == 'manager':
            self.manager.on_confirmation(sender)

    def on_request(self, sender, data):
        if data['tool'] == 'queue':
            self.queue.on_request(sender, data)
        elif data['tool'] == 'manager':
            self.manager.on_request(sender, data)