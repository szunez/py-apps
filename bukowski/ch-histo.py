import numpy as np
import pandas as pd
import scipy.special

from bokeh.layouts import gridplot
from bokeh.models import BoxSelectTool, LassoSelectTool
from bokeh.plotting import curdoc, figure, output_file, show

def make_plot(title, hist, edges, x, pdf, cdf):
    p = figure(title=title, tools='', background_fill_color="#fafafa")
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5)
    p.line(x, pdf, line_color="#ff8888", line_width=4, alpha=0.7, legend_label="PDF")
    p.line(x, cdf, line_color="orange", line_width=2, alpha=0.7, legend_label="CDF")

    p.y_range.start = 0
    p.legend.location = "center_right"
    p.legend.background_fill_color = "#fefefe"
    p.xaxis.axis_label = 'x'
    p.yaxis.axis_label = 'Pr(x)'
    p.grid.grid_line_color="white"
    return p
def update(attr, old, new):
    inds = new
    if len(inds) == 0 or len(inds) == len(x):
        hhist1 = hzeros
    else:
        neg_inds = np.ones_like(x, dtype=np.bool)
        neg_inds[inds] = False
        hhist1, _ = np.histogram(x[inds], bins=hedges)

    hh1.data_source.data["top"]   =  hhist1

dataFile = './data/toc.csv'
data = pd.read_csv(dataFile)

duration = pd.DatetimeIndex(data['Length (hh:mm:ss)'])

y = duration.hour * 3600 + duration.minute * 60 + duration.second
#y = y.sort_values()
print('\n========================================================================')
print(data['Title'][0]+' by '+data['Author'][0]+', published in '+str(int(data['Published'][0])))
print('The mean chapter length is '+str(int(np.mean(y)/60))+' minutes')
print('Chapters range from '+str(int(np.min(y)/60))+' to '+str(int(np.max(y)/60))+' minutes')
print('========================================================================\n')

#wantCh = input('Would you like to see the chapter titles (yes/no)? :')
#loadedData = None
#if wantCh[0]=='y' and loadedData==False:
#    print(data['Chapter'])
#    loadedData = True
#else :

#x = [n for n in range(len(y))]

# Normal Distribution

mu, sigma = 0, 0.5

measured = np.random.normal(mu, sigma, 1000)
hist, edges = np.histogram(measured, density=True, bins=50)

x = np.linspace(-2, 2, 1000)
pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2 / (2*sigma**2))
cdf = (1+scipy.special.erf((x-mu)/np.sqrt(2*sigma**2)))/2

p1 = make_plot("Normal Distribution (μ=0, σ=0.5)", hist, edges, x, pdf, cdf)
#output_file(data['Author']+'.html', title=data['Title'])

show(gridplot([p1], ncols=1, plot_width=600, plot_height=600, toolbar_location=None))
#print(x,measured)
