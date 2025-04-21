#Importing necessary components from Dash and Bootstrap for layout creation
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from components.sidebar import create_sidebar  #Custom Sidebar component

def leaderboard_block(title, dropdown_id, table_id):

    return dbc.Col([  #Create a column to hold the leaderboard content
        html.Div([  #Wrapping the content inside a div for structural styling

            #Header Row with Title and Dropdown for selecting time period
            html.Div([
                html.H4(title, className="leaderboard-section-title"),  #Section title
                dcc.Dropdown(  #Dropdown to select the time period for leaderboard data
                    id=dropdown_id,
                    options=[  #Options for the dropdown menu
                        {"label": "All Time", "value": "all_time"},
                        {"label": "Monthly", "value": "monthly"},
                        {"label": "Weekly", "value": "weekly"},
                        {"label": "Daily", "value": "daily"},
                    ],
                    value="all_time",  #Default selection
                    clearable=False,  #Disable clearing the selection
                    className="leaderboard-dropdown"  #CSS class for styling the dropdown
                )
            ], className="leaderboard-header-row"),  #Apply class for styling the header row

            #The DataTable for displaying the leaderboard data (Rank, Name, Score)
            dash_table.DataTable(
                id=table_id,
                columns=[  #Columns for the leaderboard table
                    {"name": "Rank", "id": "rank"},
                    {"name": "Name", "id": "name"},
                    {"name": "Score", "id": "score"}
                ],
                style_data_conditional=[  #Conditional styling for the rows based on their class
                    {
                        'if': {'filter_query': '{row_class} = "gold-row"'},
                        'backgroundColor': '#fff8dc',
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {'filter_query': '{row_class} = "silver-row"'},
                        'backgroundColor': '#e0e0e0',
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {'filter_query': '{row_class} = "bronze-row"'},
                        'backgroundColor': '#fce5cd',
                        'fontWeight': 'bold'
                    }
                ],
                style_cell={  #General cell styling
                    'textAlign': 'center',
                    'fontFamily': 'sans-serif',
                    'fontSize': '15px',
                },
                style_header={  #Styling for the table headers
                    'fontWeight': 'bold',
                    'fontSize': '16px',
                    'color': 'black',
                    'fontFamily': 'sans-serif',
                },
                style_table={'overflowX': 'auto'},  #Enabling horizontal scrolling for the table
                row_deletable=False,  #Disable row deletion
                style_as_list_view=True  #Display the table as a list view
            )
        ])
    ], width=6)  #Wrap the content inside a Bootstrap column, making the block 6 units wide

def leaderboard_page():

    return dbc.Container([  #Create a container for the layout
        dbc.Row([  #Create a row to hold the content
            dbc.Col(create_sidebar(), width=2),  #Sidebar column, takes 2 width units

            dbc.Col([  #Main content column, takes 10 width units
                #Leaderboard rows, each row containing different leaderboard sections
                dbc.Row([  
                    leaderboard_block("💪 Top Workout Sessions", "workout-timeframe", "workout-leaderboard"),  #Workout sessions leaderboard
                    leaderboard_block("🔥 Top Calories Burned", "calories-timeframe", "calories-leaderboard")  #Calories burned leaderboard
                ], className="leaderboard-container"),

                dbc.Row([  
                    leaderboard_block("🚶 Top Steps Taken", "steps-timeframe", "steps-leaderboard"),  #Steps leaderboard
                    leaderboard_block("🌍 Top Distance Walked", "distance-timeframe", "distance-leaderboard")  #Distance walked leaderboard
                ], className="leaderboard-container")
            ], width=10, className="leaderboard-content-container")  #Main content section
        ])
    ], fluid=True)  #Set the container as fluid to expand it fully
