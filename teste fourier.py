import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from oselm import OSELMClassifier
from sklearn.neural_network import MLPClassifier

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

for i in range(len(data)):
    y_train = data[i][:60]
    y_test = data[i][60:]


    X_train = [[x] for x in np.arange(len(y_train))]
    X_test = [[x] for x in np.arange(len(y_train), len(y_train) + len(y_test))]


    fourier = np.fft.fft(y_train)
    n = fourier.size
    timestep = 1
    print np.fft.fftfreq(n, d=timestep)

    plt.plot(X_train, y_train)
    plt.plot(X_train, fourier)
    plt.show()