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
from dash.dependencies import Input, Output, State
from plotly import graph_objs as go
from plotly.graph_objs import *
import glob
import base64
import os
import sys
from pathlib import Path
sys.path.append("..")
from src.data import make_dataset

styles = {
    'pre': {
        'border': 'grey',
        'overflowX': 'scroll'
    }
}

external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# creates new dataset for images and labels (capped at 1000 images)
df = make_dataset.load_raw_labels()
df = df[:1000].copy()

# assigns random latitude and longitude coordinates around a central point geographically located in the Amazon Rainforest
# creates a new column for coodinates in the new dataframe and address lack of geotagged Kaggles image files
df = make_dataset.add_random_lat_lon(df, [-3, -62])
tags = df['tags']
print(df.columns)

# creates a scatterplot figure overlay of South America continent 
# adds hovertip functionality and square markers for geotagged image points
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

# sets basic design layout with a banner title and colors
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
                    The WiDS Incubator Amazon Rainforest Satellite Imagery team is using machine learning and remote sensing data on Landsat images to identify regions where deforestation has occurred and understand potential factors behind it; 
                    The original intent was to allow users to batch upload images and run predictive analytics to label the images with appropriate labels, describing atmospheric conditions, class cover, or land use.
                    While we are still undergoing GUI development, we have successfully geotagged images for this demonstration and connected interactive filters to help a user analyze the data.
                    This data is from a Kaggle competition called Planet: Understanding the Amazon from Space. [Please see here for more information](https://www.kaggle.com/c/planet-understanding-the-amazon-from-space/data).
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
                            ),
                                ], style={'padding':'25px'}),
            ]
        ),

        # creates a data table for users to filter based on preferred label attributes                   
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
                        'maxWidth':'50px'},
            ),
                ),
            ], 
                className='row',
            ),
        ],
)
# creates call backs between the map and the attributes selected in the dropdown function
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
        ],
    )

if __name__ == '__main__':
    app.run_server(debug=True)