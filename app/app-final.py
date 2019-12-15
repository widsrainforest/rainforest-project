#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'app'))
	print(os.getcwd())
except:
	pass


import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import numpy as np
from dash_core_components import Upload
from dash.dependencies import Input, Output, State
from plotly import graph_objs as go
from plotly.graph_objs import *
import glob
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

external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']

models, labels = app_tools.load_models('05_Nov_19_log_reg')
predictions = app_tools.load_predict_image('train_0.jpg', models)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Store component to save data in visitor's browser - memory/local/session
# https://dash.plot.ly/dash-core-components/
# store = dcc.Store(id='my-store', data={'my-data': 'data'})

df = make_dataset.load_raw_labels()
df = df[:100].copy()

df = make_dataset.add_random_lat_lon(df, [-3, -62])
tags = df['tags']

fig = go.Figure(data=go.Scattergeo(
        lon = df['lon'],
        lat = df['lat'],
        # The idea is to also call upon the image labels and image name within the hover box
        # image = df['image_name'],
        # label = df['label'],
        hovertemplate =
        'Image Name: {lon} <br> Coordinates: {lon} <br> Image Labels: {lat}',
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
        title = 'Locations of Amazon Rainforest Satellite Imagery',
        clickmode='event+select',
        dragmode='select',
        hovermode='closest',
        showlegend=True,
        autosize=True,
        geo = dict(
            scope='south america',
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5,
        ),
        width=500,
        height=500,
        margin=go.layout.Margin(l=25, r=25, b=25, t=75, pad=4),
        plot_bgcolor= 'LightGrey',
        paper_bgcolor='LightGrey'
    )

app = dash.Dash(external_stylesheets=external_stylesheets)

colors={
    'background':'LightGrey',
    'text':'#7FDBFF'
},

app.layout = html.Div([
    dcc.Store(id='aggregate_data'),
    html.Div([
        html.Div([
            html.H2(
                children="Amazon Rainforest Satellite Imagery",
                className='banner',
                style={
                    'textAlign': 'center'}
            ),
        
            html.H5(
                children="Booz Allen WiDS Incubator Challenge",
                className='banner',
                style={
                    'textAlign': 'left',
                    'color':'DarkSeaGreen',
                    'textAlign': 'center',
                },
            )])]),
        
        html.Div([
            dcc.Markdown('''
            ###### Objectives: 
            Use machine learning and remote sensing data from Landsat satellites to identify regions where deforestation has occurred in remote regions; 
            Label image chips with atmospheric conditions, class cover, and land use;
            Understand where, how, and why deforestation occurs in the Amazon.
            This data is from a Kaggle competition called Planet: Understanding the Amazon from Space. [Click here for the link](https://www.kaggle.com/c/planet-understanding-the-amazon-from-space/data).
                        '''
                        ),
            ],
            style={
                'textAlign': 'left'},
        ),
        html.Hr(),
        html.Div([
            html.Label(children="Atmosheric Conditions",
            style={'textAlign': 'left'}
            ),

            html.Div([ 
                dcc.Dropdown(
                    id='dropdown1',
                    options=[
                        {'label': 'Partly cloudy', 'value': 'partly_cloudy'},
                        {'label': 'Cloudy', 'value': 'cloudy'},
                        {'label': 'Hazy','value': 'haze'},
                        {'label': 'Clear', 'value': 'clear'},
                    ],
                        value=[''],
                className='four columns',
                style={'margin-top': '10'}
                ),
            ], className='row'),

            html.Label(
                children="Land Use",
                style={
                    'textAlign': 'left'},
            ),
            html.Div([
                dcc.Dropdown(
                id='dropdown2',
                options=[
                    {'label': 'Slash and Burn', 'value': 'slash_and_burn'},
                    {'label': 'Selective Logging', 'value': 'selective_logging'},
                    {'label': 'Conventional Mining', 'value': 'conventional_mining'},
                    {'label': 'Artisinal Mining', 'value': 'artisinal_mining'},
                ],
                    value=[''],
                className='four columns',
                style={'margin-top': '10'}
                ),
            ], className='row'),
            
            html.Label(
                children="Multi-Select Dropdown",
                style={
                    'textAlign': 'left'}),

            html.Div([
                dcc.Dropdown(
                id='Multi-Select Dropdown',
                    options=[
                        {'label': 'Partly cloudy', 'value': 'partly_cloudy'},
                        {'label': 'Cloudy', 'value': 'cloudy'},
                        {'label': 'Hazy','value': 'haze'},
                        {'label': 'Clear', 'value': 'clear'},
                        {'label': 'Slash and Burn', 'value': 'slash_and_burn'},
                        {'label': 'Selective Logging', 'value': 'selective_logging'},
                        {'label': 'Conventional Mining', 'value': 'conventional_mining'},
                        {'label': 'Artisinal Mining', 'value': 'artisinal_mining'},
                        {'label': 'Blooming', 'value': 'blooming'},
                        {'label': 'Bare Ground', 'value': 'bare_ground'},
                        {'label': 'Water', 'value': 'water'},
                        {'label': 'Road', 'value': 'road'},
                        {'label': 'Agriculture', 'value': 'agriculture'},
                        {'label': 'Habitation', 'value': 'habitation'},
                    ],
                    value=['partly_cloudy', 'cloudy', 'haze', 'clear', 'slash_and_burn'
                        'selective_logging', 'conventional_mining', 'artisinal_mining', 'blooming',
                        'bare_ground', 'water', 'road', 'agriculture', 'habitation'],
                    multi=True
                    ),
                ],
                style={'width':'25%', 'display':'inline-block'}
                )]),

            html.Label(children="Upload Image File(s)",
                style={'textAlign': 'left'}),
        
        html.Div([
            html.Div(id='waitfor'),
                dcc.Upload(
                    id='upload-the-data',
                    children=html.Div(
                    ["Drag and drop or click to select a file to upload."]
                ),
                style={
                    "width": "50%",
                    "height": "50px",
                    "lineHeight": "50px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "boderRadius": "5px",
                    "textAlign": "center",
                    "margin": "10px",
                },
                multiple=True,
            ),
            html.Div(id='output'),

            html.Div([
                dcc.Graph(id='map', figure=fig)
            ]),
        ]
        ),

        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='filename_dropdown',
                    options=[
                        {'label': 'train_0.jpg', 'value': 'train_0.jpg'},
                        {'label': 'train_1.jpg', 'value': 'train_1.jpg'},
                        {'label': 'train_10.jpg', 'value': 'train_10.jpg'},
                        {'label': 'train_11.jpg', 'value': 'train_11.jpg'},
                    ],
                    value='train_0.jpg',
                    style={'width':'50%'}
            ),
                dash_table.DataTable(
                    id = 'table',
                    columns = [{'name':label, 'id':label} for label in labels],
                    data = [dict(zip(labels, [0]*len(labels)))],
                    style_as_list_view=True,
                    style_header={'backgroundColor': 'rgb(30,30,30)'},
                    style_cell={
                        'backgroundColor':'rgb(50,50,50)',
                        'color':'white'
                    },
                )
            ], className='six columns',
            style={'width':'50%'})
        # ]),
       
        #     html.H2(children="Amazon Rainforest Satellite Imagery",
        #         dash_table.DataTable(
        #             id = 'table-2',
        #             columns = [{'name': label, 'id': label} for label in labels],
        #             data = [dict(zip(labels), [0]*len(labels)))],
        #             style_as_li
        #         )
        ])
])

@app.callback(
    Output('table', 'data'),
    [Input('filename_dropdown', 'value')]
)
def update_table(filename):
    predictions = app_tools.load_predict_image(filename, models)
    return [dict(zip(labels, predictions))]

def generate_table(dataframe, max_rows=15):
    return html.Table(
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

if __name__ == '__main__':
    app.run_server(debug=True)
    
''''''
''''''

#%% [markdown]
# # Resource
#%% [markdown]
# ### Plotly Dash Tutorial - Working with table and map (Video 04) - YOUTUBE - https://www.youtube.com/watch?time_continue=1050&v=lu0PtsMor4E&feature=emb_logo
#%% [markdown]
# ### UDEMY COURSE - https://bah.udemy.com/course/interactive-python-dashboards-with-plotly-and-dash/learn/lecture/9570036#overview

#%%



