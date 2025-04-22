import dash_bootstrap_components as dbc
from dash import html

def generate_metric_card(title, value):

    return dbc.Col(
        html.Div([
            html.H5(title, className="card-title"),
            html.H2(value, className="card-value"),
        ], className="metric-card"),
        width=4
    )
