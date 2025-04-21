#Dash & Component Imports 
from dash import Input, Output, State, ctx, dash, ALL, MATCH
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

#Services 
from services.user_service import fetch_user_points, update_user_points
from services.rewards_service import mark_reward_claimed, get_claimed_rewards

#UI Components 
from components.rewards_ui import reward_card_content


#Callback Registration 
def register_rewards_callbacks(dash_app):

    #Handle Reward Claim Button Clicks 
    @dash_app.callback(
        Output("claim-status", "children"),
        Output("points-balance", "children"),
        Input({'type': 'claim-button', 'index': ALL}, 'n_clicks'),
        State("username-store", "data"),
        prevent_initial_call=False
    )
    def handle_rewards(n_clicks_list, username_data):
    
        if not username_data or 'username' not in username_data:
            raise PreventUpdate

        username = username_data["username"]
        triggered = ctx.triggered_id

        if triggered is None or triggered == "username-store":
            current_points = fetch_user_points(username)
            return dash.no_update, f"{current_points} Points"

        if isinstance(triggered, dict) and triggered.get("type") == "claim-button":
            reward_id = triggered["index"]

            reward_lookup = {
                "stepper": ("Golden Stepper Badge", 100),
                "hydration": ("Hydration Hero Badge", 150),
                "legend": ("Fitness Legend Title", 300),
                "nerd": ("Nutrition Nerd Badge", 200),
                "avatar": ("Custom Avatar Unlock", 500),
                "logger": ("Consistent Logger Badge", 180),
                "theme": ("Theme: Aqua Pulse", 250),
                "champ": ("Power Champ Title", 350)
            }

            reward_name, cost = reward_lookup.get(reward_id, (None, None))
            if not reward_name:
                return dbc.Alert("Invalid reward selected.", color="danger", dismissable=True), dash.no_update

            current_points = fetch_user_points(username)
            if current_points < cost:
                return dbc.Alert("Not enough points to claim this reward.", color="danger", dismissable=True), f"{current_points} Points"

            was_claimed = mark_reward_claimed(username, reward_id, reward_name)
            if not was_claimed:
                return dbc.Alert("You’ve already claimed this reward.", color="warning", dismissable=True), f"{current_points} Points"

            new_balance = current_points - cost
            update_user_points(username, new_balance)

            msg = f"You claimed: {reward_name}! 🎉 Your balance is now {new_balance} points."
            return dbc.Alert(msg, color="success", dismissable=True), f"{new_balance} Points"

        raise PreventUpdate

    #Update a Single Reward Card After Claim 
    @dash_app.callback(
        Output({'type': 'reward-card-body', 'index': MATCH}, 'children'),
        Output({'type': 'reward-card', 'index': MATCH}, 'className'),
        Input({'type': 'claim-button', 'index': MATCH}, 'n_clicks'),
        State("username-store", "data"),
        prevent_initial_call=True
    )
    def update_single_card(n_clicks, username_data):
 
        if not username_data or 'username' not in username_data:
            raise PreventUpdate

        username = username_data["username"]
        reward_id = ctx.triggered_id["index"]

        reward_lookup = {
            "stepper": ("Golden Stepper Badge", 100, "👣"),
            "hydration": ("Hydration Hero Badge", 150, "💧"),
            "legend": ("Fitness Legend Badge", 300, "👑"),
            "nerd": ("Nutrition Nerd Badge", 200, "🍎"),
            "logger": ("Consistent Logger Badge", 180, "📝"),
            "champ": ("Power Champ Badge", 350, "💪")
        }

        reward_name, cost, icon = reward_lookup.get(reward_id, (None, None, None))
        if not reward_name:
            raise PreventUpdate

        claimed_rewards = get_claimed_rewards(username)
        claimed_date = claimed_rewards.get(reward_id)

        content, claimed = reward_card_content(
            title=reward_name,
            points_required=cost,
            reward_id=reward_id,
            icon=icon,
            claimed_date=claimed_date
        )

        card_class = "reward-card"
        if claimed:
            card_class += " reward-claimed-gold sparkle"

        return content, card_class
