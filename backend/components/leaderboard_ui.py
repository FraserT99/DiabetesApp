from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from components.sidebar import create_sidebar

def leaderboard_block(title, dropdown_id, table_id):

    return dbc.Col([  
        html.Div([


            html.Div([
                html.H4(title, className="leaderboard-section-title"),
                dcc.Dropdown(
                    id=dropdown_id,
                    options=[
                        {"label": "All Time", "value": "all_time"},
                        {"label": "Monthly", "value": "monthly"},
                        {"label": "Weekly", "value": "weekly"},
                        {"label": "Daily", "value": "daily"},
                    ],
                    value="all_time",
                    clearable=False,
                    className="leaderboard-dropdown"
                )
            ], className="leaderboard-header-row"),


            dash_table.DataTable(
                id=table_id,
                columns=[
                    {"name": "Rank", "id": "rank"},
                    {"name": "Name", "id": "name"},
                    {"name": "Score", "id": "score"}
                ],
                style_data_conditional=[
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
                style_cell={
                    'textAlign': 'center',
                    'fontFamily': 'sans-serif',
                    'fontSize': '15px',
                },
                style_header={
                    'fontWeight': 'bold',
                    'fontSize': '16px',
                    'color': 'black',
                    'fontFamily': 'sans-serif',
                },
                style_table={'overflowX': 'auto'},
                row_deletable=False,
                style_as_list_view=True
            )
        ])
    ], width=6)

def leaderboard_page():

    return dbc.Container([
        dbc.Row([
            dbc.Col(create_sidebar(), width=2),

            dbc.Col([

                dbc.Row([  
                    leaderboard_block("💪 Top Workout Sessions", "workout-timeframe", "workout-leaderboard"),
                    leaderboard_block("🔥 Top Calories Burned", "calories-timeframe", "calories-leaderboard")
                ], className="leaderboard-container"),

                dbc.Row([  
                    leaderboard_block("🚶 Top Steps Taken", "steps-timeframe", "steps-leaderboard"),
                    leaderboard_block("🌍 Top Distance Walked", "distance-timeframe", "distance-leaderboard")
                ], className="leaderboard-container")
            ], width=10, className="leaderboard-content-container")
        ])
    ], fluid=True)
