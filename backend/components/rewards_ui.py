#Importing necessary libraries
from dash import html, dcc
import dash_bootstrap_components as dbc  #For responsive layouts and reusable Bootstrap components

#Import custom components and services
from components.sidebar import create_sidebar  #Sidebar component for navigation
from services.rewards_service import get_claimed_rewards  #Service to fetch the claimed rewards


#Function to generate the content for each reward card
def reward_card_content(title, points_required, reward_id, icon, claimed_date):

    claimed = claimed_date is not None  #Determine if the reward has been claimed

    #Initialize the reward card content
    inner_content = [
        html.Div(icon, className="reward-icon"),  #Reward icon
        html.H5(title, className="reward-title"),  #Reward title
        html.P(f"{points_required} Points", className="reward-points")  #Points required
    ]

    #If the reward is claimed, show the claim date, otherwise show the claim button
    if claimed:
        inner_content.append(
            html.P(
                f"Claimed on {claimed_date.strftime('%b %d, %Y at %H:%M')}",
                className="reward-claimed-text"
            )
        )
    else:
        inner_content.append(
            dbc.Button(
                "Claim",  #Button text
                id={'type': 'claim-button', 'index': reward_id},  #Button ID for claim action
                color="primary",
                className="claim-button"
            )
        )

    return inner_content, claimed  #Return the content and whether it's claimed or not


#Function to create the reward card component
def reward_card(title, points_required, reward_id, icon, claimed_date):

    #Get the content for the reward card and check if it’s claimed
    content, claimed = reward_card_content(title, points_required, reward_id, icon, claimed_date)
    
    #Assign a class to the card based on whether it’s claimed or not
    card_class = "reward-card"
    if claimed:
        card_class += " reward-claimed-gold sparkle"  #Add additional class for claimed rewards

    #Return the HTML structure for the reward card
    return html.Div(
        dbc.Card(
            dbc.CardBody(
                content,  #Card content
                id={'type': 'reward-card-body', 'index': reward_id}  #Unique ID for the card body
            ),
            className=card_class,  #Card class
            id={'type': 'reward-card', 'index': reward_id}  #Unique ID for the card
        ),
        className="mb-4"  #Margin-bottom class for spacing
    )


#Function to generate the rewards page layout
def rewards_page(username):
  
    #List of reward items with their respective details (ID, title, points, and icon)
    reward_items = [
        {"id": "stepper", "title": "Golden Stepper Badge", "points": 100, "icon": "👣"},
        {"id": "hydration", "title": "Hydration Hero Badge", "points": 150, "icon": "💧"},
        {"id": "legend", "title": "Fitness Legend Badge", "points": 300, "icon": "👑"},
        {"id": "nerd", "title": "Nutrition Nerd Badge", "points": 200, "icon": "🍎"},
        {"id": "logger", "title": "Consistent Logger Badge", "points": 180, "icon": "📝"},
        {"id": "champ", "title": "Power Champ Badge", "points": 350, "icon": "💪"},
    ]

    #Fetch the claimed rewards for the user
    claimed_rewards = get_claimed_rewards(username)

    #Return the page layout
    return dbc.Container(fluid=True, children=[
        dbc.Row([  #Layout row for sidebar and main content
            dbc.Col(create_sidebar(), width=2),  #Sidebar with navigation
            dbc.Col([  #Main content area
                html.Div(className="rewards-page-wrapper", children=[
                    dbc.Row([  #Hero section with the rewards header
                        dbc.Col([  #Left column for hero section
                            html.Div(className="rewards-hero", children=[
                                html.Div("🎁 Rewards", className="rewards-header"),  #Header text
                                html.Div(
                                    "Use your points to unlock awesome badges, titles, and personalization!",
                                    className="rewards-subtext"  #Subtext for explanation
                                ),
                            ])
                        ], width=9),  #Width of the left column

                        #Right column for points balance display
                        dbc.Col([html.Div(id="points-balance", className="points-balance")],
                                width=3, style={"display": "flex", "alignItems": "center", "justifyContent": "flex-end"})
                    ]),

                    #Display claim status and other alerts
                    html.Div(id="claim-status", className="my-2"),

                    #Display the rewards items in a row of cards
                    dbc.Row([
                        dbc.Col(
                            reward_card(  #For each reward item, generate a reward card
                                item["title"],
                                item["points"],
                                item["id"],
                                item["icon"],
                                claimed_rewards.get(item["id"])
                            ),
                            width=4  #Each card takes up 4 columns in the row
                        ) for item in reward_items  #Iterate over all reward items
                    ], className="rewards-row", justify="start")  #Rewards row for layout
                ])
            ], width=10)  #Main content takes up 10 columns
        ])
    ])  #End of container
