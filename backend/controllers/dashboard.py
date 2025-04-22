#Standard Library Imports 
from urllib.parse import parse_qs

#Third-Party Imports 
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

#Services (Backend Logic) 
from services.user_service import METRIC_CATEGORIES, fetch_user_data, fetch_health_history, METRIC_LABELS, THRESHOLDS
from services.rewards_service import get_claimed_rewards

#Controllers (Callback Registration) 
from controllers.challenges import register_challenges_callbacks
from controllers.log_data import register_log_data_callbacks
from controllers.leaderboards import register_leaderboard_callbacks
from controllers.profile import register_profile_callbacks
from controllers.rewards import register_rewards_callbacks
from controllers.goals import register_goals_callbacks

#UI Components 
from components.dashboard_ui import dashboard_page
from components.log_data_ui import log_data_page
from components.challenges_page_ui import challenges_page
from components.leaderboard_ui import leaderboard_page
from components.rewards_ui import rewards_page
from components.profile_ui import profile_page
from components.goals_ui import goals_page
from components.sidebar import create_sidebar
from components.graphs import create_metric_graph
from components.ui_helpers import generate_metric_card
from components.dashboard_ui import generate_goal_section


#App Initialisation 
def create_dashboard(app):
    """Create and return the Dash dashboard application."""
    dash_app = dash.Dash(
        __name__,
        server=app,
        url_base_pathname='/dashboard/',
        suppress_callback_exceptions=True,
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            '/static/styles/dashboard.css',
            '/static/styles/logdata.css',
            '/static/styles/challenges.css',
            '/static/styles/leaderboard.css',
            '/static/styles/profile.css',
            '/static/styles/rewards.css',
            '/static/styles/goals.css',
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
        ]
    )

    dash_app.layout = dbc.Container([
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='username-store', storage_type='memory'),
        dcc.Store(id='active-category-store', data="all", storage_type='memory'),
        html.Div(id="page-content")
    ], fluid=True)

    #Register Callback Controllers 
    register_challenges_callbacks(dash_app)
    register_log_data_callbacks(dash_app)
    register_leaderboard_callbacks(dash_app)
    register_profile_callbacks(dash_app)
    register_rewards_callbacks(dash_app)
    register_goals_callbacks(dash_app)

    #Callback: Store Username from URL Params 
    @dash_app.callback(
        Output('username-store', 'data'),
        [Input('url', 'search')],
        [State('username-store', 'data')]
    )
    def store_username(search, current_data):
        """Extract and store username from URL query string."""
        params = parse_qs(search.lstrip('?'))
        new_username = params.get('username', [None])[0]

        if new_username is None and current_data:
            return current_data

        print(f"[DEBUG] Storing username: {new_username}")
        return {'username': new_username}

    #Callback: Page Routing 
    @dash_app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname")],
        [State("username-store", "data")]
    )
    def display_page(pathname, username_data):
        """Render the appropriate page based on the URL path."""
        username = username_data.get('username') if username_data else None

        if pathname == "/log_data":
            return log_data_page(username)
        elif pathname == "/challenges":
            return challenges_page(username)
        elif pathname == "/leaderboard":
            return leaderboard_page()
        elif pathname.startswith("/rewards"):
            return rewards_page(username)
        elif pathname.startswith("/profile"):
            return profile_page(username)
        elif pathname.startswith("/goals"):
            return goals_page(username)
        else:
            return dashboard_page(username)

    #Callback: Update Sidebar Title 
    @dash_app.callback(
        Output('sidebar-title', 'children'),
        Input('username-store', 'data')
    )
    def update_sidebar_title(username_data):
        """Update sidebar with the user's name."""
        username = username_data.get('username', "User") if username_data else "User"
        return f"{username}'s Dashboard"

    #Callback: Load Dashboard Metric Summary 
    @dash_app.callback(
        Output('summary-container', 'children'),
        Input('username-store', 'data')
    )
    def load_dashboard(username_data):
        """Load user metadata into dashboard summary cards."""
        username = username_data.get('username') if username_data else None
        user_data = fetch_user_data(username)

        if not user_data:
            return html.Div("No data available.", className="no-data")

        metric_cards = [
            generate_metric_card("Patient Name", f"{user_data['first_name']} {user_data['last_name']}"),
            generate_metric_card("Patient Age", user_data['age']),
            generate_metric_card("Patient Gender", user_data['gender']),
        ]

        return html.Div(metric_cards, className="metrics-row")

    #Callback: Update Graph on Metric Selection 
    @dash_app.callback(
        Output('graph-container', 'children'),
        Output('graph-label', 'children'),
        [Input('username-store', 'data'), Input('metric-dropdown', 'value')]
    )
    def update_graph(username_data, selected_metric):
        """Update the metric graph dynamically."""
        username = username_data.get('username') if username_data else None
        df = fetch_health_history(username, selected_metric)

        if df.empty:
            return html.Div("No historical data available.", className="no-data"), METRIC_LABELS[selected_metric]

        df = df.sort_values("Date", ascending=True)

        return (
            create_metric_graph(df, METRIC_LABELS[selected_metric], THRESHOLDS.get(selected_metric, {})),
            METRIC_LABELS[selected_metric]
        )

    #Callback: Load Goal Section Donuts 
    @dash_app.callback(
        Output("goal-section-content", "children"),
        Input("username-store", "data")
    )
    def update_goal_section(username_data):
        """Render the goal progress donut cards."""
        username = username_data.get("username") if username_data else None
        return generate_goal_section(username)
    
    from services.log_data_service import get_consecutive_log_streak

    @dash_app.callback(
    Output("streak-box", "children"),
    Input("username-store", "data")
)
    def update_streak_box(username_data):
        username = username_data.get("username") if username_data else None
        if not username:
            return dbc.Alert("User not found", color="warning")

        streak = get_consecutive_log_streak(username)

        return dbc.Card([
            dbc.CardHeader("🔥 Log Streak", className="dashboard_streak-header"),
            dbc.CardBody([
                html.H3(f"{streak} Days", className="streak-count"),
                html.P("You've logged activity for this many days in a row!", className="dashboard_streak-caption")
            ])
        ], className="dashboard_streak-card")
        
    @dash_app.callback(
        Output("daily-quote", "children"),
        Input("quote-interval", "n_intervals")
    )
    def rotate_daily_quote(n):
        quotes = [
            "💪 *Progress, not perfection.*",
            "🏃 *One step at a time adds up to miles.*",
            "🥦 *Fuel your body, feed your goals.*",
            "🧘 *Small habits → big results.*",
            "🚰 *Hydration is motivation.*",
            "📈 *Your health is your wealth.*",
            "🔥 *Consistency beats intensity.*",
            "🌿 *Eat clean, feel strong.*",
            "🎯 *Discipline is remembering what you want.*",
            "🚴 *Your body hears everything your mind says.*"
        ]

        index = n % len(quotes)
        quote = quotes[index]

        return dbc.Card([
            dbc.CardHeader("🌟 Daily Motivation", className="dashboard_quote-header"),
            dbc.CardBody([
                html.Blockquote(quote, className="dashboard_quote-text")
            ])
        ], className="dashboard_quote-card")
        
    from services.log_data_service import fetch_metric_summary
    from services.user_service import METRIC_GOAL_BEHAVIOR
    from pytz import timezone
    from datetime import datetime, timedelta

    UK_TZ = timezone("Europe/London")  #Local timezone for correct goal windows

    @dash_app.callback(
    Output("metric-grid-container", "children"),
    Input("metric-time-filter", "value"),
    State("username-store", "data"),
    Input("active-category-store", "data")  #Use active category from store
)
    def update_metric_grid(filter_value, username_data, active_category):
        if not username_data or "username" not in username_data:
            return dbc.Alert("User not found", color="warning")

        username = username_data["username"]
        summary = fetch_metric_summary(username, period=filter_value)

        now = datetime.now(UK_TZ)
        if filter_value == "day":
            header = f"Metrics as of {now.strftime('%B %d, %Y')}"
        elif filter_value == "week":
            start = (now - timedelta(days=now.weekday())).strftime('%B %d')
            end = (now + timedelta(days=6 - now.weekday())).strftime('%B %d, %Y')
            header = f"Metrics for {start} – {end}"
        elif filter_value == "month":
            header = f"Metrics for {now.strftime('%B %Y')}"
        else:
            header = ""

        if not summary:
            return html.Div("No data available.")

        cards = []

        for i, (metric, data) in enumerate(summary.items()):
            category = get_metric_category(metric)

            #Apply filtering based on active category
            if active_category and active_category != "all" and category != active_category:
                continue

            behavior = METRIC_GOAL_BEHAVIOR.get(metric, "latest")
            label = data["label"].split(" (")[0].strip()
            value = data["value"]
            unit = data["unit"]

            if behavior == "cumulative":
                top_label = f"Total {label}"
            elif behavior == "average":
                top_label = f"Average {label}"
            elif behavior == "change":
                top_label = f"Total Change in {label}"
            else:
                top_label = label

            center_value = f"{value} {unit}"
            category_class = f"metric-card-{category}"

            card = dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Div(top_label, className="metric-card-label"),
                        html.Div(center_value, className="metric-card-value")
                    ])
                ])
            ],
            className=f"metric-summary-card {category_class}",
            key=f"{metric}-{filter_value}",
            style={"animationDelay": f"{i * 100}ms"})

            cards.append(card)

        return html.Div([
            #Filter Buttons + Legend
            dbc.Row([
                dbc.Col([], width=2),
                dbc.Col([], width=8),
                dbc.Col(
                    html.Div([
                        dbc.Button("🧬 Medical", id="legend-medical", className=f"legend medical {'active-legend' if active_category == 'medical' else ''}", n_clicks=0),
                        dbc.Button("🥗 Nutrition", id="legend-nutrition", className=f"legend nutrition {'active-legend' if active_category == 'nutrition' else ''}", n_clicks=0),
                        dbc.Button("🏃 Activity", id="legend-activity", className=f"legend activity {'active-legend' if active_category == 'activity' else ''}", n_clicks=0),
                        dbc.Button("⚖️ Body", id="legend-body", className=f"legend body {'active-legend' if active_category == 'body' else ''}", n_clicks=0),
                        ], className="category-legend"),
                    width=2
                )
            ], className="mb-1"),

            #Centered Date Label
            dbc.Row([
                dbc.Col(html.Div(header, className="metric-grid-period-label text-center"), width=12)
            ], className="mb-2"),

            #Metric Cards Grid
            dbc.Row([
                dbc.Col(card, width=12, md=6, lg=4, xl=3) for card in cards
            ], className="g-3")
        ])
   
    from services.challenge_service import get_nearly_completed_challenges

    @dash_app.callback(
        Output("near-complete-challenges", "children"),
        Input("username-store", "data")
    )
    def render_nearly_complete_challenges(username_data):
        if not username_data or "username" not in username_data:
            return dbc.Alert("User not found", color="warning")

        username = username_data["username"]
        challenges = get_nearly_completed_challenges(username)

        if not challenges:
            return html.Div("No near-complete challenges yet. Keep going! 💪", className="text-center text-muted")

        cards = []
        for ch in challenges:
            percent = min(int((ch["progress"] / ch["goal"]) * 100), 100)
            cards.append(
                dbc.Card([
                    dbc.CardBody([
                        html.H6(ch["name"], className="challenge-title"),
                        html.P(ch["description"], className="challenge-desc"),
                        dbc.Progress(value=percent, label=f"{percent}%", striped=True, animated=True, color="success" if percent >= 90 else "info")
                    ])
                ], className="almost-there-card")
            )

        return dbc.Row([dbc.Col(card, width=12, md=6, lg=4) for card in cards], className="g-3")

    @dash_app.callback(
        Output("badge-carousel", "children"),
        Input("badge-interval", "n_intervals"),
        State("username-store", "data")
    )
    def rotate_badges(n, username_data):
        if not username_data or "username" not in username_data:
            return dbc.Alert("No user loaded", color="danger")

        username = username_data["username"]
        claimed = get_claimed_rewards(username)

        if not claimed:
            return dbc.Card([
                dbc.CardHeader("🏅 Your Badges", className="dashboard_badge-header"),
                dbc.CardBody(html.Div("No badges claimed yet!", className="dashboard_badge-empty"))
            ], className="dashboard_badge-card")

        #Ordered list of badge IDs
        badge_list = list(claimed.items())
        index = n % len(badge_list)
        badge_id, date = badge_list[index]

        #Optional: Emoji/Icon mapping
        badge_icons = {
            "stepper": "👣",
            "hydration": "💧",
            "legend": "👑",
            "nerd": "🍎",
            "avatar": "🎭",
            "logger": "📝",
            "theme": "🎨",
            "champ": "💪"
        }

        badge_names = {
            "stepper": "Golden Stepper Badge",
            "hydration": "Hydration Hero",
            "legend": "Fitness Legend",
            "nerd": "Nutrition Nerd",
            "avatar": "Custom Avatar",
            "logger": "Consistent Logger",
            "theme": "Aqua Pulse Theme",
            "champ": "Power Champ"
        }

        icon = badge_icons.get(badge_id, "🏅")
        title = badge_names.get(badge_id, badge_id.replace("_", " ").title())

        return dbc.Card([
            dbc.CardHeader("🏅 Your Badges", className="dashboard_badge-header"),
            dbc.CardBody([
                html.Div(icon, className="badge-icon"),
                html.H5(title, className="badge-title"),
                html.P(f"Claimed on {date}", className="dashboard_badge-date")
            ])
        ], className="dashboard_badge-card")

    #Callback: Rotating Right Side Metrics (Health Summary) 
    @dash_app.callback(
        Output('rotating-right-metric', 'children'),
        [
            Input('username-store', 'data'),
            Input('right-metric-interval', 'n_intervals'),
            Input('prev-metric-btn', 'n_clicks'),
            Input('next-metric-btn', 'n_clicks')
        ],
        prevent_initial_call=True
    )
    def update_right_metric(username_data, n_intervals, prev_clicks, next_clicks):
        """Rotate between grouped health metric summaries."""
        username = username_data.get('username') if username_data else None
        user_health = fetch_user_data(username) or {}

        categories = [
            "exercise", "diet", "hydration", "heart_health", "body_metrics"
        ]
        total_categories = len(categories)

        prev_clicks = prev_clicks or 0
        next_clicks = next_clicks or 0
        current_index = (n_intervals + next_clicks - prev_clicks) % total_categories
        category = categories[current_index]

        metric_data = {
            "exercise": ("LATEST EXERCISE SUMMARY", [
                ("Steps:", f"{user_health.get('latest_steps_taken', 'N/A')}"),
                ("Active Minutes:", f"{user_health.get('latest_active_minutes', 'N/A')} min"),
                ("Calories Burned:", f"{user_health.get('latest_calories_burned', 'N/A')} kcal"),
                ("Distance Walked:", f"{user_health.get('latest_distance_walked', 'N/A')} km"),
                ("Workout Sessions:", f"{user_health.get('latest_workout_sessions', 'N/A')}"),
            ]),
            "diet": ("LATEST DIET SUMMARY", [
                ("Calories:", f"{user_health.get('latest_calories_consumed', 'N/A')} kcal"),
                ("Protein:", f"{user_health.get('latest_protein_intake', 'N/A')} g"),
                ("Carbs:", f"{user_health.get('latest_carbs_intake', 'N/A')} g"),
                ("Fats:", f"{user_health.get('latest_fats_intake', 'N/A')} g"),
                ("Fiber Intake:", f"{user_health.get('latest_fiber_intake', 'N/A')} g"),
            ]),
            "hydration": ("LATEST HYDRATION STATUS", [
                ("Water Intake:", f"{user_health.get('latest_water_intake', 'N/A')} L")
            ]),
            "heart_health": ("LATEST HEART HEALTH", [
                ("Resting Heart Rate:", f"{user_health.get('latest_heart_rate', 'N/A')} bpm"),
            ]),
            "body_metrics": ("LATEST BODY METRICS", [
                ("Weight:", f"{user_health.get('latest_weight', 'N/A')} kg"),
                ("Height:", f"{user_health.get('latest_height', 'N/A')} cm"),
                ("BMI:", f"{user_health.get('latest_bmi', 'N/A')}"),
            ])
        }

        title, metrics = metric_data.get(category, ("UNKNOWN CATEGORY", []))

        return html.Div([
            html.H5(title, className="metric-title"),
            html.Div([
                html.Div([
                    html.Span(label, className="metric-label"),
                    html.Span(value, className="metric-value")
                ], className="right-metric-row")
                for label, value in metrics
            ]),
            html.Div([
                html.Button("◀", id="prev-metric-btn", className="metric-btn"),
                html.Button("▶", id="next-metric-btn", className="metric-btn")
            ], className="metric-navigation")
        ])
        
    @dash_app.callback(
    Output("active-category-store", "data"),
    [
        Input("legend-medical", "n_clicks"),
        Input("legend-nutrition", "n_clicks"),
        Input("legend-activity", "n_clicks"),
        Input("legend-body", "n_clicks"),
        Input("metric-time-filter", "value")  
    ],
    State("active-category-store", "data"),
    prevent_initial_call=True
)
    def set_or_reset_category(med, nut, act, body, time_filter, current):
        ctx = dash.callback_context

        if not ctx.triggered:
            return current

        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if triggered_id == "metric-time-filter":
            return "all"  

        #handle legend buttons
        mapping = {
            "legend-medical": "medical",
            "legend-nutrition": "nutrition",
            "legend-activity": "activity",
            "legend-body": "body"
        }

        selected = mapping.get(triggered_id)

        return "all" if selected == current else selected

def get_metric_category(metric_name):
    for category, metrics in METRIC_CATEGORIES.items():
        if metric_name in metrics:
            return category
    return "default"


