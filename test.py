import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
import requests
import pandas as pd

def get_covid_data(country):
    url = f'https://coronavirus-19-api.herokuapp.com/countries/{country}'
    r = requests.get(url)
    data = r.json()
    df = pd.DataFrame(data)
    return df

app = dash.Dash(__name__)
server = app.server
app.title = 'COVID-19 Dashboard'

app.layout =html.Div(style={'backgroundColor': 'black'}, children=[
    dbc.Container([
    html.H1('COVID-19 Dashboard'),
    dcc.Dropdown(
        id='country-dropdown',
        options=[
            {'label': 'United States', 'value': 'US'},
            {'label': 'China', 'value': 'CN'},
            {'label': 'India', 'value': 'IN'},
            {'label': 'Russia', 'value': 'RU'},
            {'label': 'Brazil', 'value': 'BR'},
        ],
        value='US'
    ),
    dcc.Graph(id='covid-graph', style={'backgroundColor': 'gray'})
    ])
])

@app.callback(
    Output('covid-graph', 'figure'),
    [Input('country-dropdown', 'value')])
def update_graph(selected_country):
    # Get COVID-19 data for the selected country
    data = get_covid_data(selected_country)

    # Create a bar chart using the data
    figure = {
        'data': [
            {'x': data['date'], 'y': data['cases'], 'type': 'bar', 'name': 'Cases'},
            {'x': data['date'], 'y': data['deaths'], 'type': 'bar', 'name': 'Deaths'},
        ],
        'layout': {
            'title': f'COVID-19 Cases and Deaths in {selected_country}'
        }
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
