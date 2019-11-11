import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import csv

x = []
y = []
a = 0.5

with open('out.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(int(row[0]))
        y.append(int(row[1]))

def func(x, b, c):
    return c/(x+b)**a

popt, pcov = curve_fit(func, x, y)
plt.plot(x, func(x, *popt), 'r-', label='fit')
