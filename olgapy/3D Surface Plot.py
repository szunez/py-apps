# 3D Surface Plot
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
import numpy as np

path = 'P:/000347 Cheniere - SPLNG Dual Loading with Pump Trips/simulations/ModifiedAllTanks/Phase1_2_12K_seg_ESD1_Trip_4_Pumps_Each_Phase_CSrate05_python/'
data = pd.read_csv(path + 'profile_data.csv').astype(np.float16)
data = data.rename(columns={'Unnamed: 0': 'Index'})
data = data.set_index('Index')
data_archive = data.copy()
data.dtypes
data.describe()
data.columns
data.memory_usage(index=True, deep=True).sum()
data = data[(data.time > 30) & (data.time < 45)]

x_ = data['dist'].to_numpy()
y_ = data['time'].to_numpy()
z_ = data['pressure'].to_numpy()
zip_data = data.groupby('time').apply(lambda x: dict(zip(x.dist, x.pressure)))


time_array = list(zip_data.index)
dist_array = list(zip_data[time_array[0]].keys())
numpy_data = np.empty([len(time_array), len(dist_array)])

for i in range(len(time_array)):
    for j in range(len(dist_array)):
        numpy_data[i,j] = zip_data[time_array[i]][dist_array[j]]
profile_data = pd.DataFrame(numpy_data, columns=dist_array, index=time_array)
profile_data['time'] = profile_data.index
temp = profile_data.pop('time')
profile_data.insert(0,'time',temp)

fig = go.Figure(data=[go.Surface(x=dist_array, y=time_array, z=profile_data)])
fig.update_layout(title='ColSep Visualization', autosize=False,
                  width=1000, height=1000,
                  margin=dict(l=65, r=50, b=65, t=90))
fig.show()