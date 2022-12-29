import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output

# Load the confirmed cases data set
confirmed_cases_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/9c3583084c24675d144bb121930c6dee3f80f370/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
confirmed_cases = pd.read_csv(confirmed_cases_url)

# Load the deaths data set
deaths_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
deaths = pd.read_csv(deaths_url)

# Load the recoveries data set
recoveries_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
recoveries = pd.read_csv(recoveries_url)

## Unpivot the data
date_columns = confirmed_cases.columns[4:]
id_vars_columns = confirmed_cases.columns[:4]
confirmed_unpivoted = confirmed_cases.melt(id_vars=id_vars_columns, value_vars=date_columns, var_name='date', value_name='confirmed')

date_columns = deaths.columns[4:]
id_vars_columns = deaths.columns[:4]
death_unpivoted = deaths.melt(id_vars=id_vars_columns, value_vars=date_columns, var_name='date', value_name='death')

date_columns = recoveries.columns[4:]
id_vars_columns = recoveries.columns[:4]
recovered_unpivoted = recoveries.melt(id_vars=id_vars_columns, value_vars=date_columns, var_name='date', value_name='recovered')


# Merge the data sets into a single dataframe
df = confirmed_unpivoted.merge(death_unpivoted, on='date')
df = df.merge(recovered_unpivoted, on='date')

# Add a column for the country
df['country'] = df['Country/Region']

# Create the Dash app
app = dash.Dash()

# Create the dropdown menu
dropdown = dcc.Dropdown(
    id='country-dropdown',
    options=[{'label': country, 'value': country} for country in df['country'].unique()],
    value='Global'
)

# Create the callback function
@app.callback(
    Output('covid-19-visualization', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_figure(selected_country):
    filtered_df = df[df['country'] == selected_country]
    return {
        'data': [
            {'x': filtered_df['date'], 'y': filtered_df['confirmed'], 'type': 'bar', 'name': 'Confirmed Cases'},
            {'x': filtered_df['date'], 'y': filtered_df['deaths'], 'type': 'bar', 'name': 'Deaths'},
            {'x': filtered_df['date'], 'y': filtered_df['recoveries'], 'type': 'bar', 'name': 'Recoveries'},
        ],
        'layout': {
            'title': f'COVID-19 Confirmed Cases, Deaths, and Recoveries - {selected_country}'
        }
    }

# Add the dropdown menu and the Graph component to the app layout
app.layout = html.Div([dropdown, dcc.Graph(id='covid-19-visualization')])

# Run the app
if __name__ == '__main__':
    app.run_server()

