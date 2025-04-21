#Importing necessary components from Dash and Bootstrap for layout creation
from dash import dcc, html
import dash_bootstrap_components as dbc
from components.sidebar import create_sidebar  #Custom Sidebar component
from services.user_service import METRIC_LABELS  #Importing METRIC_LABELS to dynamically create metric dropdown options

def log_data_page(username="User"):
    
    #Full list of loggable metrics (Dynamically expandable)
    loggable_metrics = METRIC_LABELS  #Retrieves the dictionary of metrics from the user service

    #Main container for the page layout
    return dbc.Container([  #Create a container to hold the entire layout
        dbc.Row([  #Create a row to divide the page into two sections (left and right)

            #Sidebar Section
            dbc.Col(create_sidebar(), width=2),  #Sidebar, occupies 2 columns of width

            #Main Content Section
            dbc.Col([  #Main content, occupies 10 columns of width
                dbc.Row([  #Create a row for the left and right content sections

                    #Left Section: Log Form (for updating metrics)
                    dbc.Col([  
                        dbc.Card([  #A card to hold the log form content
                            dbc.CardBody([  #Card body containing form elements
                                html.Div([  #Metric Dropdown
                                    html.Label("Select Metric to Update:", className="form-label"),
                                    dcc.Dropdown(
                                        id="log-metric-dropdown",  #Dropdown for metric selection
                                        options=[{"label": label, "value": key} for key, label in loggable_metrics.items()],
                                        value="latest_fasting_blood_sugar",  #Default value
                                        clearable=False,  #Prevent clearing the selection
                                        className="form-control"  #Styling for the dropdown
                                    )
                                ], className="form-group"),

                                html.Div([  #Input field for entering the new value
                                    html.Label("Enter New Value:", className="form-label"),
                                    dbc.Input(id="log-new-value", type="number", className="form-control", debounce=True),
                                ], className="form-group"),

                                #Buttons for submitting data or navigating back
                                html.Div([  
                                    dbc.Button("Update Metric", id="update-metric-btn", className="update-btn", color="primary", n_clicks=0),
                                    dbc.Button("Back to Dashboard", href="/dashboard", className="back-btn", color="secondary"),
                                ], className="button-group"),

                                #Section to display the last 5 logs for the selected metric
                                html.Div(id="recent-metric-history"),

                                #Success/Error Message (Display after action completion)
                                html.Div(id="update-message", className="success-message"),
                            ])
                        ], className="log-data-card")  #Card wrapping the log form
                    ], width=6),  #Left side of the layout takes 6 columns of width

                    #Right Section: Health Tips (Full Width)
                    dbc.Col([  #The right section now spans full width for health tips
                        dbc.Card([  
                            dbc.CardBody([  #Card body for the health tips
                                html.H4(id="tips-title", className="tips-title"),  #Title for health tips section
                                html.Div(id="health-tips", className="tips-container"),  #Container for health tips content
                            ])
                        ], className="tips-card"),
                    ], width=6)  #Right column takes the remaining 6 columns of width

                ])
            ], width=10)  #Main content section takes 10 columns of width

        ])
    ], fluid=True)  #Set the container as fluid to ensure full width usage
