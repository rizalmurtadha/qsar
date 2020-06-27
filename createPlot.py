import csv
import pandas
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math

def create(name):
    df = pandas.read_csv("{}.csv".format(name))
    range_min = min(df[df.columns[0]].min(),df[df.columns[-1]].min())
    range_max = max(df[df.columns[-1]].max(),df[df.columns[-1]].max())

    plt.xlabel('Experimental '+df.columns[0], fontsize=18)
    plt.ylabel('Predicted '+df.columns[0], fontsize=16)
    plt.plot([range_min,range_max],[range_min,range_max],color='black')
    plt.scatter(df[df.columns[0]], df[df.columns[-1]], c='b', label="Train set")
    plt.legend(loc='best')
    # plt.show()
    # plt.show()
    plt.savefig('plot.jpg')
    plt.clf()
    plt.close()