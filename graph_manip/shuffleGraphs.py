import random
import numpy as np

def shuffle(E, num):
    A = np.copy(E)
    for i in range(num):
        indices = random.sample(range(A.shape[0]), 2)
        temp = A[indices[0], 1]
        A[indices[0],1] = A[indices[1],1]
        A[indices[1],1] = temp
    return A
