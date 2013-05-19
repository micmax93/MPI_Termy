from mpi4py import MPI


def mpi_send(target, data, tag=0):
    MPI.COMM_WORLD.send(data, target, tag)


def mpi_recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG):
    return MPI.COMM_WORLD.recv(None, source, tag)


def mpi_rank():
    return MPI.COMM_WORLD.Get_rank()


def mpi_count():
    return MPI.COMM_WORLD.Get_size()


def mpi_bcast(data):
    MPI.COMM_WORLD.bcast(data)