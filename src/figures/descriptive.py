import pandas as pd
import sqlite3
import plotly.figure_factory as ff
import plotly.offline
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# User Type (Customer = 24-hour pass or 3-day pass user; Subscriber = Annual Member)
# Gender (Zero=unknown; 1=male; 2=female)

options = {
    "template": 'presentation+plotly_dark', 
    "autosize":True
}

with sqlite3.connect('citibike.db') as conn:
    trips = pd.read_sql_query("""
    SELECT tripduration,     
    gender, 
    2018-birth_year AS age, 
    usertype, 
    CAST(strftime('%w', starttime) AS INTEGER) AS weekday,
    CAST(strftime('%m', starttime) AS INTEGER) AS month,
    CAST(strftime('%H', starttime) AS INTEGER) hour
    FROM trips 
    """, conn)

trips = trips.loc[(trips.tripduration < 7200) & (trips.tripduration > 20)]

print()

trips.gender.replace({0:'unknown', 1:'male', 2:'female'}, inplace = True)


trips_small = trips.sample(frac = 0.02)

usertypes = trips.usertype.unique()
hist_data_duration = []
hist_data_age = []

for utype in usertypes:
    hist_data_duration.append(trips_small.tripduration.loc[trips_small.usertype == utype])
    hist_data_age.append(trips_small.age.loc[trips_small.usertype == utype])

fig = ff.create_distplot(hist_data_duration, usertypes, show_rug=False, show_hist=True, show_curve=True, bin_size=50)
fig.update_layout(**options, xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text="tripduration (in sec)")))
plotly.offline.plot(fig, filename='docs/figures/tripduration.html')

fig = ff.create_distplot(hist_data_age, usertypes, show_rug=False, show_hist=True, show_curve=True, bin_size=5)
fig.update_layout(**options,  xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text="age")))
plotly.offline.plot(fig, filename='docs/figures/age.html')


fig = make_subplots(
    rows=1, cols=2, 
    specs=[[{"type": "domain"}, {"type": "domain"}]],
    subplot_titles=(usertypes[0], usertypes[1]))

for ind, utype in enumerate(usertypes):
    values = trips[trips.usertype == utype].gender.value_counts().sort_values().reset_index()
    labels = values['index']
    values = values.gender
    fig.add_trace(go.Pie(labels=labels, values=values, hole=.4, name=utype),row=1, col=ind+1)

fig.update_layout(**options)
plotly.offline.plot(fig, filename='docs/figures/gender.html')

for name in ['weekday', 'month', 'hour']:
    dat = trips.groupby(['usertype', name]).tripduration.count().reset_index()
    dat = dat.rename(columns={"tripduration": "#trips"})
    fig = px.bar(dat, x=name, y="#trips", color="usertype", barmode='group', height=500)
    fig.update_layout(**options)
    plotly.offline.plot(fig, filename=f'docs/figures/{name}.html')