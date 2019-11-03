import os
import sys
from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

sys.path.append("..")

from src.app import app_tools
from src.data import make_dataset

models, labels = app_tools.load_models('02_Nov_19_log_reg')

predictions = app_tools.load_predict_image('train_0.jpg', models)

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
            )
    
])

if __name__ == '__main__':
    app.run_server(debug=True)