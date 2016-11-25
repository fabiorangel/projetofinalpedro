import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso


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

data = np.array(data)
X = np.arange(len(y))

sc = StandardScaler()
X = sc.fit_transform(X)


class CounterRadarRegressor:
    def __init__(self, binlist):
        self.binlist = binlist
        self.reg = Lasso()

    def fit(x,y):
        X = self.transform(x)
        self.reg.fit(X_train, y_train)

    def predict(x):
        X_train = X[:-12]
        X_test = X[-12:]
        y_train = data[1][:-12]
        y_test = data[1][-12:]
        y_pred = self.reg.predict(X_test)
        return y_test, y_pred
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
            X.append(sen(x))
        if self.binlist[2] == 1:
            X.append(senU2(x))
        if self.binlist[3] == 1:
            X.append(senU3(x))
        if self.binlist[4] == 1:
            X.append(senU4(x))
        if self.binlist[5] == 1:
            X.append(intercept(x))

        X = np.array(X)
        return X.T

    
for i in xrange(len(y_pred)):
    print y_pred[i], y_test[i]
