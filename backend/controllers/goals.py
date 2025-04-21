#Dash and Plotly Imports 
from dash import Input, Output, State, html, dcc, MATCH, callback_context, ALL, dash
import plotly.graph_objs as go

#Standard Library 
from datetime import datetime, timedelta
import calendar
import pandas as pd

#Services and Models 
from services.goals_service import (
    set_patient_goal,
    get_patient_goals,
    delete_patient_goal
)
from services.goal_utils import calculate_goal_progress
from services.user_service import (
    METRIC_LABELS,
    fetch_health_history,
    GOAL_TYPE_OPTIONS_BY_METRIC,
    METRIC_GOAL_BEHAVIOR
)
from models.patientGoal import PatientGoal


#Callback Registration 
def register_goals_callbacks(dash_app):

    @dash_app.callback(
        Output("goal-feedback-alert", "children"),
        Output("goal-feedback-alert", "is_open"),
        Input("save-goal-btn", "n_clicks"),
        State("goal-metric-dropdown", "value"),
        State("goal-value-input", "value"),
        State("goal-type-dropdown", "value"),
        State("username-store", "data"),
        prevent_initial_call=True
    )
    def save_goal(n_clicks, metric, goal_value, goal_type, user_data):
        """Save a new goal for the logged-in user."""
        if not user_data or not metric or goal_value is None or goal_value < 0.000001:
            return "⚠️ Please enter a value greater than 0.", True

        username = user_data["username"]
        success = set_patient_goal(username, metric, float(goal_value), goal_type)

        return ("✅ Goal saved!" if success else "❌ Error saving goal."), True

    @dash_app.callback(
        Output("existing-goals-display", "children"),
        Input("goal-feedback-alert", "is_open"),
        Input("goal-delete-alert", "is_open"),
        Input("goal-refresh-trigger", "data"),
        Input("goal-load-trigger", "data"),  #Allows loading on initial visit
        State("username-store", "data"),
        prevent_initial_call=False
    )
    def update_existing_goals(_, __, ___, ____, user_data):
        """Render all goals saved by the user."""
        if not user_data:
            return html.P("Log in to view your goals.")

        username = user_data["username"]
        goals = get_patient_goals(username)

        if not goals:
            return html.P("No goals saved yet.")

        return html.Div([
            html.H4("📌 Your Goals:"),
            html.Div([
                html.Div([
                    #Header row with goal details
                    html.Div([
                        html.Div(METRIC_LABELS.get(goal.metric_name, goal.metric_name), className="goal-metric-name"),
                        html.Div(f"Goal: {goal.goal_value:.2f}", className="goal-value"),
                        html.Div(goal.goal_type.capitalize(), className="goal-type-label")
                    ], className="goal-card-header"),

                    #Hidden storage for goal ID
                    dcc.Store(id={"type": "goal-id-store", "index": goal.id}, data=goal.id),

                    #Action buttons
                    html.Div([
                        html.Button("📊 View Graph", id={"type": "view-graph-btn", "index": goal.id},
                                    className="btn btn-info btn-sm me-2"),
                        html.Button("❌ Close Graph", id={"type": "close-graph-btn", "index": goal.id},
                                    className="btn btn-secondary btn-sm"),
                        html.Button("🗑️ Delete", id={"type": "delete-goal-btn", "index": goal.id},
                                    className="btn btn-danger btn-sm")
                    ], className="d-flex gap-2 mt-2"),

                    #Output container for goal graph
                    html.Div(id={"type": "goal-graph-output", "index": goal.id}, className="mt-2")

                ], className="goal-card") for goal in goals
            ])
        ])

    @dash_app.callback(
        Output("goal-type-dropdown", "options"),
        Output("goal-type-dropdown", "disabled"),
        Input("goal-metric-dropdown", "value")
    )
    def update_goal_type_options(selected_metric):
        """Enable and populate goal type dropdown based on metric selected."""
        if not selected_metric:
            return [], True

        options = GOAL_TYPE_OPTIONS_BY_METRIC.get(selected_metric, [])
        return [{"label": opt.capitalize(), "value": opt} for opt in options], False

    @dash_app.callback(
        Output("goal-delete-alert", "children"),
        Output("goal-delete-alert", "is_open"),
        Output("goal-refresh-trigger", "data"),
        Input({"type": "delete-goal-btn", "index": ALL}, "n_clicks"),
        State({"type": "delete-goal-btn", "index": ALL}, "id"),
        prevent_initial_call=True
    )
    def handle_delete_goal(n_clicks_list, ids):
        """Delete a specific goal when delete button is clicked."""
        ctx = callback_context
        if not ctx.triggered:
            return "", False, dash.no_update

        for i, n_clicks in enumerate(n_clicks_list):
            if n_clicks:
                goal_id = ids[i]["index"]
                success = delete_patient_goal(goal_id)
                message = "✅ Goal deleted." if success else "❌ Error deleting goal."
                return message, True, datetime.utcnow().timestamp()

        return "", False, dash.no_update

    @dash_app.callback(
        Output({"type": "goal-graph-output", "index": MATCH}, "children"),
        [
            Input({"type": "view-graph-btn", "index": MATCH}, "n_clicks"),
            Input({"type": "close-graph-btn", "index": MATCH}, "n_clicks")
        ],
        State({"type": "goal-id-store", "index": MATCH}, "data"),
        State("username-store", "data"),
        prevent_initial_call=True
    )
    def toggle_graph(view_clicks, close_clicks, goal_id, user_data):
        """Toggle visibility of a graph showing progress for a selected goal."""
        ctx = callback_context
        if not ctx.triggered or not user_data:
            return ""

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if "close-graph-btn" in trigger_id:
            return ""

        username = user_data["username"]
        goal = PatientGoal.query.get(goal_id)
        if not goal:
            return html.P("Goal not found.")

        return generate_goal_chart(
            username=username,
            metric_name=goal.metric_name,
            goal_value=goal.goal_value,
            goal_type=goal.goal_type
        )


#Utility: Generate Goal Progress Graph 
def generate_goal_chart(username, metric_name, goal_value, goal_type="daily"):

    start, end, x_data, y_data, progress = calculate_goal_progress(
        username, metric_name, goal_type, goal_value
    )

    if x_data is None or y_data is None or len(x_data) == 0:
        return html.P("No logged data for this period.")

    behavior = METRIC_GOAL_BEHAVIOR.get(metric_name, "cumulative")

    #Base progress line
    graph_data = [
        go.Scatter(
            x=x_data,
            y=y_data.round(2),
            mode="lines+markers",
            name="Your Progress",
            line=dict(color="royalblue")
        )
    ]

    #Add goal/reference lines depending on behavior
    if behavior == "change":
        graph_data.append(go.Scatter(
            x=[start, end],
            y=[goal_value, goal_value],
            mode="lines",
            name="Target",
            line=dict(dash="dash", color="orange")
        ))
        if len(y_data) > 0:
            start_value = y_data.iloc[0]
            graph_data.append(go.Scatter(
                x=[start, end],
                y=[start_value, start_value],
                mode="lines",
                name="Start Value",
                line=dict(dash="dot", color="gray")
            ))
    else:
        graph_data.append(go.Scatter(
            x=[start, end],
            y=[goal_value, goal_value],
            mode="lines",
            name="Goal",
            line=dict(dash="dash", color="orange")
        ))

    return dcc.Graph(
        config={"displayModeBar": False},
        figure={
            "data": graph_data,
            "layout": go.Layout(
                title=f"{METRIC_LABELS.get(metric_name, metric_name)} Goal Progress",
                height=300,
                margin=dict(t=40, b=40, l=50, r=10),
                yaxis=dict(title="Value"),
                xaxis=dict(title="Date", range=[start, end])
            )
        }
    )
