from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from components.sidebar import create_sidebar
from services.user_service import fetch_user_data, METRIC_LABELS, METRIC_GOAL_BEHAVIOR
from services.goals_service import get_patient_goals
from services.goal_utils import calculate_goal_progress

def create_goal_donut(metric, value, goal, percent, behavior="cumulative"):

    ring_color = get_ring_color(percent)

    if behavior == "change":
        completed = percent
        remaining = max(100 - percent, 0)
    else:
        remaining = max(goal - value, 0)
        completed = min(value, goal)

    fig = go.Figure(data=[go.Pie(
        labels=["Completed", "Remaining"],
        values=[completed, remaining],
        hole=0.7,
        marker=dict(
            colors=[ring_color, "#eaeaea"],
            line=dict(color="#f8f9fa", width=0)
        ),
        textinfo="none",
        hoverinfo="label+value+percent",
        sort=False
    )])

    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        annotations=[dict(
            text=f"{percent}%",
            x=0.5, y=0.5,
            font_size=22,
            font_color='white',
            font_family="sans-serif",
            showarrow=False
        )]
    )

    return dcc.Graph(
        figure=fig,
        config={"displayModeBar": False},
        style={"height": "220px", "width": "100%"}
    )    

def get_ring_color(percent):

    if percent >= 100:
        return "#00b894"  #Teal green for fully completed
    elif percent >= 50:
        return "#fdcb6e"  #Warm yellow for halfway there
    else:
        return "#d63031"  #Soft red for below 50% progress


def generate_goal_section(username):
    print(f"[DEBUG] generate_goal_section for: {username}")

    goals = get_patient_goals(username)
    print(f"[DEBUG] Retrieved {len(goals)} goals")

    user_data = fetch_user_data(username)
    print(f"[DEBUG] User data keys: {list(user_data.keys()) if user_data else 'No data'}")

    if not goals or not user_data:
        print("[DEBUG] No goals or user data found")
        return dbc.Alert("No goals found. Head to 'Set Goals' to create one!", color="info")

    donut_cards = []

    for goal in goals:
        metric = getattr(goal, "metric_name", None)
        target = getattr(goal, "goal_value", None)
        goal_type = getattr(goal, "goal_type", "daily")

        if not metric or target is None:
            print("[DEBUG] Skipping invalid goal - missing metric or target")
            continue

        _, _, _, y_data, progress_value = calculate_goal_progress(
            username, metric, goal_type, goal_value=target
        )

        if progress_value is None:
            progress_value = 0

        print(f"[DEBUG] Goal - Metric: {metric}, Target: {target}, Progress Value: {progress_value}")
        behavior = METRIC_GOAL_BEHAVIOR.get(metric, "cumulative")

        if behavior == "change":
            percent = progress_value
            last_logged = y_data.iloc[-1] if isinstance(y_data, pd.Series) and not y_data.empty else 0
            value_display = f"{last_logged:.2f} / {target:.2f}"

            donut = create_goal_donut(
                metric=metric.replace("latest_", "").replace("_", " ").title(),
                value=last_logged,
                goal=target,
                percent=percent,
                behavior=behavior  
            )
        else:
            percent = min(100, round((progress_value / target) * 100, 1)) if target else 0
            value_display = f"{progress_value:.2f} / {target:.2f}"

            donut = create_goal_donut(
                metric=metric.replace("latest_", "").replace("_", " ").title(),
                value=progress_value,
                goal=target,
                percent=percent,
                behavior=behavior  
            )

        donut_card = dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.Span(
                        metric.replace("latest_", "").replace("_", " ").title(),
                        style={"color": "white", "fontWeight": "bold", "fontSize": "18px", "fontFamily": "sans-serif"}
                    ),
                    className="text-center"
                ),
                dbc.CardBody([
                    donut,
                    html.P(
                        value_display,
                        style={"color": "white", "fontWeight": "bold"},
                        className="text-center mt-2"
                    ),
                    html.Div(
                        html.Span(goal_type.upper(), className="goal-type-badge"),
                        className="text-center mt-1"
                    )
                ])
            ], className="goal-progress-card")
        ], width=3, className="mb-4")

        donut_cards.append(donut_card)

    print(f"[DEBUG] Finished rendering {len(donut_cards)} donut cards")
    return dbc.Row(donut_cards, className="goal-donut-row")

def dashboard_page(username):
    return dbc.Container([

        dbc.Row([
            dbc.Col(create_sidebar(), width=2),

            dbc.Col([

                dbc.Row([
                    dbc.Col(html.Div(id='summary-container', className="metrics-row"), width=12)
                ], className="justify-content-center"),
                
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Label("Select Metric:", className="dropdown-label"),
                            dcc.Dropdown(
                                id="metric-dropdown",
                                options=[{"label": label, "value": key} for key, label in METRIC_LABELS.items()],
                                value="latest_fasting_blood_sugar",
                                clearable=False,
                                className="dropdown-style"
                            )
                        ], className="dropdown-container"),
                    ], width=6),

                    dbc.Col([
                        html.H5(id="graph-label", className="graph-label")
                    ], width=6, style={"display": "flex", "alignItems": "center", "justifyContent": "center"})
                ], className="dropdown-label-row"),

                dbc.Row([
                    dbc.Col(html.Div(id="graph-container", className="graph-container"), width=8),
                    dbc.Col([
                        html.Div(id="rotating-right-metric", className="right-metric"),
                        html.Div([
                            html.Button("◀", id="prev-metric-btn", className="metric-btn"),
                            html.Button("▶", id="next-metric-btn", className="metric-btn")
                        ], className="metric-navigation"),
                        dcc.Interval(id="right-metric-interval", interval=5000, n_intervals=0)
                    ], width=4),
                ], className="graph-metric-row"),

        
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("🎯 Your Goals", className="goal-section-title"),
                            dbc.CardBody(html.Div(id="goal-section-content"))
                        ], className="goal-section-card mt-4")
                    ], width=12)
                ]),

                dbc.Row([
                    dbc.Col(html.Div(id="streak-box"), width=4),
                    dbc.Col(html.Div(id="daily-quote"), width=4),
                    dbc.Col(html.Div(id="badge-carousel"), width=4)
                ], className="mt-4"),

                dcc.Interval(id="quote-interval", interval=8000, n_intervals=0),
                dcc.Interval(id="badge-interval", interval=6000, n_intervals=0),


                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("📊 Your Metrics Overview", className="metric-grid-title"),
                            dbc.CardBody([
                                dbc.RadioItems(
                                    id="metric-time-filter",
                                    options=[
                                        {"label": "Day", "value": "day"},
                                        {"label": "Week", "value": "week"},
                                        {"label": "Month", "value": "month"},
                                    ],
                                    value="day",
                                    inline=True,
                                    className="metric-filter-radio"
                                ),
                                dcc.Loading(
                                    id="loading-metric-grid",
                                    type="circle",
                                    color="#004a77",  
                                    fullscreen=False,
                                    children=html.Div(id="metric-grid-container", className="metric-grid")
                                )
                            ])
                        ], className="metric-overview-card")
                    ], width=12)
                ], className="mt-4"),

                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("🏁 Almost There!", className="challenge-close-title"),
                            dbc.CardBody(html.Div(id="near-complete-challenges"))
                        ], className="near-challenges-card")
                    ], width=12)
                ], className="mt-4")

            ], width=10)
        ])
    ], fluid=True)
