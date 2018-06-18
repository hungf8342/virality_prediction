import numpy as np
import networkx as nx
import os, sys
sys.path.insert(0, '../')
import models.hawkes as hs
import pickle

def main():
    xData = []
    yData = []
    count = 0
    for filename in os.listdir("graphlets"):
        if filename.endswith("gfc"): 
            graphlets = np.loadtxt(open(os.path.join("graphlets", filename), "rb"),usecols=range(2,48))
            E = np.loadtxt(open(os.path.join("graphs", filename[:-4] + ".dat"), "rb"), dtype="int")
            datVec = np.sum(graphlets, axis=0)
            hawkes = hs.exact_hawkes_arr(E, 0.1426)
            if hawkes > 0:
                xData.append(datVec)
                yData.append(hawkes)
                print(count)
            else:
                print("-1")
            count += 1
    pickle.dump((xData, yData), open("outData.dat", 'wb'))
main()
