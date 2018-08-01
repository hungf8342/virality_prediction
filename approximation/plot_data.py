import sklearn.linear_model as lm
import sklearn.model_selection as ms
import pickle
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sklearn.metrics as mt

D = pickle.load(open("outDataLocal_second_deg.dat", "rb"))

#xData = np.asarray(D[0])#.reshape(-1,1)
xData = np.log10(np.asarray(D[3]).reshape(-1,1))#[np.asarray(range(0, 1000)) * 33, :] #np.append(x2Data, np.asarray(D[0]), axis=1)
yData = np.log10(np.asarray(D[4]))#[np.asarray(range(0, 1000)) * 33]

inds = yData.argsort()

sortX = xData[inds]
sortY = yData[inds]

model = lm.LinearRegression()

xTrain, xTest, yTrain, yTest = ms.train_test_split(xData, yData, test_size=0.3, random_state=64)

model.fit(xTrain, yTrain)
print(mt.r2_score(yTest, model.predict(xTest)))
print(mt.mean_squared_error(yTest, model.predict(xTest)))
print(model.coef_)
print(model.intercept_)
print(np.asarray(model.coef_).argsort())
plt.xlabel("exact # expected Hawkes events")
plt.ylabel("predicted # expected Hawkes events")
plt.title("Local Graphlet Count to Local Expected Hawkes")
plt.plot(yTest, model.predict(xTest), "r.", alpha=0.2, label="Linear Regression")
plt.plot(yTest, yTest, "b-", label="Perfect Prediction")
plt.legend()
plt.savefig("Output.png")
