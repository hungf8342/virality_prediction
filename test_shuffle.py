import graph_manip.shuffleGraphs as sg
import models.hawkes as hk
import numpy as np
import matplotlib.pyplot as plt

def getDegree(E):
    deg = np.zeros(np.max(E))
    for edge in E:
        deg[edge[0] - 1] += 1

data = np.loadtxt("graphs/soc-anybeat.txt", dtype='int')

orig_deg = getDegree(data)

equal_count = 0

for i in range(1000):
    temp_dat = sg.shuffle(data, i)
    temp_deg = getDegree(temp_dat)
    if not np.array_equal(temp_deg, orig_deg):
        print("NOT Equal!")
    else:
        equal_count += 1
    print(equal_count)

print("Equal: " + str(equal_count))
