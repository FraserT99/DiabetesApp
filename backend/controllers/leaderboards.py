#Dash Imports 
from dash import Output, Input

#Services 
from services.leaderboard_service import fetch_leaderboard


#Callback Registration 
def register_leaderboard_callbacks(dash_app):
    
    @dash_app.callback(
        [
            Output("steps-leaderboard", "data"),
            Output("workout-leaderboard", "data"),
            Output("calories-leaderboard", "data"),
            Output("distance-leaderboard", "data"),
        ],
        [
            Input("steps-timeframe", "value"),
            Input("workout-timeframe", "value"),
            Input("calories-timeframe", "value"),
            Input("distance-timeframe", "value"),
        ]
    )
    def update_leaderboards(*timeframes):
       
        metrics = [
            "latest_steps_taken",
            "latest_workout_sessions",
            "latest_calories_burned",
            "latest_distance_walked",
        ]
        return [fetch_leaderboard(metric, tf) for metric, tf in zip(metrics, timeframes)]
