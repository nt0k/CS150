# -*- coding: utf-8 -*-
import dash_bootstrap_components
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context, dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import reusable as drc
import figures

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])

app.layout = html.Div(className="app-container", children=[
    html.H1(style={"textAlign": "center"}, className="title mb-3 mt-2", children='Homeless Data Visualization'),
    html.Div(style={"textAlign": "center"}, className="subtitle mb-3",
             children='By Nathan Kirk for CS150 | nkirk@westmont.edu'),

    dbc.Row([
        html.Div(
            dcc.Graph(id="comparison_graph1", figure=figures.comparison_visual1())
        )
    ]),
    dbc.Row([
        dbc.Col(html.Div(id="left-column", children=[
            drc.Card(id="first-card", children=[
                dcc.Graph(id="ca_graph", figure=figures.ca_visual_1()),
            ])
        ]), width=6),

        dbc.Col(html.Div(id="right-column", children=[
            drc.Card(id="second-card", children=[
                dcc.Graph(id="ny_graph", figure=figures.ny_visual_1()),
            ])
        ]), width=6),
    ])
])

if __name__ == '__main__':
    app.run(debug=True)
