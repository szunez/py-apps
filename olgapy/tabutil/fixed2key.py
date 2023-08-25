import os
import re
import numpy as np
import pandas as pd

tabfile=input()
# Read the tab-delimited text file into a pandas dataframe
df = pd.read_csv('path/to/your/file.txt', delimiter='\t', header=None)

# Reshape the dataframe into a 1D array
arr = df.values.reshape(-1)

# Display the array
print(arr)