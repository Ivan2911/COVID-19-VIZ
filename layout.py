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
                    html.H5('Last Updated: 222/2/22/', className="text-red font-weight-bold")
                ])
            ], color="info", className="text-center", style={'border-radius': '8px'}),
        ], width=8),

    ], className="mb-4 mt-4"), #End of row
], fluid=True)


if __name__=='__main__':
    app.run_server(debug=True, port=8002)