from my_mpi import *
from entry_queue import *
from locker_queue import *
from utils import exec_later


if __name__ == '__main__':

    mpi_barrier()
    q = {}

    q['entry'] = EntryQueue()
    q['lockers'] = LockerQueue(gender=GENDER_MALE)
    q['entry'].get_locker_func = q['lockers'].get_locker

    q['lockers'].entry_free_func = q['entry'].exit_critical
    q['lockers'].get_shower_func = q['lockers'].leave_locker  # TODO shower :)
    q['lockers'].locker_in_delay = 0.3

    loops = 1
    finished = 0

    q['entry'].send_request()

    while True:
        data = mpi_recv()
        name = data['name']
        #say("Received com ", data)
        if data['cmd'] == 'request':
            q[name].on_request(data['rank'], data)

        elif data['cmd'] == 'allowed':
            q[name].on_confirmation(data['rank'])

        elif data['cmd'] == 'job_done':
            if data['rank'] == mpi_rank():
                loops -= 1
                if loops > 0:
                    q['entry'].send_request()
                else:
                    finished += 1
                    mpi_bcast(q['entry'].mk_msg('job_done'))
            else:
                finished += 1
            if finished == mpi_count():
                break
