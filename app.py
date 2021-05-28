import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cyborg/bootstrap.min.css']
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}], external_stylesheets=external_stylesheets)
app.title = 'Protest Index'
server = app.server

df = pd.read_csv('https://raw.githubusercontent.com/orectique/protestindex/main/Factors.csv')

available_countries = df['Country'].unique()

app.layout = html.Div([
    html.H1(children='Protest Index'),
    html.Div(children='''
        A way to compare the magnitudes of protests around the world across years.
        Choose the list of countries you would like to see and set the range of years.
    '''),
    html.Div([
    dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in available_countries],
                value= ['Afghanistan', 'Japan'],
                multi = True,
                clearable=False
            ),

    ],style={'width': '48%', 'float': 'left', 'display': 'inline-block', 'padding': '25px 30px 25px 35px'}),

    html.Div([
        dcc.Graph(id='indicator-graphic')
        ],style={'width': '100%', 'float': 'right', 'display': 'inline-block', 'padding': '25px 30px 25px 30px'}),

    html.Div([dcc.RangeSlider(
        id='year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=[df['Year'].min(), df['Year'].max()],
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    )
    ], style={'width': '50%', 'float': 'initial', 'display': 'inline-block', 'padding': '25px 30px 25px 35px'})
])

#style={'width': '45%', 'float': 'right', 'display': 'inline-block'})

@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('country', 'value'),
    Input('year--slider', 'value'))
def update_graph(country_names, year_value):
    year_list = list( i for i in range(year_value[0], year_value[1] + 1))
    df1 = df[df['Country'].isin(list(country_names))]
    dff = df1[df1['Year'].isin(year_list)]
    fig = px.scatter(dff, x="Factor1", y="Factor2", template = 'plotly_dark', color = 'Country', hover_data=['Year'])
    

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
