import os
from pathlib import Path
import statistics
import numpy as np
import scipy.stats
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
fname = os.path.join("data.tpl")
tpl = np.loadtxt(fname, delimiter = ",")
n = tpl.shape[0]
x = tpl[0:n,0]
y = tpl[0:n,1]
slope, intercept, r, *__ = scipy.stats.linregress(x, y)
line = f'Regression line: y={intercept:.2f}+{slope:.2f}x, r={r:.2f}'
fig, ax = plt.subplots()
ax.plot(x, y, linewidth=0, marker='s', label='Data points')
ax.plot(x, intercept + slope * x, label=line)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend(facecolor='white')
plt.show()