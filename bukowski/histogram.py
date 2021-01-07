import numpy as np
import scipy.special
import pandas as pd

from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show


def make_plot(title, hist, edges, x, pdf):
    p = figure(title=title, tools='', background_fill_color="#fafafa")
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5)
    p.line(x, pdf, line_color="#ff8888", line_width=4, alpha=0.7, legend_label="PDF")

    p.y_range.start = 0
    p.legend.location = "center_right"
    p.legend.background_fill_color = "#fefefe"
    p.xaxis.axis_label = 'x'
    p.yaxis.axis_label = 'Pr(x)'
    p.grid.grid_line_color="white"
    return p

# Test data to supersede random function generated points
dataFile = './data/toc.csv'
data = pd.read_csv(dataFile)

duration = pd.DatetimeIndex(data['Length (hh:mm:ss)'])

y = duration.hour * 3600 + duration.minute * 60 + duration.second
measured = y.sort_values()

# Normal Distribution
mu, sigma = np.mean(measured), np.var(measured)/1000
hist, edges = np.histogram(measured, density=True, bins=20)
x = np.linspace(np.min(measured)*0.9, np.max(measured)*1.1, 2000)

pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2 / (2*sigma**2))
p1 = make_plot("Normal Distribution (μ=0, σ=0.5)", hist, edges, x, pdf)

# Log-Normal Distribution
mu, sigma = np.mean(measured)*1000, 1
pdf = 1/(x* sigma * np.sqrt(2*np.pi)) * np.exp(-(np.log(x)-mu)**2 / (2*sigma**2))
p2 = make_plot("Log Normal Distribution (μ=0, σ=0.5)", hist, edges, x, pdf)

# Gamma Distribution
k, theta = 7.5, 1000
pdf = x**(k-1) * np.exp(-x/theta) / (theta**k * scipy.special.gamma(k))
p3 = make_plot("Gamma Distribution (k=7.5, θ=1)", hist, edges, x, pdf)

# Weibull Distribution
lam, k = 1, 1.25
pdf = (k/lam)*(x/lam)**(k-1) * np.exp(-(x/lam)**k)
p4 = make_plot("Weibull Distribution (λ=1, k=1.25)", hist, edges, x, pdf)

output_file('histogram.html', title="histogram.py example")

show(gridplot([p1,p2,p3,p4], ncols=2, plot_width=400, plot_height=400, toolbar_location=None))