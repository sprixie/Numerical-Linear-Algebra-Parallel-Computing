from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

print("Hello World from process", rank)

from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print("Hello from process", rank, "of", size)

from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    print("Hello from the controller process!")

