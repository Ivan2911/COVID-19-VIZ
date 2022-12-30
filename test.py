import dash                              # pip install dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input

from dash_extensions import Lottie       # pip install dash-extensions
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px              # pip install plotly
import pandas as pd                      # pip install pandas
from datetime import date
import calendar
#from wordcloud import WordCloud          # pip install wordcloud

# Lottie by Emil - https://github.com/thedirtyfew/dash-extensions
url_global_casses = "https://assets10.lottiefiles.com/packages/lf20_4cuwsw1e.json"
url_death = "https://assets9.lottiefiles.com/private_files/lf30_qufxtzzx.json"
url_recovered = "https://assets8.lottiefiles.com/packages/lf20_txJcSM.json"
url_active = "https://assets9.lottiefiles.com/packages/lf20_tk0uford.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

# Bootstrap themes by Ann: https://hellodash.pythonanywhere.com/theme_explorer
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardImg(src='/assets/A_logo.png') # 150px by 45px
            ],className='mb-2'),
            dbc.Card([
                dbc.CardBody([
                    dbc.CardLink("Source Code: GitHub", target="_blank",
                                 href="https://github.com/Ivan2911/COVID-19-VIZ"
                    )
                ])
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.DatePickerSingle(
                        id='my-date-picker-start',
                        date=date(2018, 1, 1),
                        className='ml-5'
                    ),
                    dcc.DatePickerSingle(
                        id='my-date-picker-end',
                        date=date(2021, 4, 4),
                        className='mb-2 ml-2'
                    ),
                ])
            ], color="info"),
        ], width=8),
    ],className='mb-2 mt-2'),

    #Global Row
    dbc.Row([
        #Global Cases
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="30%", height="50%", url=url_global_casses), className="card-header-fixed-size"),
                dbc.CardBody([
                    html.H6('Global Casses'),
                    html.H2(id='content-global_casses', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=3),

        #Global Deaths
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="30%", height="30%", url=url_death), className="card-header-fixed-size"),
                dbc.CardBody([
                    html.H6('Global Deaths'),
                    html.H2(id='content-global_deaths', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=3),
        #Global Recovered
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="30%", height="30%", url=url_recovered), className="card-header-fixed-size"),
                dbc.CardBody([
                    html.H6('Global Recovered'),
                    html.H2(id='content-global_recovered', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=3),
        #Global Active
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="30%", height="30%", url=url_active), className="card-header-fixed-size"),
                dbc.CardBody([
                    html.H6('Global Active'),
                    html.H2(id='content-global_active', children="000")
                ], style={'textAlign': 'center'})
            ]),
        ], width=3),

    ],className='mb-3'),

    #Graph Rows
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='line-chart', figure={}),
                ])
            ]),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='bar-chart', figure={}),
                ])
            ]),
        ], width=4),
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='TBD', figure={}),
                ])
            ]),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='pie-chart', figure={}),
                ])
            ]),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='wordcloud', figure={}),
                ])
            ]),
        ], width=4),
    ],className='mb-2'),
], fluid=True)

#Update: Global cards information
@app.callback(
    Output("content-global_casses", "children"),
    Output("content-global_deaths", "children"),
    Output("content-global_recovered", "children"),
    Output("content-global_active", "children"),
    
)



if __name__=='__main__':
    app.run_server(debug=True, port=8001)