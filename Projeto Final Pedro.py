import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso
import matplotlib.pyplot as plt
from sklearn.svm import SVR


class CounterRadarRegressor:
    def __init__(self, binlist, norm=True):
        self.binlist = binlist
        self.reg = Lasso()
        self.norm = norm

    def fit(self, x,y):
        X = self.transform(x)

        if self.norm:
            self.sc = StandardScaler()
            X = self.sc.fit_transform(X)

        self.reg.fit(X, y)

    def predict(self, x):
        X = self.transform(x)
        if self.norm:
            X = self.sc.transform(X)

        return self.reg.predict(X)
    
    def sen(self, x):
        return np.sin(x)
    def senU2(self, x):
        return np.sin(x/2)
    def senU3(self, x):
        return np.sin(x/3)
    def senU4(self, x):
        return np.sin(x/4)
    def intercept(self, x):
        return np.ones(len(x))

    def transform(self, x):
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
            X.append(x**2)

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

regressao = CounterRadarRegressor([1,1,1,1,1,1], norm=True)
data = np.array(data)

y_train = data[4][:10]
y_test = data[4][10:]


X_train = np.arange(len(y_train))
X_test = np.arange(len(y_train), len(y_train) + len(y_test))



regressao.fit(X_train, y_train)
ypred = regressao.predict(X_test)


ytrain_pred = regressao.predict(X_train)
plt.plot(X_train, y_train)
plt.plot(X_train, ytrain_pred)
plt.show()

plt.plot(X_test, y_test)
plt.plot(X_test, ypred)
plt.show()