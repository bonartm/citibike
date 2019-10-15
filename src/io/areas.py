import googlemaps
import pandas as pd
import sqlite3
import time
import logging

logging.basicConfig(filename='log.log',level=logging.INFO, format='%(asctime)s %(message)s')

with open("key") as f:
    key = f.readline()

gmaps = googlemaps.Client(key=key)

with sqlite3.connect('citibike.db') as conn:
    df = pd.read_sql_query("""
        SELECT DISTINCT start_lat AS lat, start_lon AS lon from trips
        UNION
        SELECT DISTINCT end_lat AS lat, end_lon AS lon from trips""", conn)

logging.info(f"fetched {len(df)} rows")

def get_area(row):
    result_type = "neighborhood|sublocality|locality"
    res = gmaps.reverse_geocode(row, result_type = result_type)
    loc = [el['address_components'][0]['long_name'] for el in res]
    time.sleep(0.05)
    if len(loc) > 0:
        return loc[0]
    else:
        logging.warning(f"no location found for {row}")
        return None
  
df['area'] = df.apply(get_area, axis=1)

df['area_id'] = df['area'].rank(method = 'min')

logging.info(f"write to db")

with sqlite3.connect('citibike.db') as conn:
    df.to_sql("areas", conn, if_exists = 'replace', index = False)