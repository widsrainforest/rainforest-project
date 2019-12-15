import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash_core_components import Upload
from dash.dependencies import Input, Output, State
from plotly import graph_objs as go
from plotly.graph_objs import *
import base64
import os
import plotly_express as px
import sys
from pathlib import Path
sys.path.append("..")
from src.app import app_tools
from src.data import make_dataset

styles = {
    'pre': {
        'border': 'grey',
        'overflowX': 'scroll'
    }
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = make_dataset.load_raw_labels()
df = df[:100].copy()

df = make_dataset.add_random_lat_lon(df, [-3, -62])

fig = go.Figure(data=go.Scattergeo(
        lon = df['lon'],
        lat = df['lat'],
        mode = 'markers',
        marker = dict(
            size = 4,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'square',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
        )))

fig.update_layout(
        title = 'Random lat lon in South America',
        geo = dict(
            scope='south america',
#             projection_type='albers usa',
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5
        ),
    )
    
app = dash.Dash(external_stylesheets=external_stylesheets)

colors={
    'background':'#111111',
    'text':'#7FDBFF'
},

app.layout = html.Div([
    html.H2(
        children="Amazon Rainforest Satellite Imagery",
        className='banner',
        style={
            'textAlign': 'center',
        },
               
    ),
    
    html.H5(
        children="Booz Allen WiDS Incubator Challenge",
        style={
            'textAlign': 'center',
            'width': '100%',
            'height': '50px',
            'lineHeight': '50px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
        },
    ),
    
    html.Div([
        dcc.Markdown('''
        ###### Objectives: 
        (1) Empower the user to understand the landscape of deforestation in the Amazon and adjust imagery collection, (2) Use machine learning and remote sensing data from Landsat satellites to identify regions where deforestation has occurred in remote regions; 
        Label image chips with atmospheric conditions, class cover, and land use.
        This data is from a Kaggle competition called Planet: Understanding the Amazon from Space. [Access the link here.](https://www.kaggle.com/c/planet-understanding-the-amazon-from-space/data).
                    '''
                    ),
        ],
        style={
            'textAlign': 'left'},
    ),
    
    html.Div([
        dcc.Graph(id='map', figure=fig)
    ])
])

if __name__ == '__main__':
    app.run_server()