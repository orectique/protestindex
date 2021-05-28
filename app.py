import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px


import pandas as pd
import random

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}], external_stylesheets=[dbc.themes.SUPERHERO])
app.title = 'Protest Index'
server = app.server

df = pd.read_csv('https://raw.githubusercontent.com/orectique/protestindex/main/Factors.csv')

available_countries = df['Country'].unique()
rand_country = random.choice(available_countries)


########################################################

app.layout = html.Div([

    html.Div([
        #Title, subtitle, button
        dcc.Markdown(
                            """
                ### Quantifying events of Social Unrest: Protest Index
                """.replace(
                                "  ", ""
                            ),
                            style = {'font-family' : '"Times New Roman", Times, serif', 'padding': '105px 10px 20px 30px'},
                        ),
        dcc.Markdown(
                            """This interactive graph is a rendition of a study by Lorem Ipsum in which they explored the creation
                            of a new indexing system to effectively capture the scale and hence enable the comparison of social unrest across countries
                            and years. """.replace(
                                "  ", ""
                            ),
                            style = {'font-family' : '"Times New Roman", Times, serif', 'padding': '20px 10px 20px 20px'},
                        ),

        html.Div([
            html.A(
                            html.Button("View the Code Notebook on GitHub.", className="learn-more-button"),
                            href="https://github.com/orectique/protestindex/blob/main/Code%20Notebook.txt",
                            target="_blank",
                        )
                    ],
                    style = {'font-family' : '"Times New Roman", Times, serif', 'display':'inline-block', 'padding':'30px 10px 30px 20px' },
                ),

        html.Div([
        #country select
        dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in available_countries],
                value= [rand_country],
                multi = True,
                clearable=False
            ),
    ], style = {'width' : '100%', 'float':'left', 'display': 'inline-block', 'padding': '30px 10px 30px 20px', 'color':'black'}),

    ], style = {'width' : '30%', 'float': 'left', 'display': 'inline-block'}),


    html.Div([
        #graph
        dcc.Graph(id='indicator-graphic')
    ], style = {'width' : '70%', 'height':'100%', 'float': 'right', 'display': 'inline-block', 'padding': '110px 20px 25px 10px'}),

    html.Div([
        #timeline
        dcc.RangeSlider(
        id='year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=[df['Year'].min(), df['Year'].max()],
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    )
    ], style = {'width' : '100%', 'margin':'auto', 'display': 'inline-block', 'padding': '25px 40px 25px 40px', 'color': 'white'})
  
])

########################################################

@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('country', 'value'),
    Input('year--slider', 'value'))
def update_graph(country_names, year_value):
    year_list = list( i for i in range(year_value[0], year_value[1] + 1))
    df1 = df[df['Country'].isin(list(country_names))]
    dff = df1[df1['Year'].isin(year_list)]
    fig = px.scatter(dff, x="Factor1", y="Factor2", template = 'plotly_dark', color = 'Country', hover_data=['Year'], title = "Scatter Plot of Protest Indices Across Years")


    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
