import sklearn.linear_model as lm
import sklearn.model_selection as ms
import pickle
import numpy as np
import matplotlib.pyplot as plt
import sklearn.metrics as mt

D = pickle.load(open("outDataLocal_dolph.dat", "rb"))

xData = np.asarray(D[0])
yData = np.log10(np.asarray(D[1]))

inds = yData.argsort()

sortX = xData[inds]
sortY = yData[inds]

model = lm.LinearRegression()

xTrain, xTest, yTrain, yTest = ms.train_test_split(xData, yData, test_size=0.3, random_state=64)

model.fit(xTrain, yTrain)
print(model.score(xTest, yTest))
print(mt.r2_score(yTest, model.predict(xTest)))
print(model.coef_)
print(np.asarray(model.coef_).argsort())
plt.plot(yTest, model.predict(xTest), "r.", alpha=0.2)
plt.plot(yTest, yTest, "b-")
plt.show()
