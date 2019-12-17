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
# import plotly_express as px
import sys
from pathlib import Path
sys.path.append("..")
# from src.app import app_tools
from src.data import make_dataset

styles = {
    'pre': {
        'border': 'grey',
        'overflowX': 'scroll'
    }
}

external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']

# models, labels = app_tools.load_models('05_Nov_19_log_reg')
# predictions = app_tools.load_predict_image('train_0.jpg', models)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Store component to save data in visitor's browser - memory/local/session
# https://dash.plot.ly/dash-core-components/
# store = dcc.Store(id='my-store', data={'my-data': 'data'})

df = make_dataset.load_raw_labels()
df = df[:200].copy()

df = make_dataset.add_random_lat_lon(df, [-3, -62])
tags = df['tags']
print(df.columns)


def make_plot(df):
    fig = go.Figure(data=go.Scattergeo(
            lon = df['lon'],
            lat = df['lat'],
            hovertemplate =
            'Lat: %{lat:.2f} W<br>' +
            'Lon: %{lon:.2f} S',
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
    return fig

first_plot = make_plot(df)

app = dash.Dash(external_stylesheets=external_stylesheets)

def build_banner():
    return html.Div(
        id='banner',
        className='banner',
        children=[
            html.Br(),
            html.H5('WiDS Incubator Challenge'),
        ],
    )

colors={
    'background':'LightGrey',
    'text':'#7FDBFF'
},

app.layout = html.Div(
    children=[
        html.Div(
            id='top-row',
            children=[
                html.Div(
                    className='row',
                    id='top-row-header',
                    children=[
                        html.Div(
                            id='test',
                            children=[
                                build_banner(),
                                html.P(
                                    id='description',
                                    children=[html.H6('Booz Allen WiDS Incubator Challenge'),
                                    ])
                            ],
                            style={
                                "color": "DarkSeaGreen",
                                'backgroundColor': 'black',
                                "textAlign": "center"}
                        ),
                    ]),
    
                html.Div([
                    dcc.Markdown('''
                    ###### Team Objectives and Overview 
                    Use machine learning and remote sensing data from Landsat satellites to identify regions where deforestation has occurred in remote regions; 
                    Label image chips with atmospheric conditions, class cover, and land use;
                    Understand where, how, and why deforestation occurs in the Amazon.
                    This data is from a Kaggle competition called Planet: Understanding the Amazon from Space. [Click here for the link](https://www.kaggle.com/c/planet-understanding-the-amazon-from-space/data).
                                '''
                                ),
                    ], className='row',
                    style={
                        'textAlign': 'middle'},
                ),
        
        html.Br(),
        html.Br(),
                        html.Div([
                            html.Label(children="Select the label(s) below:",
                                    className='row',
                                    # className='four columns',
                                    style={'textAlign': 'left'}),
                            dcc.Dropdown(
                            id='multi_select',
                            className='row',
                                options=[
                                    {'label': 'Partly cloudy', 'value': 'partly_cloudy'},
                                    {'label': 'Cloudy', 'value': 'cloudy'},
                                    {'label': 'Primary', 'value': 'primary'},
                                    {'label': 'Haze','value': 'haze'},
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
                                value=['partly_cloudy', 'cloudy', 'primary', 'haze', 'clear', 'slash_and_burn'
                                    'selective_logging', 'conventional_mining', 'artisinal_mining', 'blooming',
                                    'bare_ground', 'water', 'road', 'agriculture', 'habitation'],
                                multi=True
                                ),
                            ],
                                className='five columns',
                            ),

                        html.Div(
                            className='row',
                            id='dropdown',            
                            children=[
                                html.Div([
                                dcc.Graph(
                                    id='map', 
                                    className='row',
                                    figure=first_plot,
                                    )
                            ],
                                className='five columns',
                                # style={'margin-right':'20'},
                            ),
                                # html.P("Select label(s) below:"),
                                ], style={'padding':'25px'}),
            ]
        ),
                                
        html.Div(  
            id='bottom-row',
            children=[
                html.Div(
                dash_table.DataTable(
                    id = 'table-2',
                    columns = [{'name': i, 'id': i, 'deletable': True} for i in df.columns
                        if i !='id'],
                    data = df.to_dict("rows"),
                    editable=True,
                    filter_action='native',
                    sort_action='native',
                    sort_mode='multi',
                    column_selectable='single',
                    row_deletable=True,
                    row_selectable='multi',
                    selected_rows=[],
                    selected_columns=[],
                    page_action='native',
                    page_current= 0,
                    page_size=15,
                    style_header={'backgroundColor': 'rgb(77,77,77)',
                                'color':'white'},
                    style_cell={
                        'overflow':'hidden',
                        'textOverflow':'ellipsis',
                        'maxWidth':'25px'},
            ),
                ),
            ], 
                className='row',
            ),
        ],
)

@app.callback(
    Output('map', 'figure'),
    [Input('multi_select', 'value')]
)
def new_plot(multi_select):
    print(multi_select)
    indices = []
    for match in multi_select:
        indices = indices + list(df[df.tags.str.contains(match)].index) 
    indices = set(indices)
    indices = list(indices)
    indices.sort()
    test_df = df.loc[indices]

    print(len(test_df))
    return make_plot(test_df)

def generate_table(alltable, max_rows=15):
    return html.Table(
        [html.Tr([html.Th(col) for col in alltable.columns])] +
        [html.Tr([
            html.Td(alltable.iloc[i][col]) for col in alltable.columns
        ]) for i in range(min(len(alltable), max_rows))
        ], className='five columns', style={'margin-top':'30',
                                            'margin-right':'50',
                                            'border':'1px solid #C6CCD5'}
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



