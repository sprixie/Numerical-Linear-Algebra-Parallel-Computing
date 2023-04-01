#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 19:20:22 2020

@author: kissami
"""
import numpy as np
from scipy.sparse import lil_matrix
from numpy.random import rand, seed
from numba import njit
from mpi4py import MPI


''' This program compute parallel csc matrix vector multiplication using mpi '''

COMM = MPI.COMM_WORLD
nbOfproc = COMM.Get_size()
RANK = COMM.Get_rank()

seed(42)

@njit
def matrixVectorMult(A, b, x):
    row, col = A.shape
    for i in range(row):
        dot = 0
        for j in range(col):
            dot += A[i, j] * b[j]
        x[i] = dot

def scatterMatrix(matrix, counts, blockSize):
    localMatrix = np.zeros((counts[RANK], matrix.shape[1]), dtype=np.float64)
    for i in range(nbOfproc):
        startRow = np.sum(counts[:i])
        endRow = startRow + counts[i]
        if RANK == i:
            localMatrix = matrix[startRow:endRow]
        COMM.Barrier()
    return localMatrix

def gatherResult(localX, counts, blockSize):
    sendcounts = counts * blockSize
    displacements = np.insert(np.cumsum(sendcounts), 0, 0)[:-1]
    recvcounts = displacements[1:] if RANK != nbOfproc - 1 else None
    X = np.zeros((blockSize * nbOfproc), dtype=np.float64)
    COMM.Gatherv(localX, [X, sendcounts, displacements, MPI.DOUBLE], root=0)
    return X

########################initialize matrix A and vector b ######################
#matrix sizes
SIZE = 1000
blockSize = SIZE // nbOfproc

# counts = block of each proc
counts = np.array([blockSize] * nbOfproc, dtype=np.intc)
counts[-1] += SIZE % nbOfproc

if RANK == 0:
    A = lil_matrix((SIZE, SIZE))
    A[0, :100] = rand(100)
    A[1, 100:200] = A[0, :100]
    A.setdiag(rand(SIZE))
    A = A.toarray()
    b = rand(SIZE)
else:
    A = None
    b = None

#########Send b to all procs and scatter A (each proc has its own local matrix#####
b = COMM.bcast(b, root=0)
LocalMatrix = scatterMatrix(A, counts, blockSize)

#####################Compute A*b locally#######################################
LocalX = np.zeros((blockSize,), dtype=np.float64)
start = MPI.Wtime()
matrixVectorMult(LocalMatrix, b, LocalX)
stop = MPI.Wtime()

##################Gather the results ###########################################
X = gatherResult(LocalX, counts, blockSize)

##################Print the results ###########################################

if RANK == 0 :
    X_ = A.dot(b)
    error = np.max(np.abs(X_ - X))
    
    print(f"CPU time of parallel multiplication using {nbOfproc} processes is: {(stop - start)*1000:.6f} ms")
    print(f"The error comparing to the dot product is: {error:.1e}")
