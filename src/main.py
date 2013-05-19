from my_mpi import *
from utils import exec_later


def say(*args):
    print(mpi_rank(), ': ', *args, sep='')


class LamportQueue:
    def __init__(self, name):
        self.name = name
        self.confirmations = 0
        self.state = 'idle'
        self.waiting_set = []

    def send_request(self):
        rank = mpi_rank()
        data = {'cmd': 'request', 'rank': rank, 'name': self.name}
        self.state = 'waiting'
        self.confirmations = 0
        mpi_send(1 - rank, data)  # todo: broadcast
        say("Request sent ", data)

    def send_confirmation(self, target):
        rank = mpi_rank()
        data = {'cmd': 'allowed', 'rank': rank, 'name': self.name}
        mpi_send(target, data)
        say("Confirmation sent to ", target)

    def exit_critical(self):
        say("Exiting critical section")
        self.state = 'idle'
        for e in self.waiting_set:
            self.send_confirmation(e)
        self.waiting_set = []

    def critical_section(self):
        #kod sekcji krytycznej
        say("Entering critical section")
        exec_later(2, LamportQueue.exit_critical, [self])

    def on_confirmation(self):
        self.confirmations += 1
        say("Confirmation received - ", self.confirmations, ' out of ', mpi_count() - 1)
        if self.confirmations == mpi_count() - 1:
            self.state = 'active'
            self.critical_section()

    def on_request(self, sender):
        say("Received request from ", sender)
        if self.state == 'idle':
            self.send_confirmation(sender)
        elif self.state == 'waiting' and mpi_rank() > sender:
            self.send_confirmation(sender)
        else:
            self.waiting_set.append(sender)


if __name__ == '__main__':
    while mpi_count() < 2:
        pass
    q = LamportQueue("kolejka")
    say("Requesting critical section")
    q.send_request()

    while True:
        data = mpi_recv()
        #say("Received com ", data)
        if data['cmd'] == 'request':
            q.on_request(data['rank'])
        elif data['cmd'] == 'allowed':
            q.on_confirmation()