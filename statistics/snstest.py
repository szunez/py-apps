import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")
tips = sns.load_dataset("tips")
print(tips)
sns.relplot(x="total_bill", y="tip", data=tips)
plt.show()