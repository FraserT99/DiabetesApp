#Importing necessary Dash components and Bootstrap for layout structure
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html  #Essential Dash components for layout
from components.sidebar import create_sidebar  #Custom sidebar component for navigation

def profile_page(username):
    
    return dbc.Container(fluid=True, children=[

        #State stores to manage active tab and refresh flag
        dcc.Store(id="active-profile-tab", data="overview"),  #Tracks active profile tab (default to "overview")
        dcc.Store(id="refresh-flag"),  #Refresh flag for updating dynamic content

        #Layout row: Sidebar + Main Content
        dbc.Row([

            #Left Sidebar (Navigation)
            dbc.Col(create_sidebar(), width=2),  #Custom sidebar with 2 columns width

            #Right Content Area
            dbc.Col([  #Main content section occupies 10 columns of width
                html.Div(className="profile-content-wrapper", children=[

                    #Profile Topbar (inside the content wrapper)
                    html.Div(className="profile-topbar", children=[

                        #Title of the profile menu
                        html.Div("Profile Menu", className="profile-topbar-title"),

                        #Tabs for different profile sections
                        html.Div(className="profile-topbar-tabs", children=[

                            #Each button represents a section (Overview, Edit Profile, Privacy, etc.)
                            html.Button("Overview", id="profile-tab-overview", className="profile-tab"),
                            html.Button("Edit Profile", id="profile-tab-edit", className="profile-tab"),
                            html.Button("Privacy Settings", id="profile-tab-privacy", className="profile-tab"),
                        ])
                    ]),

                    #Dynamic content that updates based on the active tab
                    html.Div(id="profile-content")  #Placeholder for content that will be updated dynamically

                ])
            ], width=10)  #Right section of the layout takes 10 columns of width

        ])
    ])  #End of the container
