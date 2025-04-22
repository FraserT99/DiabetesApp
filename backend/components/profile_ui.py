import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from components.sidebar import create_sidebar

def profile_page(username):
    
    return dbc.Container(fluid=True, children=[


        dcc.Store(id="active-profile-tab", data="overview"),
        dcc.Store(id="refresh-flag"),


        dbc.Row([


            dbc.Col(create_sidebar(), width=2),


            dbc.Col([
                html.Div(className="profile-content-wrapper", children=[


                    html.Div(className="profile-topbar", children=[


                        html.Div("Profile Menu", className="profile-topbar-title"),


                        html.Div(className="profile-topbar-tabs", children=[


                            html.Button("Overview", id="profile-tab-overview", className="profile-tab"),
                            html.Button("Edit Profile", id="profile-tab-edit", className="profile-tab"),
                            html.Button("Privacy Settings", id="profile-tab-privacy", className="profile-tab"),
                        ])
                    ]),


                    html.Div(id="profile-content")

                ])
            ], width=10)

        ])
    ])
