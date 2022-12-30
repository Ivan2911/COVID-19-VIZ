import pandas as pd
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output

#========================================#
#         DATA PROCESSING                #
#========================================#

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
df = confirmed_unpivoted.merge(right = death_unpivoted, how = "left", on=["Province/State", "Country/Region", "Lat","Long","date"])
df = df.merge(right = recovered_unpivoted, how = "left", on=["Province/State", "Country/Region", "Lat","Long","date"])

#null replacments
df["recovered"] = df["recovered"].fillna(0)

#generate active columns
df["active"] = df["confirmed"] - df["death"] - df["recovered"]

#Change the date format
df['date'] = pd.to_datetime(df['date'])

#derive more data
global_sum_by_date_df = df.groupby(["date"])[["confirmed","death","recovered","active"]].sum().reset_index()
country_sum_by_date_df = df.groupby(["date","Country/Region"])[["confirmed","death","recovered","active"]].sum().reset_index()


#Last update date
last_update= df["date"].iloc[-1].strftime('%Y-%m-%d')


#========================================#
#             APLICATIION                #
#========================================#

# Create the Dash app
app = dash.Dash()

# Application Layout
app.layout = dbc.Container([






    
])









])


# Callback Function
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

