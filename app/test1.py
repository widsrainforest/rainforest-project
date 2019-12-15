styles = {
    'pre': {
        'border': 'grey',
        'overflowX': 'scroll'
    }
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# UPLOAD_DIRECTORY= '/downloads/wids/app_uploaded_files'

# if not os.path.exists(UPLOAD_DIRECTORY):
#     os.makedirs(UPLOAD_DIRECTORY)

# @server.route("/download/<path:path>")
# def download(path):
#     return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)
    
df = make_dataset.load_raw_labels()
df = df[:100].copy()

df = make_dataset.add_random_lat_lon(df, [-3, -62])
tags = df['tags']

fig = go.Figure(data=go.Scattergeo(
#         locationmode = 'USA-states',
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

for tags, data in tags.items():
    fig.add_trace(go.Scatter(
        x=df['lat'],
        y=df['lon'],
        name=tags,
        text=df['tags'],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "GDP per Capita: %{y:$,.0f}<br>" +
        "Life Expectation: %{x:.0%}<br>" +
        "Population: %{marker.size:,}" +
        "<extra></extra>",
        ))

fig.update_traces(
    mode='markers',
    marker={'sizemode':'area',
            'sizeref':10})

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
    
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
sys.path.append("..")

from src.app import app_tools
from src.data import make_dataset

models, labels = app_tools.load_models('05_Nov_19_log_reg')

# loads raw image file, turns into a numpy array, and feeds into models to create a prediction
predictions = app_tools.load_predict_image('train_0.jpg', models)

colors={
    'background':'#111111',
    'text':'#7FDBFF'
},

app.layout = html.Div([
    html.Div([
        html.H2(
            children="Amazon Rainforest Satellite Imagery",
            className='banner',
            style={
                'textAlign': 'center',
            },
        ),
    
        html.H5(
            children="Booz Allen WiDS Incubator Challenge",
            className='banner',
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
            className='six columns',
            style={
                'width':'50%',
                'display':'inline-block',
                'textAlign': 'left'},
        ),

        html.Br(),

        html.Label(
            children="Atmosheric Conditions",
            className='six columns',
            style={
                'textAlign': 'left'
            }
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
                    value=['']
                ),
        ],
        style={'width':'50%', 'display':'inline-block'}
        ),

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
                value=['']
            ),
        ],
        style={
            'width':'50%', 'display':'inline-block'},
        ),

        html.Label(
            children="Multi-Select Dropdown",
            style={
                'textAlign': 'left'},
        ),

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
        style={'width':'50%', 'display':'inline-block'}
        ),

        html.H6 ("file"),
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
                data = [dict(zip(labels, [0]*len(labels)))]

    )
    
])

@app.callback(
    Output('table', 'data'),
    [Input('filename_dropdown', 'value')]
)
def update_table(filename):
    predictions = app_tools.load_predict_image(filename, models)
    return [dict(zip(labels, predictions))]

if __name__ == '__main__':
    app.run_server(debug=True)