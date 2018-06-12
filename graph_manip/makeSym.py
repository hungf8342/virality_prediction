import numpy as np
from sets import Set

def makeSym(name):
    orig = np.loadtxt(name, dtype='int');
    points = Set()
    
    for point in orig:
        points.add((point[0],point[1]))
        points.add((point[1],point[0]))
    
    symmetric = []
    for point in points:
        symmetric.append([point[0], point[1]])
    print symmetric
    np.savetxt("sym" + name, symmetric, fmt='%d')
