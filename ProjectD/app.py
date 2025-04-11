import dash
from dash import *
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
from ProjectD import ingestion
from ProjectD import reusable as drc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])

app.layout = html.Div(className="app-container", children=[
    html.H1(style={"textAlign": "center"}, className="title mb-3 mt-2", children='Apprehensions at the Souther Border'),
    html.Div(style={"textAlign": "center"}, className="subtitle mb-3",
             children='By Nathan Kirk for CS150 | nkirk@westmont.edu'),

    dbc.Row([
        dbc.Col(html.Div(id="left-column", children=[
            drc.Card(id="first-card", children=[
                html.H3(id="description_title", children="Description", className="m-2"),
                html.P(id="description_text", className="m-2",
                       children="Title 8 of the U.S. Code governs immigration and nationality laws. When U.S. Border "
                                "Patrol (USBP) reports an “Apprehension” under Title 8, it means that someone was "
                                "physically stopped and taken into custody for attempting to enter the U.S. unlawfully "
                                "between ports of entry."),
                dcc.Graph(id="left_graph", figure={}, style={"height": "600px", "width": "100%"}),
            ])
        ]), width=6),

        dbc.Col(html.Div(id="right-column", children=[
            drc.Card(id="second-card", children=[
                dcc.Graph(id="first_graph", figure={}, style={"height": "600px", "width": "100%"}),
            ])
        ]), width=6),
    ])
])


@app.callback(
    Output("first_graph", "figure"),
    Input("first_graph", "figure")
)
def make_graph(fig):
    df = ingestion.fetch_and_clean_data()
    # Clean up Encounter Count values and convert to integers
    df["Encounter Count"] = df["Encounter Count"].astype(str).str.replace(",", "").astype(int)
    df["Date"] = pd.to_datetime(df["Date"])

    # Create the line graph using Scatter
    trace = go.Scatter(
        x=df["Date"],
        y=df["Encounter Count"],
        mode="lines",
        name="Apprehensions at the Southern Border",
        line=dict(color="#000000", width=5)
    )

    additional_line = go.Scatter(
        x=[df["Date"].min(), "2025-06-01"],
        y=[8000, 8000],  # Constant y value for the whole line
        mode="lines",
        name="Normal Bottom",
        line=dict(color="red", dash="dash")
    )

    layout = go.Layout(
        title="Apprehensions at the Southern Border Return to Normal Levels",
        xaxis=dict(
            title="Year",
            range=['2015-01-01', '2025-06-01'],
            showline=True,  # Show axis line
            linecolor="lightgray",  # Color of the axis line
            linewidth=1,
        ),
        yaxis=dict(
            title="Apprehensions",
            range=[0, 275000],
            gridcolor="lightgray",
            showgrid=True,
            showline=True,  # Show axis line
            linecolor="lightgray",  # Color of the axis line
            linewidth=1,
        ),
        hovermode="closest",
        plot_bgcolor="#FFFFFF",
        legend=dict(
            orientation="h",  # Horizontal legend
            x=0.5,  # Center it horizontally
            y=-0.2,  # Move it below the x-axis (negative y)
            xanchor="center",  # Anchor x at the center of the legend
            yanchor="top"  # Anchor y at the top of the legend box
        ),
        annotations=[
            dict(
                x="2017-04-01",  # x position (a date or number depending on x-axis)
                y=15000,  # y position
                xref="x",
                yref="y",
                text="Similar level hit several times before"
                     "<br>in Trump's and Biden's terms",
                showarrow=True,
                arrowhead=2,
                ax=15,
                ay=-220,
                font=dict(size=12, color="black"),
                bgcolor="white",
                bordercolor="black",
                borderwidth=1
            )
        ],
    )

    fig = go.Figure(data=[trace, additional_line], layout=layout)
    return fig


@app.callback(
    Output("left_graph", "figure"),
    Input("left_graph", "figure")
)
def make_graph(fig):
    df = ingestion.fetch_and_clean_data()
    # Clean up Encounter Count values and convert to integers
    df["Encounter Count"] = df["Encounter Count"].astype(str).str.replace(",", "").astype(int)
    df["Date"] = pd.to_datetime(df["Date"])

    # Create the line graph using Scatter
    trace = go.Scatter(
        x=df["Date"],
        y=df["Encounter Count"],
        mode="lines",
        name="Apprehensions at the Southern Border",
        line=dict(color="#000000", width=5)
    )

    additional_line = go.Scatter(
        x=["2023-12-01", "2023-12-01"],
        y=[0, 300000],  # Constant y value for the whole line
        mode="lines",
        name="Policy Takes Effect",
        line=dict(color="red", dash="dash")
    )

    layout = go.Layout(
        title="Trump Inherits Biden's Policy Progress",
        xaxis=dict(
            title="Year",
            range=['2023-06-01', '2025-06-01'],
            showline=True,  # Show axis line
            linecolor="lightgray",  # Color of the axis line
            linewidth=1,
        ),
        yaxis=dict(
            title="Apprehensions",
            range=[0, 300000],
            gridcolor="lightgray",
            showgrid=True,
            showline=True,  # Show axis line
            linecolor="lightgray",  # Color of the axis line
            linewidth=1,
        ),
        hovermode="closest",
        plot_bgcolor="#FFFFFF",
        legend=dict(
            orientation="h",  # Horizontal legend
            x=0.5,  # Center it horizontally
            y=-0.2,  # Move it below the x-axis (negative y)
            xanchor="center",  # Anchor x at the center of the legend
            yanchor="top"  # Anchor y at the top of the legend box
        ),
        annotations=[
            dict(
                x="2023-12-01",  # x position (a date or number depending on x-axis)
                y=150000,  # y position
                xref="x",
                yref="y",
                text="Biden's policy shift"
                     "<br>takes effect",
                showarrow=True,
                arrowhead=2,
                ax=250,
                ay=-50,
                font=dict(size=12, color="black"),
                bgcolor="white",
                bordercolor="black",
                borderwidth=1
            ),
            dict(
                x="2025-01-01",  # x position (a date or number depending on x-axis)
                y=32000,  # y position
                xref="x",
                yref="y",
                text="Trump takes office",
                showarrow=True,
                arrowhead=2,
                ax=0,
                ay=-100,
                font=dict(size=12, color="black"),
                bgcolor="white",
                bordercolor="black",
                borderwidth=1
            )
        ],
    )

    fig = go.Figure(data=[trace, additional_line], layout=layout)
    return fig


if __name__ == '__main__':
    app.run(debug=True)
