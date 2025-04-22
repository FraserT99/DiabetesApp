#Dash & Component Imports 
import dash
from dash import html, Input, Output, State, ctx, dcc
import dash_bootstrap_components as dbc

#Services 
from services.user_service import fetch_user_data, fetch_recent_activity, update_user_data
from services.challenge_service import fetch_challenges, fetch_patient_progress
from services.rewards_service import get_claimed_rewards


#Callback Registration 
def register_profile_callbacks(dash_app):
    """Registers all callbacks for the Profile Page."""

    #Set Active Profile Tab Based on Button Click 
    @dash_app.callback(
        Output("active-profile-tab", "data"),
        [
            Input("profile-tab-overview", "n_clicks"),
            Input("profile-tab-edit", "n_clicks"),
            Input("profile-tab-privacy", "n_clicks"),
        ],
        prevent_initial_call=True
    )
    def set_active_tab(*n_clicks):
        """Track which profile tab is selected based on clicked input."""
        triggered = ctx.triggered_id
        if triggered:
            return triggered.replace("profile-tab-", "")
        return dash.no_update

    #Render Profile Tab Content 
    @dash_app.callback(
        Output("profile-content", "children"),
        Input("active-profile-tab", "data"),
        State("username-store", "data")
    )
    def render_tab(tab, username_data):
        """Render the UI for the selected profile tab."""
        if not username_data or "username" not in username_data:
            return html.Div("User not found")

        username = username_data["username"]
        user_data = fetch_user_data(username)
        activity = fetch_recent_activity(username)

        #OVERVIEW TAB 
        if tab == "overview":
            all_challenges = fetch_challenges()
            daily_challenges = [ch for ch in all_challenges if ch["challenge_type"] == "daily"]

            challenge_progress_display = []
            for ch in daily_challenges:
                progress = fetch_patient_progress(username, ch["id"])
                if progress >= ch["goal"]:
                    display = f"✅ {ch['name']} – Completed"
                else:
                    display = f"{ch['name']} – {int(progress)}/{int(ch['goal'])}"
                challenge_progress_display.append(display)

            claimed_rewards = get_claimed_rewards(username)

            badge_lookup = {
                "stepper": ("Golden Stepper Badge", "👣", "Take 5,000+ steps in a day."),
                "hydration": ("Hydration Hero Badge", "💧", "Log 2L+ of water in one day."),
                "legend": ("Fitness Legend Badge", "👑", "Complete all daily challenges in one day."),
                "nerd": ("Nutrition Nerd Badge", "🍎", "Log your meals consistently for 3 days."),
                "logger": ("Consistent Logger Badge", "📝", "Log any data 7 days in a row."),
                "champ": ("Power Champ Badge", "💪", "Win a leaderboard challenge."),
            }

            badge_cards = []
            for reward_id, (name, icon, tooltip) in badge_lookup.items():
                is_claimed = reward_id in claimed_rewards
                date = claimed_rewards[reward_id].strftime("%Y-%m-%d") if is_claimed else None

                card_style = {
                    "width": "10rem",
                    "margin": "0.5rem",
                    "opacity": 1.0 if is_claimed else 0.4,
                    "border": "2px solid #ccc" if not is_claimed else None,
                    "cursor": "default",
                }

                card = dbc.Card([
                    dbc.CardBody([
                        html.Div(icon, className="display-4 text-center"),
                        html.H6(name, className="text-center mt-2"),
                        html.P(f"Claimed: {date}" if is_claimed else "Locked", className="text-center text-muted small")
                    ])
                ], style=card_style, id=f"badge-{reward_id}")

                tooltip_component = dbc.Tooltip(
                    tooltip,
                    target=f"badge-{reward_id}",
                    placement="top",
                    delay={"show": 250, "hide": 100},
                )

                #Append both card and tooltip
                badge_cards.extend([card, tooltip_component])

            #Return full overview content layout
            return html.Div([
                #Personal Info
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Personal Information", className="profile-section-title"),
                            dbc.CardBody([
                                dbc.Row([
                                    #Basic Info
                                    dbc.Col([
                                        html.H5("🧍 Basic Info", className="profile-subsection"),
                                        html.P(f"Full Name: {user_data.get('first_name', '')} {user_data.get('last_name', '')}", className="profile-text"),
                                        html.P(f"Age: {user_data.get('age', 'N/A')}", className="profile-text"),
                                        html.P(f"Gender: {user_data.get('gender', 'N/A')}", className="profile-text"),
                                        html.P(f"Ethnicity: {user_data.get('ethnicity', 'N/A')}", className="profile-text"),
                                        html.P(f"Diagnosis: {user_data.get('diagnosis', 'N/A')}", className="profile-text"),
                                    ], width=4),
                                    #Lifestyle
                                    dbc.Col([
                                        html.H5("💬 Lifestyle", className="profile-subsection"),
                                        html.P(f"Smoking: {user_data.get('smoking', 'N/A')}", className="profile-text"),
                                        html.P(f"Alcohol: {user_data.get('alcohol_consumption', 'N/A')} units/week", className="profile-text"),
                                        html.P(f"Activity: {user_data.get('physical_activity', 'N/A')} hrs/week", className="profile-text"),
                                        html.P(f"Diet: {user_data.get('diet_quality', 'N/A')}/10", className="profile-text"),
                                        html.P(f"Sleep: {user_data.get('sleep_quality', 'N/A')}/10", className="profile-text"),
                                    ], width=4),
                                    #Medical History
                                    dbc.Col([
                                        html.H5("🩺 Medical History", className="profile-subsection"),
                                        html.P(f"Hypertension: {user_data.get('hypertension', 'N/A')}", className="profile-text"),
                                        html.P(f"Pre-Diabetes: {user_data.get('previous_pre_diabetes', 'N/A')}", className="profile-text"),
                                        html.P(f"PCOS: {user_data.get('polycystic_ovary_syndrome', 'N/A')}", className="profile-text"),
                                        html.P(f"Gestational Diabetes: {user_data.get('gestational_diabetes', 'N/A')}", className="profile-text"),
                                        html.P(f"Family History Diabetes: {user_data.get('family_history_diabetes', 'N/A')}", className="profile-text"),
                                    ], width=4),
                                ]),
                                html.Hr(),
                                dbc.Row([
                                    #Medications
                                    dbc.Col([
                                        html.H5("💊 Medications", className="profile-subsection"),
                                        html.P(f"Antihypertensives: {user_data.get('antihypertensive_medications', 'N/A')}", className="profile-text"),
                                        html.P(f"Statins: {user_data.get('statins', 'N/A')}", className="profile-text"),
                                        html.P(f"Antidiabetics: {user_data.get('antidiabetic_medications', 'N/A')}", className="profile-text"),
                                    ], width=4),
                                    #Checkups
                                    dbc.Col([
                                        html.H5("📅 Checkups & Adherence", className="profile-subsection"),
                                        html.P(f"Checkups Per Year: {user_data.get('medical_checkups_frequency', 'N/A')}", className="profile-text"),
                                        html.P(f"Medication Adherence: {user_data.get('medication_adherence', 'N/A')}/10", className="profile-text"),
                                        html.P(f"Health Literacy: {user_data.get('health_literacy', 'N/A')}/10", className="profile-text"),
                                    ], width=4),
                                    #Rewards
                                    dbc.Col([
                                        html.H5("🎯 Reward Summary", className="profile-subsection"),
                                        html.Div(f"{user_data.get('reward_points', 0)}", className="profile-reward"),
                                    ], width=4),
                                ])
                            ])
                        ], className="profile-section")
                    ], width=12)
                ]),

                html.Div(style={"height": "5px"}), 

                #Challenge + Activity Rows
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Daily Challenge Progress", className="profile-section-title"),
                            dbc.CardBody([
                                html.Ul([html.Li(display) for display in challenge_progress_display], className="profile-activity-list")
                            ])
                        ], className="profile-section")
                    ], width=6),

                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Recent Log Activity", className="profile-section-title"),
                            dbc.CardBody([
                                html.Ul([html.Li(f"📌 {event}") for event in activity], className="profile-activity-list")
                            ])
                        ], className="profile-section")
                    ], width=6),
                ], className="mt-4"),

                #Badges Section
                dbc.Card([
                    dbc.CardHeader("🏅 Claimed Badges", className="profile-section-title"),
                    dbc.CardBody([
                        html.Div(
                            badge_cards if badge_cards else html.P("No badges claimed yet."),
                            style={
                                "display": "flex",
                                "flexWrap": "wrap",
                                "gap": "1rem",
                                "justifyContent": "flex-start",
                                "alignItems": "stretch"
                            }
                        )
                    ])
                ], className="profile-section mt-4")
            ])

        #EDIT TAB 
        elif tab == "edit":
            return dbc.Card([
                dbc.CardHeader("✏️ Edit Profile", className="profile-section-title"),
                dbc.CardBody([
                    html.Div(id="save-status", className="mb-3 profile-text"),

                    dbc.Form([
                        dbc.Row([
                            #Left Column
                            dbc.Col([
                                dbc.Label("First Name", className="profile-subsection"),
                                dbc.Input(id="edit-first-name", type="text", value=user_data.get("first_name", ""), className="mb-3"),

                                dbc.Label("Last Name", className="profile-subsection"),
                                dbc.Input(id="edit-last-name", type="text", value=user_data.get("last_name", ""), className="mb-3"),

                                dbc.Label("Age", className="profile-subsection"),
                                dbc.Input(id="edit-age", type="number", value=user_data.get("age", ""), className="mb-3"),

                                dbc.Label("Gender", className="profile-subsection"),
                                dbc.Select(
                                    id="edit-gender",
                                    options=[{"label": "Male", "value": "Male"}, {"label": "Female", "value": "Female"}],
                                    value=user_data.get("gender", "Male"),
                                    className="mb-3"
                                ),
                            ], width=6),

                            #Right Column
                            dbc.Col([
                                dbc.Label("Smoking", className="profile-subsection"),
                                dbc.Select(
                                    id="edit-smoking",
                                    options=[{"label": "No", "value": 0}, {"label": "Yes", "value": 1}],
                                    value=user_data.get("smoking", 0),
                                    className="mb-3"
                                )
                            ], width=6),
                        ]),

                        html.Div([
                            dbc.Button("💾 Save Changes", id="save-profile-btn", color="primary", className="profile-save-btn")
                        ], className="d-flex justify-content-center mt-4")
                    ])
                ])
            ], className="profile-section")

        #PRIVACY TAB 
        elif tab == "privacy":
            return dbc.Card([
                dbc.CardHeader("🔐 Privacy Settings", className="profile-section-title"),
                dbc.CardBody([
                    dbc.Form([
                        dbc.Checklist(
                            options=[{"label": "Show my profile on the leaderboard", "value": "show_on_leaderboard"}],
                            value=["show_on_leaderboard"] if user_data.get("show_on_leaderboard", True) else [],
                            id="privacy-leaderboard-toggle",
                            switch=True,
                            className="mb-3"
                        ),
                        dbc.Checklist(
                            options=[{"label": "Receive email alerts", "value": "email_alerts"}],
                            value=["email_alerts"] if user_data.get("email_alerts", True) else [],
                            id="privacy-email-toggle",
                            switch=True,
                            className="mb-3"
                        ),
                        dbc.Checklist(
                            options=[{"label": "Receive SMS alerts", "value": "sms_alerts"}],
                            value=["sms_alerts"] if user_data.get("sms_alerts", False) else [],
                            id="privacy-sms-toggle",
                            switch=True,
                            className="mb-3"
                        ),
                        dbc.Checklist(
                            options=[{"label": "Allow data export", "value": "data_export_consent"}],
                            value=["data_export_consent"] if user_data.get("data_export_consent", False) else [],
                            id="privacy-export-toggle",
                            switch=True,
                            className="mb-4"
                        ),

                        html.Div(id="privacy-save-status", className="profile-text mb-2"),
                        dbc.Button("💾 Save Privacy Settings", id="save-privacy-btn", color="primary", className="profile-save-btn")
                    ])
                ])
            ], className="profile-section")

    #Save Profile Info 
    @dash_app.callback(
        Output("save-status", "children"),
        Input("save-profile-btn", "n_clicks"),
        State("username-store", "data"),
        State("edit-first-name", "value"),
        State("edit-last-name", "value"),
        State("edit-age", "value"),
        State("edit-gender", "value"),
        State("edit-smoking", "value"),
        prevent_initial_call=True
    )
    def save_profile(n_clicks, username_data, first_name, last_name, age, gender, smoking):
        """Save updated personal profile data."""
        if not username_data or not username_data.get("username"):
            return "Error: User not found.", dash.no_update

        updated_data = {
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "gender": gender,
            "smoking": bool(smoking),
        }

        success = update_user_data(username_data["username"], updated_data)
        return "✅ Profile updated!" if success else "❌ Update failed."

    #Trigger Tab Refresh After Save 
    @dash_app.callback(
        Output("active-profile-tab", "data", allow_duplicate=True),
        Input("refresh-flag", "data"),
        prevent_initial_call=True
    )
    def refresh_after_save(flag):
        """Refresh active tab when external flag updates."""
        return flag if flag else dash.no_update

    #Save Privacy Settings 
    @dash_app.callback(
        Output("privacy-save-status", "children"),
        Input("save-privacy-btn", "n_clicks"),
        State("username-store", "data"),
        State("privacy-leaderboard-toggle", "value"),
        State("privacy-email-toggle", "value"),
        State("privacy-sms-toggle", "value"),
        State("privacy-export-toggle", "value"),
        prevent_initial_call=True
    )
    def save_privacy_settings(n_clicks, username_data, leaderboard_val, email_val, sms_val, export_val):
        """Save user privacy preference toggles."""
        if not username_data or "username" not in username_data:
            return "❌ Error: User not found."

        updated_data = {
            "show_on_leaderboard": "show_on_leaderboard" in leaderboard_val,
            "email_alerts": "email_alerts" in email_val,
            "sms_alerts": "sms_alerts" in sms_val,
            "data_export_consent": "data_export_consent" in export_val,
        }

        success = update_user_data(username_data["username"], updated_data)
        return "✅ Privacy settings updated!" if success else "❌ Failed to save privacy settings."
