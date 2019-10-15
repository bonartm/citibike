import pandas as pd
import sqlite3

def clean_columns(columns):
    columns = columns.str.strip().str.lower().str.replace(' ', '_')
    columns = [c.replace('_station', '') for c in columns]
    columns = [c.replace('latitude', 'lat') for c in columns]
    columns = [c.replace('longitude', 'lon') for c in columns]
    return columns


dat = pd.read_csv("data/NYPD_Motor_Vehicle_Collisions_-_Crashes.csv", low_memory = False)
dat.columns = clean_columns(dat.columns)
dat['date'] = pd.to_datetime(dat['date'])
dat['datetime'] = dat.date + pd.to_timedelta(dat.time+":00")
dat.drop(['date', 'time'], inplace = True, axis = 1)
dat  = dat[dat.datetime.dt.year == 2018]

with sqlite3.connect('citibike.db') as conn:
    dat.to_sql("collisions", conn, if_exists = 'replace', index = False)







