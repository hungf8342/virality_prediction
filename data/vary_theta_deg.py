import sklearn.linear_model as lm
import sklearn.model_selection as ms
import numpy as np
import random
import networkx as nx
import os, sys
sys.path.insert(0, '../')
import models.hawkes as hs
import graph_manip.graphAttribs as ga
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sklearn.metrics as mt

# Loads the secondary degree of each node
def loadSecondDeg(G, theta):
    degrees = np.zeros(len(G.nodes()))
    deg_map = G.degree()
    for i in range(len(degrees)):
        degrees[i] = theta * deg_map[i]
        for edge in G.edges(i):
            degrees[i] += (theta ** 2) * deg_map[edge[1]]
   
    return degrees + 1

def main():

    # Initialize values
    outData = []
    count = 0
    total_theta = 0
    total_num = 0
    graph_nodes = 0

    # Find the average critical theta for the shuffled graphs
    for filename in os.listdir("graphlets"):
        if filename.endswith("gfc"): 
            
            # Load up the related graphs
            gDat = open(os.path.join("graphs", filename[:-4] + ".dat"), "rb")
            firstLine = gDat.readline().split()

            # Get the critical values
            G = nx.read_edgelist(gDat, nodetype=int)
            total_theta += ga.getCritTheta(G)
            total_num += 1
            print(str(total_num) + ': \t' + str((1.0 * total_theta)/total_num))
            sys.stdout.flush()

    # Take the average of the calculated theta
    theta = np.real(total_theta) / total_num

    # Initialize the outData matrix
    for alpha in np.linspace(0.8, 1.1, 1000):
        sec_deg = []
        hawkes = []
        outData.append((alpha, sec_deg, hawkes))
    
    # Load in data from files
    for filename in os.listdir("graphlets"):
        if filename.endswith("gfc"):
            
            # Load up the related graph
            gDat = open(os.path.join("graphs", filename[:-4] + ".dat"), "rb")
            firstLine = gDat.readline().split()
            G = nx.read_edgelist(gDat, nodetype=int)
            N = int(firstLine[0])
            graph_nodes = N 
           
            D, V = hs.getEigData(G)

            for i in range(len(outData)):
                # Calculate the expected hawkes events from each
                # node
                hVec = hs.getHawkesVecFromEig(D, V, theta * outData[i][0])
                deg_vec = np.asarray(G.degree())[:,1]
                #sec_vec = loadSecondDeg(G, theta)
                print(str(count) + ": " + str(outData[i][0]))

                if len(hVec) > 0:
                    for j in range(N):
                        #i = random.randint(0, N - 1)
                        outData[i][1].append(deg_vec[j])
                        outData[i][2].append(hVec[j])
            count += 1
            print(count)
            sys.stdout.flush()
   
    # Initialize data arrays
    rSquare = []
    rms = []
    coeff = []
    alphas = []
    average_hwks = []
    node_order = []
    top_1_acc = []
    top_5_acc = []
    top_10_acc = []
    for data in outData:
        if len(data[2]) > 0:

            # Train the linear model
            xData = np.asarray(data[1]).reshape(-1,1)
            yData = np.log10(np.asarray(data[2]))
            model = lm.LinearRegression()
            xTrain, xTest, yTrain, yTest = ms.train_test_split(xData, yData, test_size=0.3, random_state=64)
            print(data[0])
            model.fit(xTrain, yTrain)

            # Get the alpha which correlates with this
            alphas.append(data[0])
            
            # Get the r^2 data
            rSquare.append(mt.r2_score(yTest, model.predict(xTest)))

            # Get the rms data
            rms.append(mt.mean_squared_error(yTest, model.predict(xTest)))

            # Get the coefficient data
            coeff.append(np.asarray(model.coef_))

            # Get the average hawkes step data
            average_hwks.append(np.mean(yData))
            
            total_top_1  = [] 
            total_top_5  = [] 
            total_top_10 = []
            # Get node ranking data
            for i in range(len(yData) / graph_nodes):
                curY = yData[i * graph_nodes:graph_nodes * (i + 1)]
                predY = model.predict(xData[i * graph_nodes:graph_nodes * (i + 1)])
                ordY = np.argsort(curY)
                ordPredY = np.argsort(predY)

                top_1 = set(ordY[:1]) & set(ordPredY[:1])
                top_5 = set(ordY[:5]) & set(ordPredY[:5])
                top_10 = set(ordY[:10]) & set(ordPredY[:10])

                total_top_1.append(len(top_1))
                total_top_5.append(len(top_5))
                total_top_10.append(len(top_10))

            top_1_acc.append(np.mean(total_top_1))
            top_5_acc.append(np.mean(total_top_5))
            top_10_acc.append(np.mean(total_top_10))

    average_hwks = np.asarray(average_hwks)
    top_1_acc = np.asarray(top_1_acc)
    top_5_acc = np.asarray(top_5_acc)
    top_10_acc = np.asarray(top_10_acc)
    rSquare = np.asarray(rSquare)
    rms = np.asarray(rms)
    ind = np.argsort(average_hwks)
 
    # top 1 accuracy
    plt.plot(average_hwks[ind], top_1_acc[ind])
    plt.xlabel("Average Number of Hawkes Events (log)")
    plt.ylabel('top 1 correct')
    plt.savefig("top_1_deg.png")
    plt.close()

    # top 5 accuracy
    plt.plot(average_hwks[ind], top_5_acc[ind])
    plt.xlabel("Average Number of Hawkes Events (log)")
    plt.ylabel('top 5 correct')
    plt.savefig("top_5_deg.png")
    plt.close()

    # top 10 accuracy
    plt.plot(average_hwks[ind], top_10_acc[ind])
    plt.xlabel("Average Number of Hawkes Events (log)")
    plt.ylabel('top 10 correct')
    plt.savefig("top_10_deg.png")
    plt.close()


    # r^2 score
    plt.plot(average_hwks[ind], rSquare[ind])
    plt.xlabel("Average Number of Hawkes Events (log)")
    plt.ylabel(r'$R^2$')
    plt.savefig("rSquare_deg.png")
    plt.close()

    # rms
    plt.plot(average_hwks[ind], rms[ind])
    plt.xlabel("Average Number of Hawkes Events (log)")
    plt.ylabel('Root Mean Squared')
    plt.savefig("rms_deg.png")
    plt.close()
    
    # number of hawkes events
    plt.plot(alphas, average_hwks)
    plt.xlabel("Alpha Value")
    plt.ylabel(r'$\log_{10} ($Average Hawkes Events$)$')
    plt.savefig("hawkes_deg.png")
    plt.close()
    
    # test fit to one alpha on all other alphas
    rSquareSpread = []
    xData = np.asarray(outData[416][1]).reshape(-1,1)
    yData = np.log10(np.asarray(outData[416][2]))
    model = lm.LinearRegression()
    xTrain, xTest, yTrain, yTest = ms.train_test_split(xData, yData, test_size=0.3, random_state=64)
    model.fit(xTrain, yTrain)

    for data in outData:
        if len(data[2]) > 0:
            xData = np.asarray(data[1]).reshape(-1,1)
            yData = np.log10(np.asarray(data[2]))
            rSquareSpread.append(max(mt.r2_score(yData, model.predict(xData)), 0))
    
    plt.plot(average_hwks, rSquareSpread)
    plt.xlabel("Average Number of Hawkes Events (log)")
    plt.ylabel(r'$R^2$')
    plt.savefig("rSquareSpread_deg.png")
    plt.close()  

main()
