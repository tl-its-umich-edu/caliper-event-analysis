## Python verson 3.6
## Replace the items in <> before running


import pandas as pd
data = pd.read_csv('<file_name>.csv', usecols=[<column_index, column_index, ...>]) # specifiy the dimensions to use in IsolationForest outlier detection


# Use the following chunk if want to use log value of a column
# ------------------------------------------------------------
from math import log

def cal_log(x):
    if x == 0:
        return 0
    else:
        return log(x)

data['<column_name>'] = list(map(cal_log, data['<column_name>']))
# ------------------------------------------------------------


from sklearn.ensemble import IsolationForest
ilf = IsolationForest(contamination=0.05) # Consider 5% of the data as "outliers", default value 0.1
ilf.fit(data) # Fit the model
data['target'] = ilf.predict(data) # Unsupervised learning and predicting outliers
data.to_csv('outliers.csv', columns=["target",], header=False)
