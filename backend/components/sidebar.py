from dash import html
import dash_bootstrap_components as dbc

def create_sidebar():
 
    return html.Div([

        html.H4(id="sidebar-title", className="sidebar-title"),


        html.Ul([
            html.Li(dbc.NavLink("Dashboard", href="/dashboard", className="nav-link")),
            html.Li(dbc.NavLink("Log Data", href="/log_data", className="nav-link", id="log-data-link")),
            html.Li(dbc.NavLink("Set Goals", href="/goals", className="nav-link")),
            html.Li(dbc.NavLink("Challenges", href="/challenges", className="nav-link")),
            html.Li(dbc.NavLink("Rewards", href="/rewards", className="nav-link")),
            html.Li(dbc.NavLink("Leaderboard", href="/leaderboard", className="nav-link")),
            html.Li(dbc.NavLink("Profile", href="/profile", className="nav-link"))
        ], className="sidebar-nav"),


        html.Div([
            html.Img(src="/static/uploads/images/logo.png", className="sidebar-logo")
        ], className="sidebar-logo-container")
    ], className="sidebar-container")
