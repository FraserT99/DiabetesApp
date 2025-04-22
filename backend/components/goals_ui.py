from dash import html, dcc
import dash_bootstrap_components as dbc
from components.sidebar import create_sidebar
from services.user_service import METRIC_LABELS

def goals_page(username="User"):

    return dbc.Container(fluid=True, className="goals-container", children=[

        dbc.Row([

            dbc.Col(create_sidebar(), width=2),

            dbc.Col([

                html.Div(className="goals-page-wrapper", children=[

                    html.Div(className="goals-hero", children=[
                        html.H2("🎯 Set Your Personal Health Goals", className="goals-header"),  
                        html.P("Track your progress with short and long-term goals, then view your performance visually.", className="goals-subtext")
                    ]),

                    html.Div(className="goals-form-wrapper", children=[

                        dbc.Row([

                            dbc.Col([
                                html.Label("Select Metric", className="goals-label"),
                                dcc.Dropdown(
                                    id="goal-metric-dropdown",  
                                    options=[{"label": label, "value": metric} for metric, label in METRIC_LABELS.items()],
                                    placeholder="e.g. Steps Taken, Calories Burned, HbA1c...",  
                                    className="goals-dropdown"
                                )
                            ], width=4),  

                            dbc.Col([
                                html.Label("Set Goal Value", className="goals-label"),
                                dcc.Input(
                                    id="goal-value-input",  
                                    type="number",
                                    placeholder="e.g. 8000 or 65",  
                                    debounce=True,  
                                    min=0.000001, 
                                    className="goals-input"
                                )
                            ], width=2),  

                            dbc.Col([
                                html.Label("Goal Type", className="goals-label"),
                                dcc.Dropdown(
                                    id="goal-type-dropdown",  
                                    options=[],  
                                    disabled=True,  
                                    placeholder="e.g. Weekly",  
                                    className="goals-dropdown"
                                )
                            ], width=3), 

                  
                            dbc.Col([
                                html.Label(" ", className="goals-label"),  
                                dbc.Button("💾 Save Goal", id="save-goal-btn", color="primary", className="goals-save-btn")  
                            ], width=3),  
                        ], className="goals-input-row"),  

                        html.Div([

                            dbc.Alert(
                                id="goal-feedback-alert",
                                is_open=False,  
                                duration=5000,  
                                fade=True,
                                dismissable=True,  
                                className="mt-2"
                            ),

                            dbc.Alert(
                                id="goal-delete-alert",
                                is_open=False,  
                                duration=5000,  
                                fade=True,
                                dismissable=True,
                                color="danger",  
                                className="mt-2"
                            ),

                            dcc.Store(id="goal-refresh-trigger"),
                            dcc.Store(id="goal-load-trigger", data=True)

                        ], className="goals-button-row"),  
                    ]),

                    html.Div(id="existing-goals-display", className="goals-current-goals")

                ])  
            ], width=10)  
        ])  
    ])  
