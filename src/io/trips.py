import boto3
import logging
import pandas as pd
import os
import multiprocessing as mp
import sqlite3

logging.basicConfig(filename='log.log',level=logging.INFO, format='%(asctime)s %(message)s')

BUCKET = 'tripdata'

s3 = boto3.client('s3')
obj = s3.list_objects(Bucket = BUCKET)
keys = [el.get('Key') for el in obj.get('Contents')]
keys = [key for key in keys if '2018' in key]
con = sqlite3.connect("citibike.db")

def clean_columns(columns):
    columns = columns.str.strip().str.lower().str.replace(' ', '_')
    columns = [c.replace('_station', '') for c in columns]
    columns = [c.replace('latitude', 'lat') for c in columns]
    columns = [c.replace('longitude', 'lon') for c in columns]
    return columns

def fetch_and_read(key):
    out = f"./data/{key}"
    if not os.path.isfile(out):
        logging.info(f"download {key} to {out}")
        s3.download_file(Bucket=BUCKET, Key=key, Filename=out)
    logging.info(f"read in {out}")
    dat = pd.read_csv(out)
    dat.columns = clean_columns(dat.columns)    
    logging.info(f"columns: {','.join(list(dat.columns))}, trips: {len(dat)}")
    dat.to_sql("trips", con, if_exists = 'append', index = False)
    return len(dat)

p = mp.Pool(1)
counts = p.map(fetch_and_read, keys)
logging.info(f'{con.execute("SELECT COUNT(*) FROM trips;").fetchone()[0]} in the db')
logging.info(f"{sum(counts)} trips in the csv files")
logging.info(f'min date: {con.execute("SELECT MIN(starttime) FROM trips;").fetchone()[0]}')
logging.info(f'max date: {con.execute("SELECT MAX(starttime) FROM trips;").fetchone()[0]}')
