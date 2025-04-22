#Imports 
from dash import Input, Output, html
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta

#Services
from services.challenge_service import (
    fetch_challenges,
    fetch_patient_progress,
    update_challenge_progress
)
from services.user_service import fetch_user_points


#Calculate Time Remaining for Challenges 
def calculate_time_remaining(challenge_type):
    
    now = datetime.now()

    if challenge_type == "daily":
        end_time = now.replace(hour=23, minute=59, second=59)
    elif challenge_type == "weekly":
        days_until_sunday = 6 - now.weekday()
        end_time = now + timedelta(days=days_until_sunday)
    elif challenge_type == "monthly":
        next_month = now.replace(day=28) + timedelta(days=4)
        end_time = next_month.replace(day=1, hour=23, minute=59, second=59) - timedelta(days=1)
    else:
        return "Unknown"

    time_remaining = end_time - now
    return f"{time_remaining.days} days, {time_remaining.seconds // 3600} hours left"


#Callback Registration 
def register_challenges_callbacks(dash_app):

    @dash_app.callback(
        [
            Output("user-points", "children"),
            Output("daily-title", "children"),
            Output("weekly-title", "children"),
            Output("monthly-title", "children"),
            Output("daily-challenges", "children"),
            Output("weekly-challenges", "children"),
            Output("monthly-challenges", "children")
        ],
        Input("username-store", "data")
    )
    def load_challenges(username_data):
        
        if not username_data:
            return (
                "User not found.",
                "Daily Challenges (0/0)",
                "Weekly Challenges (0/0)",
                "Monthly Challenges (0/0)",
                html.Div(),
                html.Div(),
                html.Div()
            )

        username = username_data.get("username")
        challenges = fetch_challenges()
        user_points = fetch_user_points(username)

        if not challenges:
            return (
                f"Points: {user_points}",
                "Daily Challenges (0/0)",
                "Weekly Challenges (0/0)",
                "Monthly Challenges (0/0)",
                html.Div("No challenges available."),
                html.Div(),
                html.Div()
            )

        #Configuration 
        progress_colors = {
            "daily": "success",
            "weekly": "primary",
            "monthly": "info"
        }

        categorized_challenges = {"daily": [], "weekly": [], "monthly": []}
        completed_counts = {"daily": 0, "weekly": 0, "monthly": 0}
        total_counts = {"daily": 0, "weekly": 0, "monthly": 0}

        #Process Each Challenge 
        for challenge in challenges:
            challenge_type = challenge["challenge_type"]
            goal = challenge["goal"]

            #Update user progress silently (log suppression enabled)
            update_challenge_progress(username, challenge["id"], amount=0, suppress_completion_logs=True)
            progress = fetch_patient_progress(username, challenge["id"])

            progress_rounded = round(progress)
            goal_rounded = round(goal)
            challenge_color = progress_colors.get(challenge_type, "info")
            completed = progress_rounded >= goal_rounded

            total_counts[challenge_type] += 1
            if completed:
                completed_counts[challenge_type] += 1

            #Build UI Elements
            time_remaining_text = calculate_time_remaining(challenge_type)

            challenge_status_badge = (
                dbc.Badge("Completed!", color="success", className="completed-badge")
                if completed
                else dbc.Badge("Not Completed", color="danger", className="not-completed-badge")
            )

            challenge_card = dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.P(challenge["description"], className="challenge-description"),
                        challenge_status_badge
                    ], className="challenge-header"),

                    dbc.Progress(
                        value=progress_rounded,
                        max=goal_rounded,
                        striped=True,
                        animated=True,
                        color=challenge_color
                    ),

                    html.P(
                        f"{progress_rounded}/{goal_rounded} completed",
                        className="challenge-progress-text"
                    ),

                    html.Div([
                        html.Span(
                            f"🏅 Earn {challenge['reward_points']} points",
                            className="challenge-points"
                        ),
                        html.Span(
                            f"⏳ {time_remaining_text}",
                            className="time-remaining"
                        )
                    ], className="challenge-footer-row")
                ]),
                className="challenge-card challenge-completed-gold sparkle"
                if completed else "challenge-card"
            )

            categorized_challenges[challenge_type].append(challenge_card)

        #Section Titles 
        daily_title = f"Daily Challenges ({completed_counts['daily']}/{total_counts['daily']})"
        weekly_title = f"Weekly Challenges ({completed_counts['weekly']}/{total_counts['weekly']})"
        monthly_title = f"Monthly Challenges ({completed_counts['monthly']}/{total_counts['monthly']})"

        return (
            f"Points: {user_points}",
            daily_title,
            weekly_title,
            monthly_title,
            categorized_challenges["daily"],
            categorized_challenges["weekly"],
            categorized_challenges["monthly"]
        )
