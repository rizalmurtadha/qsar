import csv
import pandas
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math

def create(name,count):
    df = pandas.read_csv("{}.csv".format(name))
    range_min = min(df[df.columns[0]].min(),df[df.columns[-1]].min())
    range_max = max(df[df.columns[-1]].max(),df[df.columns[-1]].max())

    plt.xlabel('Experimental Values', fontsize=18)
    plt.ylabel('Predicted Values', fontsize=16)
    plt.plot([range_min,range_max],[range_min,range_max],color='black')
    plt.scatter(df[df.columns[0]], df[df.columns[-1]], c='b', label="Train set")
    plt.legend(loc='best')
    plt.title('Model '+str(count+1))
    # plt.show()
    # plt.show()
    plt.savefig('plot_'+str(count+1)+'.png')
    plt.clf()
    plt.close()