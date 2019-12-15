import os
import sys
from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

sys.path.append("..")

from src.app import app_tools
from src.data import make_dataset

models, labels = app_tools.load_models('05_Nov_19_log_reg')

predictions = app_tools.load_predict_image('train_0.jpg', models)

df = make_dataset.load_raw_labels()
df = df[:100].copy()

df = make_dataset.add_random_lat_lon(df, [-3, -62])

fig = go.Figure(data=go.Scattergeo(
#         locationmode = 'USA-states',
        lon = df['lon'],
        lat = df['lat'],
#         text = df['text'],
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
            # colorscale = 'Blues',
            # cmin = 0,
            # color = df['cnt'],
            # cmax = df['cnt'].max(),
#             colorbar_title="Incoming flights<br>February 2011"
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

styles = {
    'pre': {
        'border': 'grey',
        'overflowX': 'scroll'
    }
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
colors={
    'background':'#111111',
    'text':'#7FDBFF'
},

app.layout = html.Div([
    
    
    dcc.Dropdown(
            id='filename_dropdown',
            options=[
                {'label': 'train_0.jpg', 'value': 'train_0.jpg'},
                {'label': 'train_1.jpg', 'value': 'train_1.jpg'},
                {'label': 'train_2.jpg', 'value': 'train_2.jpg'},
                {'label': 'train_3.jpg', 'value': 'train_3.jpg'},
            ],
                value=['train_0.jpg']
            ),
    dcc.Graph(id='map', figure=fig)
    
])

if __name__ == '__main__':
    app.run_server(debug=True)