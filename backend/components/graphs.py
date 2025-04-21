#Importing Plotly Express for creating visualizations
import plotly.express as px

#Importing Dash Core Components for embedding the graph in the Dash app
from dash import dcc

def create_metric_graph(df, metric_label, thresholds):
    
    #Create the line chart using Plotly Express
    fig = px.line(df, x="Date", y="Value", title=None)

    #Add color zones for different thresholds (Normal, Warning, Critical)
    fig.add_hrect(y0=thresholds["normal"][0], y1=thresholds["normal"][1], 
                  fillcolor="rgba(0, 255, 0, 0.15)", opacity=0.4, 
                  layer="below", line=dict(width=1, color="green"))
    
    fig.add_hrect(y0=thresholds["warning"][0], y1=thresholds["warning"][1], 
                  fillcolor="rgba(255, 255, 0, 0.15)", opacity=0.4, 
                  layer="below", line=dict(width=1, color="yellow"))
    
    fig.add_hrect(y0=thresholds["critical"][0], y1=thresholds["critical"][1], 
                  fillcolor="rgba(255, 0, 0, 0.15)", opacity=0.4, 
                  layer="below", line=dict(width=1, color="red"))

    #Customize the appearance of the chart
    fig.update_traces(line=dict(color="black", width=4))  #Set line color and width
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),  #Set chart margins
        plot_bgcolor="white",  #Set plot background color
        paper_bgcolor="white",  #Set paper background color
        xaxis=dict(showgrid=True, gridcolor="lightgray"),  #Customize x-axis grid
        yaxis=dict(showgrid=True, gridcolor="lightgray"),  #Customize y-axis grid
        annotations=[  #Add annotation for the latest value on the chart
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

    #Return the Plotly graph as a Dash component with interaction options
    return dcc.Graph(figure=fig, config={"displayModeBar": True, "scrollZoom": True})
