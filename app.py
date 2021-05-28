import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
import random

external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cyborg/bootstrap.min.css']
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}], external_stylesheets=external_stylesheets)
app.title = 'Protest Index'
server = app.server

df = pd.read_csv('https://raw.githubusercontent.com/orectique/protestindex/main/Factors.csv')

available_countries = df['Country'].unique()
rand_country = random.choice(available_countries)

app.layout = html.Div([
    
    html.Div(
            [  dcc.Markdown(
                            """
                ### Quantifying events of Social Unrest:
                
                ### Protest Index
                """.replace(
                                "  ", ""
                            ),
                            className="title",
                        ),
                        dcc.Markdown(
                            """This interactive report is a rendition of a study by Sreehari P Sreedhar.""".replace(
                                "  ", ""
                            ),
                            className="subtitle",
                        ),

                html.Div([
                        html.A(
                            html.Button("View the Code Notebook on GitHub.", className="learn-more-button"),
                            href="https://github.com/orectique/protestindex/blob/main/Code%20Notebook.txt",
                            target="_blank",
                        )
                    ],
                    className="info-button",
                ),



    
      html.Div([dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in available_countries],
                value= [rand_country],
                multi = True,
                clearable=False
            ),

    ],style={'width': '7%', 'float': 'left', 'display': 'inline-block', 'padding': '25px 30px 25px 35px'}),

        html.Div([dcc.RangeSlider(
        id='year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=[df['Year'].min(), df['Year'].max()],
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    )
    ], style={'width': '100%', 'float': 'bottom', 'display': 'inline-block', 'padding': '25px 10px 25px 10px'})
            ], style={'width': '50%', 'float': 'left', 'display': 'inline-block', 'padding': '25px 30px 25px 10px'}),

    html.Div([
    html.Div([
        dcc.Graph(id='indicator-graphic')
        ],style={'width': '100%', 'float': 'centre', 'display': 'inline-block'}),
    ], style={'width': '50%', 'float': 'right', 'display': 'inline-block', 'padding': '25px 10px 25px 30px'}),


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
