import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso


class CounterRadarRegressor:
    def __init__(self, binlist):
        self.binlist = binlist
        self.reg = Lasso()

    def fit(x,y):
        X = self.transform(x)
        return self.reg.fit(x, y)

    def predict(x):
        X = self.transform(x)
        return self.reg.predict(x)
    
    def sen(x):
        return np.sin(x)
    def senU2(x):
        return np.sin(x/2)
    def senU3(x):
        return np.sin(x/3)
    def senU4(x):
        return np.sin(x/4)
    def intercept(x):
        return np.ones(len(x))

    def transform(x):
        X = []
        if self.binlist[0] == 1:
            X.append(x)
        if self.binlist[1] == 1:
            X.append(self.sen(x))
        if self.binlist[2] == 1:
            X.append(self.senU2(x))
        if self.binlist[3] == 1:
            X.append(self.senU3(x))
        if self.binlist[4] == 1:
            X.append(self.senU4(x))
        if self.binlist[5] == 1:
            X.append(self.intercept(x))

        X = np.array(X)
        return X.T


f = open("BASE.csv")

header = f.readline()
data = []

for item in f:
    item = item.split(',')[17:]
    y = []
    for i in xrange(len(item)):
        item[i] = float(item[i])
        y.append(item[i])
    data.append(y)

regressao = CounterRadarRegressor([1,1,1,1,1,1])
data = np.array(data)
X = np.arange(len(y))

sc = StandardScaler()
X = sc.fit_transform(X)
