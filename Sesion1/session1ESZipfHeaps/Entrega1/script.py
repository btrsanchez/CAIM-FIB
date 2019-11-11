import matplotlib
#matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import csv
import numpy as np


def func(x, b, c):
    return c/(x+b)**a


x = []
y = []
a = 0.99

with open('outZIPS.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(int(row[0]))
        y.append(int(row[1]))

popt, pcov = curve_fit(func,x,y)
print('Zipf\'s optimal parameters:')
print('b = %d, c = %d' % (popt[0],popt[1]))
fitArray = []
logFitArray = []
for num in x:
    fitArray.append(func(num, *popt))
    logFitArray.append(np.log(func(num, *popt)))

logx = np.log(x)
logy = np.log(y)

plt.plot(x, y, label='Original Frequencies')
plt.plot(x, fitArray, label='Zipf law')
plt.xlabel('Rank of the word')
plt.ylabel('Frequency of the word')
plt.legend()
plt.show()

