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
    for alpha in np.linspace(0.7, 1.0, 500):
        network_data = []
        outData.append((alpha, network_data))
    
    # Load in data from files
    for filename in os.listdir("graphlets"):
        if filename.endswith("gfc"):
            
            # Load up the related graph
            gDat = open(os.path.join("graphs", filename[:-4] + ".dat"), "rb")
            firstLine = gDat.readline().split()
            G = nx.read_edgelist(gDat, nodetype=int)
            N = int(firstLine[0])
            graph_nodes = N 
           
            # Load up the relevant data fro the graph
            D, V = hs.getEigData(G)

            d, dA = hs.get_sec_deg_dat(G)
            
            for i in range(len(outData)):
                outData[i][1].append(([],[]))
                # Calculate the expected hawkes events from each
                # node
                hVec = hs.getHawkesVecFromEig(D, V, theta * outData[i][0])
                if len(hVec) > 0:
                    for j in range(N):
                        outData[i][1][-1][0].append([d[j],dA[j], d[j] + theta * outData[i][0] * dA[j]])
                        outData[i][1][-1][1].append(hVec[j])

            count += 1
            print(count)
            sys.stdout.flush()
 
    # Process data for both linear regression and ordering

    separated_dat = []
    log_dat = []
    for theta_dat in outData:
        test_ind = set(random.sample(range(len(theta_dat[1])), int(len(theta_dat[1]) * 0.3)))
        print test_ind
        
        # Process normal data
        separated_dat.append([theta_dat[0], [], [], [], []])
        for i in range(len(theta_dat[1])):
            if i in test_ind:
                separated_dat[-1][1] += theta_dat[1][i][0]
                separated_dat[-1][2] += theta_dat[1][i][1]
            else:
                separated_dat[-1][3] += theta_dat[1][i][0]
                separated_dat[-1][4] += theta_dat[1][i][1]

        # Process top-k data
        log_dat.append([theta_dat[0], [], [], [], []])
        for i in range(len(theta_dat[1])):
            sort_ind = np.argsort(theta_dat[1][i][1])
            new_dat = np.zeros(len(theta_dat[1][i][1]))#np.linspace(0, 1, len(theta_dat[1][i][1]))
            new_dat[-10:] = 1
            if i in test_ind:
                log_dat[-1][1] += np.asarray(theta_dat[1][i][0])[sort_ind].tolist()
                log_dat[-1][2] += new_dat.tolist()
            else:
                log_dat[-1][3] += np.asarray(theta_dat[1][i][0])[sort_ind].tolist()
                log_dat[-1][4] += new_dat.tolist()

  
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
    top_1_acc_log = []
    top_5_acc_log = []
    top_10_acc_log = []
    
    for sd_ind in range(len(separated_dat)):
        data = separated_dat[sd_ind]
        log_data = log_dat[sd_ind]
        if len(data[1]) > 0 and len(data[3]) > 0:

            # Train the linear model
            xTest = data[1]
            yTest = np.log10(data[2])
            xTrain = data[3]
            yTrain = np.log10(data[4])
            xData = np.append(xTest, xTrain, axis=0) 
            yData = np.append(yTest, yTrain)
            model = lm.LinearRegression()
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

            # Get node order data
            yInd = np.argsort(yData[:graph_nodes])
            node_order.append(np.arange(graph_nodes)[yInd])
            
            total_top_1  = [] 
            total_top_5  = [] 
            total_top_10 = []
            # Get node ranking data
            for i in range(len(yData) / graph_nodes):
                curY = yData[i * graph_nodes:graph_nodes * (i + 1)]
                predY = model.predict(xData[i * graph_nodes:graph_nodes * (i + 1)])
                ordY = np.argsort(curY)
                ordPredY = np.argsort(predY)
                top_1 = set(ordY[-1:]) & set(ordPredY[-1:])
                top_5 = set(ordY[-5:]) & set(ordPredY[-5:])
                top_10 = set(ordY[-10:]) & set(ordPredY[-10:])

                total_top_1.append(len(top_1))
                total_top_5.append(len(top_5))
                total_top_10.append(len(top_10))

            top_1_acc.append(np.mean(total_top_1))
            top_5_acc.append(np.mean(total_top_5))
            top_10_acc.append(np.mean(total_top_10))

            # Get logistic regression rankings
            
            
            xTest = log_data[1]
            yTest = log_data[2]
            xTrain = log_data[3]
            yTrain = log_data[4]
            model = lm.LinearRegression()
            model.fit(xTrain, yTrain)

            total_top_1_log  = [] 
            total_top_5_log  = [] 
            total_top_10_log = []
            # Get node ranking data
            print(data[0]) 
            for i in range(len(yData) / graph_nodes):
                curY = yData[i * graph_nodes:graph_nodes * (i + 1)]
                predY = model.predict(xData[i * graph_nodes:graph_nodes * (i + 1)])
                ordY = np.argsort(curY)
                ordPredY = np.argsort(predY)
                top_1 = set(ordY[-1:]) & set(ordPredY[-1:])
                top_5 = set(ordY[-5:]) & set(ordPredY[-5:])
                top_10 = set(ordY[-10:]) & set(ordPredY[-10:])

                total_top_1_log.append(len(top_1))
                total_top_5_log.append(len(top_5))
                total_top_10_log.append(len(top_10))

            top_1_acc_log.append(np.mean(total_top_1_log))
            top_5_acc_log.append(np.mean(total_top_5_log))
            top_10_acc_log.append(np.mean(total_top_10_log))

    average_hwks = np.asarray(average_hwks)
    top_1_acc = np.asarray(top_1_acc)
    top_5_acc = np.asarray(top_5_acc)
    top_10_acc = np.asarray(top_10_acc)
    top_1_acc_log = np.asarray(top_1_acc_log)
    top_5_acc_log = np.asarray(top_5_acc_log)
    top_10_acc_log = np.asarray(top_10_acc_log)
    rSquare = np.asarray(rSquare)
    rms = np.asarray(rms)
    ind = np.argsort(average_hwks)
    
    # top 1 accuracy
    plt.plot(average_hwks[ind], top_1_acc[ind])
    plt.xlabel("Average Number of Hawkes Events (log)")
    plt.ylabel('top 1 correct')
    plt.savefig("top_1_sec.png")
    plt.close()

    # top 5 accuracy
    plt.plot(average_hwks[ind], top_5_acc[ind])
    plt.xlabel("Average Number of Hawkes Events (log)")
    plt.ylabel('top 5 correct')
    plt.savefig("top_5_sec.png")
    plt.close()

    # top 10 accuracy
    plt.plot(average_hwks[ind], top_10_acc[ind])
    plt.xlabel("Average Number of Hawkes Events (log)")
    plt.ylabel('top 10 correct')
    plt.savefig("top_10_sec.png")
    plt.close()
    
    # top 1 logistic accuracy
    plt.plot(average_hwks[ind], top_1_acc_log[ind])
    plt.xlabel("Average Number of Hawkes Events (log)")
    plt.ylabel('top 1 correct')
    plt.savefig("top_1_sec_log.png")
    plt.close()

    # top 5 logistic accuracy
    plt.plot(average_hwks[ind], top_5_acc_log[ind])
    plt.xlabel("Average Number of Hawkes Events (log)")
    plt.ylabel('top 5 correct')
    plt.savefig("top_5_sec_log.png")
    plt.close()

    # top 10 logistic accuracy
    plt.plot(average_hwks[ind], top_10_acc_log[ind])
    plt.xlabel("Average Number of Hawkes Events (log)")
    plt.ylabel('top 10 correct')
    plt.savefig("top_10_sec_log.png")
    plt.close()


    # r^2 score
    plt.plot(average_hwks[ind], rSquare[ind])
    plt.xlabel("Average Number of Hawkes Events (log)")
    plt.ylabel(r'$R^2$')
    plt.savefig("rSquare_sec.png")
    plt.close()

    # rms
    plt.plot(average_hwks[ind], rms[ind])
    plt.xlabel("Average Number of Hawkes Events (log)")
    plt.ylabel('Root Mean Squared')
    plt.savefig("rms_sec.png")
    plt.close()
    
    # number of hawkes events
    plt.plot(alphas, average_hwks)
    plt.xlabel("Alpha Value")
    plt.ylabel(r'$\log_{10} ($Average Hawkes Events$)$')
    plt.savefig("hawkes_sec.png")
    plt.close()
    
    # test fit to one alpha on all other alphas
    rSquareSpread = []
    thisData = separated_dat[416]
    xTest   = thisData[1]
    yTest   = np.log10(thisData[2])
    xTrain  = thisData[3]
    yTrain  = np.log10(thisData[4])
    model = lm.LinearRegression()
    model.fit(xTrain, yTrain)

    for data in separated_dat:
        if len(data[1]) > 0:
            yData = np.log10(np.append(data[2], data[4]))
            xData = np.append(data[1], data[3], axis=0)
            rSquareSpread.append(max(mt.r2_score(yData, model.predict(xData)), 0))
     
    plt.plot(average_hwks, rSquareSpread)
    plt.xlabel("Average Number of Hawkes Events (log)")
    plt.ylabel(r'$R^2$')
    plt.savefig("rSquareSpread_sec.png")
    plt.close()  

main()
