from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    data = int(input("Enter an integer value to send: "))
    comm.send(data, dest=rank+1)
else:
    data = comm.recv(source=rank-1)
    print("Process", rank, "received value", data)
    data += rank
    if rank == size - 1:
        comm.send(data, dest=0)
    else:
        comm.send(data, dest=rank+1)
