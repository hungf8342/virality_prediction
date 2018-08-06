import joint_single as ms
import neighbors_twolevel as up
import casc_gen_graph as cg
import numpy as np
import seaborn as sb
import pandas as pd
import matplotlib.pyplot as plt

#main function for generating data
def data_gen(data,graph,X):
    for i in range(5):
      cg.gen(data,"../orig_graphs/"+graph)
      ms.main_subgraph(data,graph,X)
      up.update(data,[5,10,15,20,25])

def plot_roc(data,tests):
    toplot=pd.DataFrame()
    deg_fin=pd.DataFrame()
    for k in tests:
        rocs=pd.read_csv("../"+str(data)+"/rocGraphs/"+str(k)+str(data)+"reg.txt",sep="\n",header=None).iloc[:35,:]
        degs=pd.read_csv("../"+str(data)+"/centROC/"+str(k)+str(data)+"reg.txt",sep="\n",header=None).iloc[:35,:]
        deg_fin[k]=list(degs.iloc[:,0])
        print(str(k)+"mean(deg): "+str(np.mean(degs.iloc[:,0]))+", std: "+str(np.std(degs.iloc[:,0])))
        toplot[(k)]=list(rocs.iloc[:,0])
        print(str(k)+"mean(graphlets): "+str(np.mean(rocs.iloc[:,0]))+", std: "+str(np.std(rocs.iloc[:,0])))
    toplot=pd.melt(toplot,id_vars=[],var_name=['k'])
    deg_fin=pd.melt(deg_fin,id_vars=[],var_name=['k'])
    toplot["type"]=list("g"*toplot.shape[0])
    deg_fin["type"]=list("d"*toplot.shape[0])
    toplot=toplot.append(deg_fin)
    print(toplot)
    plt.clf()
    ax=sb.boxplot(x=toplot['k'],y=toplot['value'],hue=toplot["type"])
    ax.set_title("AUC scores of Graphlet/Degree-Based Models, "+str(data))
    ax.set_ylabel('AUC')
    ax.set_xlabel('')
    plt.savefig("../"+str(data)+"/rocs.png")
#data_gen("Caltech-X10","socfb-Caltech36.txt",10)
plot_roc("Caltech-X20",[5,10,15,20,25])
