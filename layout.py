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



# Lottie by Emil - https://github.com/thedirtyfew/dash-extensions
url_global_casses = "https://assets10.lottiefiles.com/packages/lf20_4cuwsw1e.json"
url_death = "https://assets9.lottiefiles.com/private_files/lf30_qufxtzzx.json"
url_recovered = "https://assets8.lottiefiles.com/packages/lf20_txJcSM.json"
url_active = "https://assets9.lottiefiles.com/packages/lf20_tk0uford.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

# Bootstrap themes by Ann: https://hellodash.pythonanywhere.com/theme_explorer
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

#####################################
#      LAYOUT    
#####################################

app.layout = dbc.Container(style={'backgroundColor': 'rgba(0, 0, 0, 0.5)'}, children=[
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.CardLink("Source Code: GitHub", target="_blank",
                                 href="https://github.com/Ivan2911/COVID-19-VIZ",
                                 className="text-muted font-weight-light"
                                )
                            ])
                    ], className="mb-2 mt-2", style={'border-radius': '8px'}),
                ], width=2),
        
        # Title
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H1('COVID-19', className="text-white font-weight-bold"),
                    html.H5('Last Updated:', className="text-red font-weight-bold")
                ])
            ], color="info", className="text-center mb-2 mt-2", style={'border-radius': '8px'}),
        ], width=8),

    ], className="mb-4 mt-4"), #End of row

    #US Global Row
    dbc.Row([
        #US Global Cases
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="30%", height="50%", url=url_global_casses), className="card-header-fixed-size"),
                dbc.CardBody([
                    html.H5('US Global Casses'),
                    html.H2('global_cases')
                ], style={'textAlign':'center'}, className="card-header-fixed-size")
            ], style={'border-radius': '8px'}),
        ], width=3),

        #Global Deaths
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="30%", height="30%", url=url_death), className="card-header-fixed-size"),
                dbc.CardBody([
                    html.H5('US Global Deaths'),
                    html.H2('global_deaths')
                ], style={'textAlign':'center'})
            ], style={'border-radius': '8px'}),
        ], width=3),
        #Global CFR
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="30%", height="30%", url=url_recovered), className="card-header-fixed-size"),
                dbc.CardBody([
                    html.H5('US Case Fertility Rate'),
                    html.H2('global_CFR')
                ], style={'textAlign':'center'}, className="card-header-fixed-size")
            ], style={'border-radius': '8px'}),
        ], width=3),
        #Global Attack Rate
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="30%", height="30%", url=url_active), className="card-header-fixed-size"),
                dbc.CardBody([
                    html.H5('US Attack Rate'),
                    html.H2('global_attack_rate')
                ], style={'textAlign': 'center'})
            ], style={'border-radius': '8px'}),
        ], width=3),

    ],className='mb-3'),

    #Graph Rows
    dbc.Row([
        #State KPI
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Dropdown(
                        id='state_dropdown',
                        options=[
                     {'label': 'Species', 'value': 'Animal Class'},
                     {'label': 'Final Ranger Action', 'value': 'Final Ranger Action'},
                     {'label': 'Age', 'value': 'Age', 'disabled':True},
                     {'label': 'Animal Condition', 'value': 'Animal Condition'},
                     {'label': 'Borough', 'value': 'Borough'},
                     {'label': 'Species Status', 'value': 'Species Status'}
            ],
                        value='Alabama',
                        disabled=False,
                        multi=False,
                        searchable=True,
                        search_value='',
                        placeholder='Please select state...',
                        clearable=True,
                        style={'width': "100%"},
                        persistence= True, 
                        persistence_type='memory'
                                ),
                             ])
                    ], className='mb-2', style={'border-radius': '8px'}),

            dbc.Card([
                #dbc.CardHeader(Lottie(options=options, width="30%", height="30%", url=url_recovered), className="card-header-fixed-size"),
                dbc.CardBody([
                    html.H6('Cases'),
                    html.H2(id='content-state_cases', children="000")
                            ], style={'textAlign':'center'})
                    ], className='mb-1', style={'border-radius': '50px'}),
            
            dbc.Card([
                #dbc.CardHeader(Lottie(options=options, width="30%", height="30%", url=url_active), className="card-header-fixed-size"),
                dbc.CardBody([
                    html.H6('Death'),
                    html.H2(id='content-state_death', children="000")
                    ], style={'textAlign': 'center'})
                ], className='mb-1', style={'border-radius': '50px'}),

           
            dbc.Card([
                #dbc.CardHeader(Lottie(options=options, width="30%", height="30%", url=url_recovered), className="card-header-fixed-size"),
                dbc.CardBody([
                        html.H6('Case Fertility Rate'),
                        html.H2(id='content-state_CFR', children="000")
                                ], style={'textAlign':'center'})
                        ], className='mb-1', style={'border-radius': '50px'}),
            
            dbc.Card([
                #dbc.CardHeader(Lottie(options=options, width="30%", height="30%", url=url_active), className="card-header-fixed-size"),
                dbc.CardBody([
                    html.H6('Attack Rate'),
                    html.H2(id='content-state_attack_rate', children="000")
                    ], style={'textAlign': 'center'})
                ], className='mb-1', style={'border-radius': '50px'}),
        ], width=3),

        #Graph
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='line-chart', figure={}),
                             ])
                    ], style={'border-radius': '8px'}),
                ], width=9),
                            ],className='mb-2'),

    #Map row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='TBD', figure={}),
                ])
            ]),
        ], width=12),

    ],className='mb-2'),
], fluid=True)


if __name__=='__main__':
    app.run_server(debug=True, port=8002)