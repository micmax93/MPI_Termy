from my_mpi import *
from utils import exec_later


if __name__ == '__main__':

    rank = mpi_rank()

    if rank == 0:
        exec_later(delay=3, function=mpi_send, args=[1, "Witam"])
        str = mpi_recv(source=1)
        print(str)

    elif rank == 1:
        str = mpi_recv(source=0)
        str += ", jestem Janusz"
        mpi_send(target=0, data=str)