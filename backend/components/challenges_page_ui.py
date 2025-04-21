#Dash imports for creating the layout
from dash import html
import dash_bootstrap_components as dbc

#Import the sidebar component to be used in the page
from components.sidebar import create_sidebar

def challenges_page(username="User"):

    #Container for the page layout
    return dbc.Container([

        #Row containing both the sidebar and main content sections
        dbc.Row([

            #Sidebar Section (Takes up 2 columns)
            dbc.Col(create_sidebar(), width=2),

            #Main Content Section (Takes up 10 columns)
            dbc.Col([

                #Points Bar Section (Centered at the Top)
                #This is where the user's current points will be displayed
                html.Div(
                    html.H4(id="user-points", className="points-bar"),  #User points shown in H4 tag
                    className="points-container"  #CSS class for styling
                ),

                #Row to display the categories of challenges (Daily, Weekly, Monthly)
                #Each column here contains the category title and a container for challenges
                dbc.Row([

                    #Daily Challenges Section
                    dbc.Col([
                        html.H4(id="daily-title", className="challenge-section-title"),  #Title for daily challenges
                        html.Div(id="daily-challenges", className="challenge-card-container"),  #Challenges go here
                    ], width=4),  #Takes up 4 columns

                    #Weekly Challenges Section
                    dbc.Col([
                        html.H4(id="weekly-title", className="challenge-section-title"),  #Title for weekly challenges
                        html.Div(id="weekly-challenges", className="challenge-card-container"),  #Challenges go here
                    ], width=4),  #Takes up 4 columns

                    #Monthly Challenges Section
                    dbc.Col([
                        html.H4(id="monthly-title", className="challenge-section-title"),  #Title for monthly challenges
                        html.Div(id="monthly-challenges", className="challenge-card-container"),  #Challenges go here
                    ], width=4),  #Takes up 4 columns

                ], className="challenge-sections"),  #Class for styling the challenge sections

            ], width=10, className="content-container")  #Main content area taking up the remaining 10 columns
        ])
    ], fluid=True)  #Ensures the layout uses the full width of the page
