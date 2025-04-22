from dash import dcc, html
import dash_bootstrap_components as dbc
from components.sidebar import create_sidebar
from services.user_service import METRIC_LABELS

def log_data_page(username="User"):
    

    loggable_metrics = METRIC_LABELS


    return dbc.Container([
        dbc.Row([


            dbc.Col(create_sidebar(), width=2),


            dbc.Col([
                dbc.Row([


                    dbc.Col([  
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.Label("Select Metric to Update:", className="form-label"),
                                    dcc.Dropdown(
                                        id="log-metric-dropdown",
                                        options=[{"label": label, "value": key} for key, label in loggable_metrics.items()],
                                        value="latest_fasting_blood_sugar",
                                        clearable=False,
                                        className="form-control"
                                    )
                                ], className="form-group"),

                                html.Div([
                                    html.Label("Enter New Value:", className="form-label"),
                                    dbc.Input(id="log-new-value", type="number", className="form-control", debounce=True),
                                ], className="form-group"),


                                html.Div([  
                                    dbc.Button("Update Metric", id="update-metric-btn", className="update-btn", color="primary", n_clicks=0),
                                    dbc.Button("Back to Dashboard", href="/dashboard", className="back-btn", color="secondary"),
                                ], className="button-group"),


                                html.Div(id="recent-metric-history"),


                                html.Div(id="update-message", className="success-message"),
                            ])
                        ], className="log-data-card")
                    ], width=6),


                    dbc.Col([
                        dbc.Card([  
                            dbc.CardBody([
                                html.H4(id="tips-title", className="tips-title"),
                                html.Div(id="health-tips", className="tips-container"),
                            ])
                        ], className="tips-card"),
                    ], width=6)

                ])
            ], width=10)

        ])
    ], fluid=True)
