import googlemaps
import pandas as pd
import sqlite3
import numpy as np
import time

with open("key") as f:
    key = f.readline()

gmaps = googlemaps.Client(key=key)

with sqlite3.connect('citibike.db') as conn:     
    dat = pd.read_sql_query("""
        SELECT tripduration, start_lat, 
        start_lon, end_lat, end_lon, starttime 
        FROM trips WHERE usertype = "Subscriber" ORDER BY RANDOM() LIMIT 2000;
    """, conn, parse_dates='starttime')

dat['duration_driving'] = 0
dat['duration_transit'] = 0
dat['duration_driving_traffic'] = 0

dat['starttime_nextweek'] = dat.starttime.apply(
    lambda x: pd.Timestamp(
        year = 2019,
        month = 10,
        day = 21+x.weekday(),
        hour = x.hour,
        minute = x.minute,
        second = x.second))  
    
dat['starttime_unix'] = dat.starttime_nextweek.astype ( np.int64 )/1000000000

def to_geostring(row):
    origin = row[['start_lat', 'start_lon']].to_list()
    dest = row[['end_lat', 'end_lon']].to_list()
    return (','.join(map(str, origin)) , ','.join(map(str, dest)) )

for index, row in dat.iterrows():
    origin, dest = to_geostring(row)
    for mode in ['transit', 'driving']:
        res = gmaps.directions(origin=origin,
                                destination=dest,
                                mode=mode,
                                units="metric",
                                departure_time=row.starttime_unix)
        leg = res[0]['legs'][0]
        if mode == 'transit':
            dat.loc[index, 'duration_transit'] = leg['duration']['value']
        else:
            dat.loc[index, 'duration_driving'] = leg['duration']['value']
            dat.loc[index, 'duration_driving_traffic'] = leg['duration_in_traffic']['value']
        time.sleep(0.02)
    

with sqlite3.connect('citibike.db') as conn:     
    dat.to_sql("routes", conn, if_exists = 'replace', index = False)