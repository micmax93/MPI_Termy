from my_mpi import *
from utils import exec_later

rank = mpi_rank()


def my_send(str):
    print(rank, ".2: Awake", sep='')
    mpi_send(target=1, data=str)
    print(rank, '.2: Comm send "', str, '"', sep='')


if __name__ == '__main__':
    print("My rank is ", rank, sep='')

    if rank == 0:

        print(rank, ".2: Going to sleep", sep='')
        exec_later(delay=3, function=my_send, args=["Witam", ])

        print(rank, ": Waiting for comm", sep='')
        str = mpi_recv(source=1)
        print(rank, ': Recieved comm "', str, '"', sep='')

    elif rank == 1:
        print(rank, ": Waiting for comm", sep='')
        str = mpi_recv(source=0)
        print(rank, ': Recieved comm "', str, '"', sep='')
        str += ", jestem Janusz"
        mpi_send(target=0, data=str)
        print(rank, ': Comm send "', str, '"', sep='')