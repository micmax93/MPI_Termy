from mpi4py import MPI

_MSG_TAG = 8


def mpi_send(target, data):
    MPI.COMM_WORLD.send(data, target, _MSG_TAG)


def mpi_recv(source):
    return MPI.COMM_WORLD.recv(None, source, _MSG_TAG)


def mpi_rank():
    return MPI.COMM_WORLD.Get_rank()


def mpi_count():
    return MPI.COMM_WORLD.Get_size()