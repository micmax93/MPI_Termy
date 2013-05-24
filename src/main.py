from my_mpi import *
from algo import *
from locker_queue import *
from utils import exec_later


def setup_queue():
    lockers = LockerQueue(name="lockers", section_exit_delay=0.5)

    def lockers_out():
        lockers.leave_locker()

    lockers.critical_section_func = lockers_out

    entry = LamportQueue(name="entry", critical_section_func=lockers.get_locker)
    return {'entry': entry, 'lockers': lockers}


if __name__ == '__main__':

    mpi_barrier()
    q = {}
    q['lockers'] = LockerQueue(name="lockers", gender=GENDER_MALE,)

    q['entry'] = LamportQueue(name="entry", critical_section_func=q['lockers'].get_locker, section_exit_delay=None)

    def lockers_out():
        #say("LOCKERS_OUT()")
        q['entry'].exit_critical()
        exec_later(0.3, q['lockers'].leave_locker)

    q['lockers'].critical_section_func = lockers_out

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
