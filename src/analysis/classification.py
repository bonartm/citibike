import pandas as pd
import sqlite3
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import logging 

logging.basicConfig(filename='log.log',level=logging.INFO, format='%(asctime)s %(message)s')

def dummy_mat(dat, name):
            one_hot = pd.get_dummies(dat[name], prefix = name, drop_first=True, sparse = False)
            dat.drop(name, axis=1, inplace = True)
            return dat.join(one_hot)
            

with sqlite3.connect('citibike.db') as conn:     
    dat = pd.read_sql_query("""
        SELECT
        tripduration,
        gender,
        2018 - birth_year AS age,
        CASE WHEN 2018 - birth_year=49 THEN 1 ELSE 0 END AS close_to_fifty,
        CAST(strftime('%w', starttime) AS INTEGER) AS weekday,
        CAST(strftime('%m', starttime) AS INTEGER) AS month,
        CAST(strftime('%H', starttime) AS INTEGER) hour,
        area_id,
        CASE WHEN usertype="Subscriber" THEN 0 ELSE 1 END AS usertype
        FROM trips
        INNER JOIN areas ON start_lat = lat AND start_lon = lon
        ORDER BY RANDOM() LIMIT 1000000
        """, conn)

dat = dat.loc[(dat.tripduration < 7200) & (dat.tripduration > 20)]
y = dat['usertype']
dat.drop('usertype', axis=1, inplace=True)

logging.info(f"fetched {len(dat)} random datapoints")

for name in ['gender', 'weekday', 'month', 'hour', 'area_id']:
     dat = dummy_mat(dat, name)

logging.info(f"data has {len(dat.columns)} features")

scaler = StandardScaler(copy=False)
dat = scaler.fit_transform(dat)
X_train, X_test, y_train, y_test = train_test_split(
    dat, y, test_size=0.4, shuffle = True)
logging.info(f"prepared train and test data")

clfs = [
    LogisticRegressionCV(
        scoring = "f1",
        Cs = 10,
        cv = 5,
        solver='saga', 
        class_weight=None, 
        max_iter=100000,
        n_jobs = 6),
    RandomForestClassifier(
        n_estimators=400, 
        max_depth=20,
        n_jobs=7)
]

for clf in clfs:
    name = type(clf).__name__
    clf.fit(X_train, y_train)
    logging.info(f"training finished for {name}")
    pred_test = clf.predict(X_test)
    pred_train = clf.predict(X_train)
    score_test = f1_score(y_test, pred_test)
    score_train = f1_score(y_train, pred_train)
    logging.info(f"name: {name}, test: {score_test}, train: {score_train}")

