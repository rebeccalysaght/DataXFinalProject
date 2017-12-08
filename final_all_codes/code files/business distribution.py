import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly
import plotly.plotly as py
from plotly.graph_objs import *

data=pd.read_csv('business.csv')
site_lat=data.latitude
plotly.tools.set_credentials_file(username='yiqi-lin', api_key='blW9X599PD6dloPmtBdR')


import pandas as pd

mapbox_access_token = 'pk.eyJ1IjoieWlxaS1saW4iLCJhIjoiY2o4d2o2aDJlMW84ODMycXFndTBibzdjcyJ9.wFroRkgjhCG4DUpakDTXfA'
site_lat = data.latitude
site_lon = data.longitude
locations_name = data.name

data = Data([
    Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=Marker(
            size=17,
            color='rgb(255, 0, 0)',
            opacity=0.7
        ),
        text=locations_name,
        hoverinfo='text'
    ),
    Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=Marker(
            size=8,
            color='rgb(242, 177, 172)',
            opacity=0.7
        ),
        hoverinfo='none'
    )]
)

layout = Layout(
    title='restaurants in yelp in America',
    autosize=True,
    hovermode='closest',
    showlegend=False,
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=38,
            lon=-94
        ),
        pitch=0,
        zoom=3,
        style='light'
    ),
)

fig = dict(data=data, layout=layout)
py.iplot(fig, filename='restaurants in yelp in America')