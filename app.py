import dash
from dash import Dash
import dash_bootstrap_components as dbc

# app = Dash(__name__, suppress_callback_exceptions=True)

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets) #suppress_callback_exceptions=True, 
server = app.server  # the Flask app
