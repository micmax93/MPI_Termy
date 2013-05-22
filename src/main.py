from my_mpi import *
from algo import *


def say_hello():
    print("Hello my name is ", mpi_rank())


if __name__ == '__main__':

    mpi_barrier()

    q = LamportQueue(name="kolejka", critical_section_func=say_hello, section_exit_delay=0.5)
    #say("Requesting critical section")
    q.send_request()

    loops = 1
    finished = 0

    while True:
        data = mpi_recv()
        #say("Received com ", data)
        if data['cmd'] == 'request':
            q.on_request(data['rank'])

        elif data['cmd'] == 'allowed':
            q.on_confirmation(data['rank'])

        elif data['cmd'] == 'job_done':
            if data['rank'] == mpi_rank():
                loops -= 1
                if loops > 0:
                    q.send_request()
                else:
                    finished += 1
                    mpi_bcast(q.mk_msg('job_done'))
            else:
                finished += 1
            if finished == mpi_count():
                break
