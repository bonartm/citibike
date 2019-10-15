import pandas as pd
import numpy as np
import sqlite3
from scipy.stats import ttest_ind, median_test, ks_2samp, ttest_rel, wilcoxon

with sqlite3.connect('citibike.db') as conn:
    dat = pd.read_sql_query("SELECT * FROM routes", conn)

cols = ['tripduration', 'duration_driving', 'duration_driving_traffic', 'duration_transit']

dat = dat.loc[(dat.tripduration < 7200) & (dat.tripduration > 20)]


print(np.round([np.mean(dat[name]- dat.tripduration) for name in cols[1:]],2))
print(np.round([np.median(dat[name] - dat.tripduration) for name in cols[1:]],2))

print([round(sum((dat.tripduration-dat[name]) < 0)/len(dat),2)*100 for name in cols[1:]])


print([round(wilcoxon(dat[cols[0]], dat[name])[1],2) for name in cols[1:]])
print([round(ttest_rel(dat[cols[0]], dat[name])[1],2) for name in cols[1:]])

