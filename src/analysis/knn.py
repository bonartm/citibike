from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.preprocessing import StandardScaler
import logging
from sklearn.model_selection import GridSearchCV

logging.basicConfig(filename='log.log',level=logging.INFO, format='%(asctime)s %(message)s')

with sqlite3.connect('citibike.db') as conn:     
    dat = pd.read_sql_query("""
        SELECT
        gender,
        tripduration,
        start_lat,
        start_lon,
        end_lat, 
        end_lon,
        CAST(strftime('%s', starttime) AS INTEGER) AS starttime,
        CASE WHEN usertype="Subscriber" THEN 0 ELSE 1 END AS usertype
        FROM trips
        --ORDER BY RANDOM() LIMIT 2000000
    """, conn)

dat = dat.loc[(dat.tripduration < 7200) & (dat.tripduration > 20)]
y = dat['usertype']
dat.drop('usertype', axis=1, inplace=True)

naive_pred = (dat.gender == 0).astype(int)

score_naive = f1_score(y, naive_pred)
logging.info(f"naive gender score: {score_naive}")

dat.drop('gender', axis=1, inplace=True)

logging.info(f"fetched {len(dat)} datapoints")

scaler = StandardScaler(copy=False)
dat = scaler.fit_transform(dat)

logging.info("scaled data")

X_train, X_test, y_train, y_test = train_test_split(
    dat, y, test_size=0.4, shuffle = True)

logging.info("start classifier")

param_grid = [
  {'n_neighbors': [1, 5, 10, 50, 100]}
 ]

knn = KNeighborsClassifier(
        weights = 'distance', 
        metric = 'minkowski',
        p = 1,
        n_jobs = 8)

clf = GridSearchCV(knn, param_grid, cv=5, scoring = 'f1')
clf.fit(X_train, y_train) 
print(pd.DataFrame(clf.cv_results_ ))
pred = clf.predict(X_test)
score_test = f1_score(y_test, pred)    
logging.info(f"knn, test score: {score_test}")

