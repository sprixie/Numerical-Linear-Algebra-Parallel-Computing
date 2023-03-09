import sys, random
from time import *

n = 512

a = [[random.random() for row in range(n)]
        for col in range(n)]
b = [[random.random() for row in range(n)]
        for col in range(n)]
c = [[0 for row in range(n)]
        for col in range(n)]
start = time()

for i in range(n):
    for j in range(n):
        for k in range(n):
            c[i][j] += a[i][k] * b[k][j]
end = time()

print(end - start)
