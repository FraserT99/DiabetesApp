#Dash imports for creating the layout
from dash import html
import dash_bootstrap_components as dbc

#Import the sidebar component to be used in the page
from components.sidebar import create_sidebar

def challenges_page(username="User"):
    
    return dbc.Container([

        dbc.Row([

            dbc.Col(create_sidebar(), width=2),

            dbc.Col([

                html.Div(
                    html.H4(id="user-points", className="points-bar"),  
                    className="points-container"  
                ),

                dbc.Row([

                    dbc.Col([
                        html.H4(id="daily-title", className="challenge-section-title"),  
                        html.Div(id="daily-challenges", className="challenge-card-container"),  
                    ], width=4),  


                    dbc.Col([
                        html.H4(id="weekly-title", className="challenge-section-title"),  
                        html.Div(id="weekly-challenges", className="challenge-card-container"),  
                    ], width=4),  

    
                    dbc.Col([
                        html.H4(id="monthly-title", className="challenge-section-title"),  
                        html.Div(id="monthly-challenges", className="challenge-card-container"), 
                    ], width=4),  

                ], className="challenge-sections"),  

            ], width=10, className="content-container")  
        ])
    ], fluid=True)  
