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
                html.H4(id="description-title", children="Description", className="m-2"),
                html.P(id="description-text", className="m-2",
                       children="Description Text"),
            ])
        ]), width=6),

        dbc.Col(html.Div(id="right-column", children=[
            drc.Card(id="second-card", children=[
                dcc.Graph(id="first_graph", figure={}),
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
    line1 = go.Scatter(
        x=df["Date"],
        y=df["Encounter Count"],
        name="Apprehensions at the Southern Border"
    )

    layout = go.Layout(
        title="Apprehensions at the Southern Border",
    )

    fig = go.Figure(line1, layout=layout)

    return fig


if __name__ == '__main__':
    app.run(debug=True)
