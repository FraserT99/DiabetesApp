#Dash imports for layout and components
from dash import html, dcc
import dash_bootstrap_components as dbc

#Importing the sidebar component to be used in the page layout
from components.sidebar import create_sidebar

#Importing METRIC_LABELS for dropdown options
from services.user_service import METRIC_LABELS

def goals_page(username="User"):

    return dbc.Container(fluid=True, className="goals-container", children=[

        #Row containing Sidebar (left) and Content (right)
        dbc.Row([

            #Sidebar Section (Takes up 2 columns)
            dbc.Col(create_sidebar(), width=2),

            #Main Content Section (Takes up 10 columns)
            dbc.Col([

                #Wrapper for the whole Goals Page content
                html.Div(className="goals-page-wrapper", children=[

                    #Hero Header Section with Title and Subtext
                    html.Div(className="goals-hero", children=[
                        html.H2("🎯 Set Your Personal Health Goals", className="goals-header"),  #Main Title
                        html.P("Track your progress with short and long-term goals, then view your performance visually.", className="goals-subtext")  #Subtext
                    ]),

                    #Goal Creation Form Section
                    html.Div(className="goals-form-wrapper", children=[

                        #Row to create the goal form with dropdowns and input fields
                        dbc.Row([

                            #Metric Dropdown (Select Metric to track)
                            dbc.Col([
                                html.Label("Select Metric", className="goals-label"),
                                dcc.Dropdown(
                                    id="goal-metric-dropdown",  #Dropdown to select a metric
                                    options=[{"label": label, "value": metric} for metric, label in METRIC_LABELS.items()],
                                    placeholder="e.g. Steps Taken, Calories Burned, HbA1c...",  #Placeholder text
                                    className="goals-dropdown"
                                )
                            ], width=4),  #This column takes up 4 units of the 12-column grid

                            #Goal Value Input (Enter the numeric value for the goal)
                            dbc.Col([
                                html.Label("Set Goal Value", className="goals-label"),
                                dcc.Input(
                                    id="goal-value-input",  #Input field for the goal value
                                    type="number",
                                    placeholder="e.g. 8000 or 65",  #Placeholder text
                                    debounce=True,  #Wait until the user stops typing before validating
                                    min=0.000001,  #Prevents entering 0 or less
                                    className="goals-input"
                                )
                            ], width=2),  #This column takes up 2 units of the 12-column grid

                            #Goal Type Dropdown (Select the type of goal, e.g. weekly, daily)
                            dbc.Col([
                                html.Label("Goal Type", className="goals-label"),
                                dcc.Dropdown(
                                    id="goal-type-dropdown",  #Dropdown to select goal type (weekly, daily, etc.)
                                    options=[],  #Empty options, will be populated dynamically
                                    disabled=True,  #Initially disabled until a metric is selected
                                    placeholder="e.g. Weekly",  #Placeholder text
                                    className="goals-dropdown"
                                )
                            ], width=3),  #This column takes up 3 units of the 12-column grid

                            #Save Goal Button (Submit the form to save the goal)
                            dbc.Col([
                                html.Label(" ", className="goals-label"),  #Blank for alignment
                                dbc.Button("💾 Save Goal", id="save-goal-btn", color="primary", className="goals-save-btn")  #Save button
                            ], width=3),  #This column takes up 3 units of the 12-column grid
                        ], className="goals-input-row"),  #Styling for the input row

                        #Section for alerts, like feedback on goal creation or deletion
                        html.Div([

                            #Auto-dismissing alert for goal creation feedback
                            dbc.Alert(
                                id="goal-feedback-alert",
                                is_open=False,  #Initially closed
                                duration=5000,  #Dismiss after 5 seconds
                                fade=True,
                                dismissable=True,  #Allow dismissing the alert
                                className="mt-2"
                            ),

                            #Auto-dismissing alert for goal deletion feedback (error messages)
                            dbc.Alert(
                                id="goal-delete-alert",
                                is_open=False,  #Initially closed
                                duration=5000,  #Dismiss after 5 seconds
                                fade=True,
                                dismissable=True,
                                color="danger",  #Red alert for errors
                                className="mt-2"
                            ),

                            #Hidden store components to manage the goal refresh state
                            dcc.Store(id="goal-refresh-trigger"),
                            dcc.Store(id="goal-load-trigger", data=True)

                        ], className="goals-button-row"),  #Styling for the buttons section
                    ]),

                    #Section to display the existing goals
                    html.Div(id="existing-goals-display", className="goals-current-goals")

                ])  #End of goals-page-wrapper
            ], width=10)  #End of main content section (right side)
        ])  #End of main row (sidebar + content)
    ])  #End of container
