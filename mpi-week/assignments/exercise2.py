from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

while True:
    if rank == 0:
        value = int(input("Enter an integer value (or negative value to exit): "))
    else:
        value = None

    value = comm.bcast(value, root=0)
    if value < 0:
        break

    print("Process", rank, "got", value)

MPI.Finalize()