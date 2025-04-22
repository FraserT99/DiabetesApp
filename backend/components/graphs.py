import plotly.express as px
from dash import dcc

def create_metric_graph(df, metric_label, thresholds):
    
    fig = px.line(df, x="Date", y="Value", title=None)

    fig.add_hrect(y0=thresholds["normal"][0], y1=thresholds["normal"][1], 
                  fillcolor="rgba(0, 255, 0, 0.15)", opacity=0.4, 
                  layer="below", line=dict(width=1, color="green"))
    
    fig.add_hrect(y0=thresholds["warning"][0], y1=thresholds["warning"][1], 
                  fillcolor="rgba(255, 255, 0, 0.15)", opacity=0.4, 
                  layer="below", line=dict(width=1, color="yellow"))
    
    fig.add_hrect(y0=thresholds["critical"][0], y1=thresholds["critical"][1], 
                  fillcolor="rgba(255, 0, 0, 0.15)", opacity=0.4, 
                  layer="below", line=dict(width=1, color="red"))

    fig.update_traces(line=dict(color="black", width=4))  
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),  
        plot_bgcolor="white",  
        paper_bgcolor="white",  
        xaxis=dict(showgrid=True, gridcolor="lightgray"),  
        yaxis=dict(showgrid=True, gridcolor="lightgray"),  
        annotations=[  
            dict(
                x=df["Date"].iloc[-1],
                y=df["Value"].iloc[-1],
                text=f"Latest Value: {df['Value'].iloc[-1]}",
                showarrow=True,
                arrowhead=2,
                ax=0,
                ay=-40
            )
        ]
    )

    return dcc.Graph(figure=fig, config={"displayModeBar": True, "scrollZoom": True})
