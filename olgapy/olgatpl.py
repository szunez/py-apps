import os
from pathlib import Path
import numpy as np
import scipy.stats
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def get_tpl_list() :
    with open('test-small.tpl') as f :
        global tplvars
        global tpldata
        tpllines = f.readlines()
        i = 0
        linecatalog = 0
        while linecatalog < 1 :
            for val in list(tpllines) :
                if val[:len('CATALOG')] == 'CATALOG' :
                    linecatalog = i
                i = i + 1
        tplvarsraw = tpllines[linecatalog + 2:linecatalog + 2 + int(tpllines[linecatalog + 1])]      
        tplvarsraw.insert(0,tpllines[linecatalog + 2 + int(tpllines[linecatalog + 1])])
        tplvars = []
        for var in tplvarsraw :
            tplvars.append(var.strip())
        tpldataraw = tpllines[linecatalog + 3 + int(tpllines[linecatalog + 1]):]
        tpldata = []
        for var in tpldataraw :
            tpldata.append(var.strip())
    f.close()
def get_trenddata() :
    with open('test.tpl') as f :
        global tplvars
        global tpldata
        tpllines = f.readlines()
        i = 0
        linecatalog = 0
        while linecatalog < 1 :
            for val in list(tpllines) :
                if val[:len('CATALOG')] == 'CATALOG' :
                    linecatalog = i
                i = i + 1
        f.close()
        tplvars = np.genfromtxt('test.tpl', delimiter='\n', dtype=str, skip_header=linecatalog + 2, max_rows=int(tpllines[linecatalog + 1]))
        tpldata = np.genfromtxt('test.tpl', delimiter=' ',skip_header=linecatalog + 3 + int(tpllines[linecatalog + 1]))
        tplvarsraw = tpllines[linecatalog + 2:linecatalog + 2 + int(tpllines[linecatalog + 1])]      
        tplvarsraw.insert(0,tpllines[linecatalog + 2 + int(tpllines[linecatalog + 1])])
        tplvars = []
        for var in tplvarsraw :
            tplvars.append(var.strip())
def show_plt() :
    plt.style.use('ggplot') #theme for matplotlib
    sns.set_theme(style="ticks") #theme for seabord
    fname = os.path.join("data.tpl")
    tpl = np.loadtxt(fname, delimiter = ",")
    n = tpl.shape[0]
    t = tpl[0:n,0]
    y = tpl[0:n,1]
    slope, intercept, r, *__ = scipy.stats.linregress(t, y)
    line = f'Regression line: y={intercept:.2f}+{slope:.2f}x, r={r:.2f}'
    fig, ax = plt.subplots()
    ax.plot(t, y, linewidth=0, marker='s', label='Data points')
    ax.plot(t, intercept + slope * t, label=line)
    ax.set_xlabel('time [ s ]')
    ax.set_ylabel('y')
    ax.legend(facecolor='white')
    plt.show()
def show_sns(data) :
    sns.set_theme(style="whitegrid")
    for var in list(data.columns[1:]) :
        sns.lineplot(data=data, x=data.iloc[:,0], y=data[var], legend="full", linewidth=2.5)
    plt.show()
get_trenddata()
trends = [0,5,6,7,8,9]
df = pd.DataFrame(tpldata, columns=tplvars)
show_sns(df.iloc[:, lambda df: trends])