from dash import html, dcc
import dash_bootstrap_components as dbc


from components.sidebar import create_sidebar
from services.rewards_service import get_claimed_rewards



def reward_card_content(title, points_required, reward_id, icon, claimed_date):

    claimed = claimed_date is not None


    inner_content = [
        html.Div(icon, className="reward-icon"),
        html.H5(title, className="reward-title"),
        html.P(f"{points_required} Points", className="reward-points")
    ]


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
                "Claim",
                id={'type': 'claim-button', 'index': reward_id},
                color="primary",
                className="claim-button"
            )
        )

    return inner_content, claimed



def reward_card(title, points_required, reward_id, icon, claimed_date):


    content, claimed = reward_card_content(title, points_required, reward_id, icon, claimed_date)
    

    card_class = "reward-card"
    if claimed:
        card_class += " reward-claimed-gold sparkle"


    return html.Div(
        dbc.Card(
            dbc.CardBody(
                content,
                id={'type': 'reward-card-body', 'index': reward_id}
            ),
            className=card_class,
            id={'type': 'reward-card', 'index': reward_id}
        ),
        className="mb-4"
    )



def rewards_page(username):
  

    reward_items = [
        {"id": "stepper", "title": "Golden Stepper Badge", "points": 100, "icon": "👣"},
        {"id": "hydration", "title": "Hydration Hero Badge", "points": 150, "icon": "💧"},
        {"id": "legend", "title": "Fitness Legend Badge", "points": 300, "icon": "👑"},
        {"id": "nerd", "title": "Nutrition Nerd Badge", "points": 200, "icon": "🍎"},
        {"id": "logger", "title": "Consistent Logger Badge", "points": 180, "icon": "📝"},
        {"id": "champ", "title": "Power Champ Badge", "points": 350, "icon": "💪"},
    ]


    claimed_rewards = get_claimed_rewards(username)


    return dbc.Container(fluid=True, children=[
        dbc.Row([
            dbc.Col(create_sidebar(), width=2),
            dbc.Col([
                html.Div(className="rewards-page-wrapper", children=[
                    dbc.Row([
                        dbc.Col([
                            html.Div(className="rewards-hero", children=[
                                html.Div("🎁 Rewards", className="rewards-header"),
                                html.Div(
                                    "Use your points to unlock awesome badges, titles, and personalization!",
                                    className="rewards-subtext"
                                ),
                            ])
                        ], width=9),


                        dbc.Col([html.Div(id="points-balance", className="points-balance")],
                                width=3, style={"display": "flex", "alignItems": "center", "justifyContent": "flex-end"})
                    ]),


                    html.Div(id="claim-status", className="my-2"),


                    dbc.Row([
                        dbc.Col(
                            reward_card(
                                item["title"],
                                item["points"],
                                item["id"],
                                item["icon"],
                                claimed_rewards.get(item["id"])
                            ),
                            width=4
                        ) for item in reward_items
                    ], className="rewards-row", justify="start")
                ])
            ], width=10)
        ])
    ])
