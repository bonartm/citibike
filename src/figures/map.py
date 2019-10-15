import folium
import json
import sqlite3
import pandas as pd
from folium.plugins import HeatMap, HeatMapWithTime
import numpy as np


with sqlite3.connect('citibike.db') as conn:
    dat = pd.read_sql_query("""
        SELECT start_lat, start_lon, starttime, usertype from trips""", conn)

dat.starttime = pd.to_datetime(dat.starttime)
dat['hour'] = dat.starttime.dt.hour

dat = dat.groupby(['hour', 'usertype', 'start_lat', 'start_lon']).starttime.count().reset_index()
dat.starttime = np.log(dat.starttime)
dat.starttime = (dat.starttime-dat.starttime.min())/(dat.starttime.max()-dat.starttime.min())

heat_customer = [
    dat[(dat.usertype == 'Customer') & (dat.hour == hour)].copy()[
        ['start_lat', 'start_lon', 'starttime']
    ].values.tolist() for hour in range(24)]

heat_subscriber = [
    dat[(dat.usertype == 'Subscriber') & (dat.hour == hour)].copy()[
        ['start_lat', 'start_lon', 'starttime']
    ].values.tolist() for hour in range(24)]


m = folium.Map(
    location=[40.761625, -73.977693],
    tiles='Stamen Toner',
    zoom_start=12
)

HeatMapWithTime(name = "Subscriber (red)", show = True, max_opacity=0.8, min_opacity=0.4,
    data=heat_subscriber, scale_radius = False, use_local_extrema = False, 
    auto_play=True, gradient={.0: '#fffbd5', 1: '#b20a2c'}, radius = 15
    ).add_to(m)

HeatMapWithTime(name = "Customer (blue)", show = True, max_opacity=0.8, min_opacity=0.4,
    data=heat_customer, scale_radius = False, use_local_extrema = False, 
    auto_play=True, gradient={.0: '#3a7bd5', 1: '#3a6073'}, radius = 15
    ).add_to(m)

folium.LayerControl(position='bottomright', collapsed=False).add_to(m)


m.save('docs/map.html')