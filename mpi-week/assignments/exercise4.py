from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

n = 8
m = 8

if rank == 0:
    A = np.random.rand(n, m)
else:
    A = None

#counts and displacements for scatterv
counts = [int(n*m/size) if i < size-1 else n*m-int(n*m/size)*i for i in range(size)]
displs = [int(n*m/size)*i for i in range(size)]

#scatterv A to other processors
A_local = np.zeros(counts[rank])
comm.Scatterv([A, counts, displs, MPI.DOUBLE], A_local, root=0)

#receive A(i,j) for processor 1, 2, and 3
if rank == 1:
    A_local = A_local.reshape(int(n/2), int(m/2))[ :, int(m/2):]
elif rank == 2:
    A_local = A_local.reshape(int(n/2), int(m/2))[int(n/2):, :]
elif rank == 3:
    A_local = A_local.reshape(int(n/2), int(m/2))[int(n/2):, int(m/2):]

#gather results to processor 0
A_gathered = None
if rank == 0:
    A_gathered = np.zeros((n, m))
comm.Gatherv(A_local, [A_gathered, counts, displs, MPI.DOUBLE], root=0)

if rank == 0:
    print("A on processor 0:\n", A)
    print("A on processor 1:\n", A_gathered[:int(n/2), int(m/2):])
    print("A on processor 2:\n", A_gathered[int(n/2):, :int(m/2)])
    print("A on processor 3:\n", A_gathered[int(n/2):, int(m/2):])
