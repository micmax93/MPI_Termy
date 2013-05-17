from mpi4py import MPI
from utils import exec_later

MSG_TAG = 8
SENDER = 1
RECEIVER = 0

comm = MPI.COMM_WORLD
rank = comm.Get_rank()


def my_send(str):
    print(rank, ".2: Awake", sep='')
    comm.send(str, 1, MSG_TAG)
    print(rank, '.2: Comm send "', str, '"', sep='')


if __name__ == '__main__':
    print("My rank is ", rank, sep='')

    if rank == 0:

        print(rank, ".2: Going to sleep", sep='')
        exec_later(delay=3, function=my_send, args=["Witam",])

        print(rank, ": Waiting for comm", sep='')
        str = comm.recv(None, 1, MSG_TAG)
        print(rank, ': Recieved comm "', str, '"', sep='')

    elif rank == 1:
        print(rank, ": Waiting for comm", sep='')
        str = comm.recv(None, 0, MSG_TAG)
        print(rank, ': Recieved comm "', str, '"', sep='')
        str += ", jestem Janusz"
        comm.send(str, 0, MSG_TAG)
        print(rank, ': Comm send "', str, '"', sep='')