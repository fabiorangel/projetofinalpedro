import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso

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
    #hipoteses
    X.append(x)
    X.append(sen(x))
    X.append(senU2(x))
    X.append(senU3(x))
    X.append(senU4(x))
    X.append(intercept(x))

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

data = np.array(data)
X = np.arange(len(y))

X = transform(X)
sc = StandardScaler()
X = sc.fit_transform(X)
X_train = X[:-12]
X_test = X[-12:]
y_train = data[1][:-12]
y_test = data[1][-12:]

reg = Lasso()
reg.fit(X_train, y_train)
y_pred = reg.predict(X_test)

for i in xrange(len(y_pred)):
    print y_pred[i], y_test[i]