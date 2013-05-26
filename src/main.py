from my_mpi import *
from access_controller import *
from lockers_monitor import *
from shower_monitor import *


def job_done():
    data = {'cmd': 'job_done', 'rank': mpi_rank(), 'name': mpi_rank()}
    mpi_send(mpi_rank(), data)


def job_finished():
    data = {'cmd': 'job_done', 'rank': mpi_rank(), 'name': mpi_rank()}
    mpi_bcast(data)


if __name__ == '__main__':

    mpi_barrier()
    q = {}

    gender = GENDER_MALE
    q['lockers'] = AccessController('lockers', gender, LockersMonitor())
    q['showers'] = AccessController('showers', gender, ShowerMonitor())

    LOCKER_DELAY = 0.2
    SHOWER_DELAY = 0.3
    POOL_DELAY = 0.5
    q['lockers'].set_access_func(LOCKER_DELAY, q['showers'].enter)
    q['showers'].set_access_func(SHOWER_DELAY, q['showers'].exit)
    q['showers'].set_exit_func(POOL_DELAY, q['lockers'].exit)
    q['lockers'].set_exit_func(0, job_done)

    loops = 1
    finished = 0

    q['lockers'].enter()

    while True:
        data = mpi_recv()
        name = data['name']
        #say("Received com ", data)
        if data['cmd'] == 'request':
            q[name].on_request(data['rank'], data)

        elif data['cmd'] == 'allowed':
            q[name].on_confirmation(data['rank'], data)

        elif data['cmd'] == 'job_done':
            if data['rank'] == mpi_rank():
                loops -= 1
                if loops > 0:
                    q['entry'].send_request()
                else:
                    finished += 1
                    job_finished()
            else:
                finished += 1
            if finished == mpi_count():
                break
