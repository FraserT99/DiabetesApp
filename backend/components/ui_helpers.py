#Import necessary components from Dash and Bootstrap
import dash_bootstrap_components as dbc
from dash import html

def generate_metric_card(title, value):

    return dbc.Col(  #Create a column for the metric card
        html.Div([  #Main container for the card
            html.H5(title, className="card-title"),  #Title of the card (metric name)
            html.H2(value, className="card-value"),  #Value of the metric (displayed as a large number)
        ], className="metric-card"),  #Card styling
        width=4  #Column width for layout
    )
