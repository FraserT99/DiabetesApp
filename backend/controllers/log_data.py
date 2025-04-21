#Dash and UI Imports 
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

#Models and Database 
from models.user import User
from models.patient import Patient
from models.challenge import Challenge
from models import db

#Services 
from services.log_data_service import fetch_metric_history
from services.user_service import METRIC_LABELS
from services.challenge_service import (
    update_challenge_progress,
    get_cumulative_metric,
    challenge_to_metric
)


#Callback Registration 
def register_log_data_callbacks(dash_app):


    @dash_app.callback(
        [
            Output("update-message", "children"),
            Output("recent-metric-history", "children")
        ],
        [
            Input("update-metric-btn", "n_clicks"),
            Input("log-metric-dropdown", "value")
        ],
        [
            State("log-metric-dropdown", "value"),
            State("log-new-value", "value"),
            State("username-store", "data")
        ]
    )
    def handle_metric_update_and_logs(n_clicks, selected_metric_trigger, selected_metric, new_value, username_data):
      
        username = username_data.get("username") if username_data else None
        if not username:
            return "User not found.", dash.no_update

        user = User.query.filter_by(username=username).first()
        if not user or not user.patient:
            return "Patient record not found.", dash.no_update

        patient = user.patient

        #Metric Update Trigger
        if dash.callback_context.triggered_id == "update-metric-btn":
            if new_value is None:
                return "Please enter a value.", dash.no_update
            if new_value < 0.000001:
                return "Value must be greater than 0.", dash.no_update

            try:
                success = patient.update_health_metric(selected_metric, float(new_value))
                if success:
                    #Update all challenges related to this metric
                    challenges = Challenge.query.all()
                    for challenge in challenges:
                        if challenge_to_metric(challenge.name) == selected_metric:
                            update_challenge_progress(username, challenge.id, None)

                    return (
                        "Updated successfully!",
                        fetch_metric_history(patient.patient_id, selected_metric)
                    )
                else:
                    return "Failed to update.", dash.no_update

            except ValueError:
                return "Invalid input. Please enter a numeric value.", dash.no_update

        #Metric Change Trigger — just refresh log
        return (
            dash.no_update,
            fetch_metric_history(patient.patient_id, selected_metric)
        )

    @dash_app.callback(
        [
            Output("health-tips", "children"),
            Output("tips-title", "children")
        ],
        Input("log-metric-dropdown", "value")
    )
    def update_health_tips(selected_metric):

        #Dynamic titles mapped from METRIC_LABELS
        metric_titles = {
            key: f"Health Tips - {label}" for key, label in METRIC_LABELS.items()
        }

        #Hardcoded tips per metric (emoji-enhanced for UI)
        tips = {
            "latest_fasting_blood_sugar": [
                "🥦 Maintain a balanced diet rich in fiber.",
                "🚫 Avoid sugary drinks and processed foods.",
                "🚰 Stay hydrated and drink plenty of water.",
                "🏃 Engage in at least 30 minutes of physical activity daily.",
                "🛌 Ensure quality sleep, as poor rest can impact blood sugar levels."
            ],
            "latest_bmi": [
                "🍽️ Maintain a balanced calorie intake.",
                "🏋️ Exercise regularly to build lean muscle.",
                "🥤 Avoid processed foods and sugary drinks.",
                "🥗 Eat more whole foods, such as vegetables and lean proteins.",
                "🚶 Incorporate more walking and movement into your daily routine."
            ],
            "latest_calories_consumed": [
                "🍎 Track daily intake and avoid empty calories.",
                "🔥 Increase physical activity to balance intake.",
                "🥦 Prioritize whole, nutrient-dense foods.",
                "📊 Use a food diary to track and improve intake."
            ],
            "latest_protein_intake": [
                "🥩 Consume lean protein sources like chicken and fish.",
                "🥚 Eggs are a great source of complete protein.",
                "🌱 Consider plant-based proteins for variety.",
                "💪 Protein helps with muscle repair and recovery."
            ],
            "latest_steps_taken": [
                "🚶 Aim for 10,000 steps per day.",
                "📉 Monitor daily steps with a fitness tracker.",
                "🌳 Take breaks to walk outdoors for fresh air.",
                "📊 Set daily and weekly step goals."
            ]
        }

        selected_title = metric_titles.get(selected_metric, "Health Tips - General Wellness")
        selected_tips = tips.get(selected_metric, ["No tips available."])

        return html.Ul([
            html.Li(text, className="tip-item") for text in selected_tips
        ]), selected_title
