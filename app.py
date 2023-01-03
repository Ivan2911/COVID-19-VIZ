import dash                              # pip install dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input

import os

from dash_extensions import Lottie       # pip install dash-extensions
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px              # pip install plotly
import pandas as pd                      # pip install pandas
from datetime import date
import calendar
#from wordcloud import WordCloud          # pip install wordcloud



#####################################
#      Data    
#####################################

#Load and read date
us2020_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-2020.csv"
us2020_cases = pd.read_csv(us2020_url, usecols=['date', 'county', 'state', 'cases', 'deaths'])
us2021_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-2021.csv"
us2021_cases = pd.read_csv(us2021_url, usecols=['date', 'county', 'state', 'cases', 'deaths'])
us2022_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-2022.csv"
us2022_cases = pd.read_csv(us2022_url, usecols=['date', 'county', 'state', 'cases', 'deaths'])

#Fill null value with 0
us2020_cases["deaths"] = us2020_cases["deaths"].fillna(0)
us2021_cases["deaths"] = us2021_cases["deaths"].fillna(0)
us2022_cases["deaths"] = us2022_cases["deaths"].fillna(0)

# Group by date and grup by date and state
us2020_date = us2020_cases.groupby(["date"])[["cases","deaths"]].sum().reset_index()
us2020_state = us2020_cases.groupby(["date", "state"])[["cases","deaths"]].sum().reset_index()

us2021_date = us2021_cases.groupby(["date"])[["cases","deaths"]].sum().reset_index()
us2021_state = us2021_cases.groupby(["date", "state"])[["cases","deaths"]].sum().reset_index()

us2022_date = us2022_cases.groupby(["date"])[["cases","deaths"]].sum().reset_index()
us2022_state = us2022_cases.groupby(["date", "state"])[["cases","deaths"]].sum().reset_index()

#Concate the data frame to union 2020, 2021 and 2022
us_date_df = pd.concat([us2020_date, us2021_date, us2022_date])
us_state_df = pd.concat([us2020_state, us2021_state, us2022_state])

#Make sure the date is in date format
us_date_df ['date'] = pd.to_datetime(us_date_df['date'])
us_state_df ['date'] = pd.to_datetime(us_state_df['date'])

#add a new column called year
us_state_df['year'] = us_state_df['date'].dt.year
us_date_df['year'] = us_date_df['date'].dt.year

#Load estimated population data
pop_df = pd.read_csv('data/estimated_population.csv')

#####################################
#      Global Data To Show    
#####################################
#Last update date
last_update= us_date_df["date"].iloc[-1].strftime('%Y-%m-%d')
#Global cases
global_cases = us_date_df["cases"].iloc[-1]
#Global deaths
global_deaths = us_date_df["deaths"].iloc[-1]
#Global CFR
global_CFR = round(global_deaths/global_cases, 4)
#Global Attack Rate
population_2022 = pop_df['2022'].sum()
global_attack_rate = round(global_cases/population_2022, 4)

#Options list
unique_state = sorted(us_state_df['state'].unique())
state_options = [{'label': value, 'value': value} for value in unique_state]

#Map data frame
map_df = pd.merge(us2022_state, pop_df, left_on='state', right_on='NAME')
map_df = map_df[['date','code','state','cases','deaths','2022']]
map_df.rename(columns={'2022': 'population'}, inplace=True)
map_df = map_df.loc[(map_df['date']== last_update)]

#Adding CFR and Attack rate
map_df = map_df.assign(CFR=round(map_df['deaths']/map_df['cases'],4))
map_df = map_df.assign(**{'attack rate': round(map_df['deaths']/map_df['cases'],4)})

map_fig = px.choropleth(
    data_frame=map_df,
    locationmode='USA-states',
    locations='code',
    scope="usa",
    color='cases',
    hover_data=['state', 'cases','deaths', 'CFR','attack rate'],
    color_continuous_scale=px.colors.sequential.YlOrRd,
    labels={'Cases': 'Number of cases'},
    template='plotly_dark'
)


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

app.layout = dbc.Container([
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
                    html.H5('Last Updated:' + last_update, className="text-red font-weight-bold")
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
                    html.H2(global_cases)
                ], style={'textAlign':'center'}, className="card-header-fixed-size")
            ], style={'border-radius': '8px'}),
        ], width=3),

        #Global Deaths
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="30%", height="30%", url=url_death), className="card-header-fixed-size"),
                dbc.CardBody([
                    html.H5('US Global Deaths'),
                    html.H2(global_deaths)
                ], style={'textAlign':'center'})
            ], style={'border-radius': '8px'}),
        ], width=3),
        #Global CFR
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="30%", height="30%", url=url_recovered), className="card-header-fixed-size"),
                dbc.CardBody([
                    html.H5('US Case Fertility Rate'),
                    html.H2(global_CFR)
                ], style={'textAlign':'center'}, className="card-header-fixed-size")
            ], style={'border-radius': '8px'}),
        ], width=3),
        #Global Attack Rate
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="30%", height="30%", url=url_active), className="card-header-fixed-size"),
                dbc.CardBody([
                    html.H5('US Attack Rate'),
                    html.H2(global_attack_rate)
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
                        options=state_options,
                        value='Alabama',
                        disabled=False,
                        multi=False,
                        searchable=True,
                        search_value='',
                        clearable=False,
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
                    dcc.Graph(id='map_fegure', figure= map_fig),
                ])
            ], style={'border-radius': '8px'}),
        ], width=12),

    ],className='mb-2'),
], fluid=True)

#####################################
#      CALL BACK     
#####################################

# Updating the 4 number cards
@app.callback(
    Output('content-state_cases','children'),
    Output('content-state_death','children'),
    Output('content-state_CFR','children'),
    Output('content-state_attack_rate','children'),
    [Input(component_id='state_dropdown', component_property='value')]
)
def update_small_cards(state):
    #filter by state
    df_state = us_state_df.loc[us_state_df['state']==state]

    # state cases
    state_cases = df_state["cases"].iloc[-1]

    #state deaths
    state_deaths = df_state["deaths"].iloc[-1]

    #state CFR
    state_CFR = round(state_deaths/state_cases, 4)

    #state attack rate
    population_state_2022 = pop_df.loc[(pop_df['NAME'] == state),'2022']
    state_attack_rate =  round(state_cases/population_state_2022, 4)

    return state_cases, state_deaths, state_CFR, state_attack_rate
    
# Updating the graph
@app.callback(
    Output(component_id='line-chart', component_property='figure'),
    [Input(component_id='state_dropdown', component_property='value')]
)
#graph
def update_graph(state):
    df_state = us_state_df.loc[us_state_df['state']==state]
    fig = px.line(df_state , x='date', y=['cases', 'deaths'], title='Covid-19 Cases and Deaths in ' + state)
    return fig

if __name__=='__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))