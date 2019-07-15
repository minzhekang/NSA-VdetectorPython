import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.feature_selection import VarianceThreshold

file = ""
df = pd.read_excel(file)
df = df.drop([" Timestamp" , "Normal/Attack"], axis = 1)

selector = VarianceThreshold()
selector.fit_transform(df)

print(selector.variances_)

