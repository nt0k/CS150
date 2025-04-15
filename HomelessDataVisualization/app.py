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
    html.H1(style={"textAlign": "center"}, className="title mb-3 mt-2",
            children='A Homeless Policy Case Study: NY vs LA'),
    html.Div(style={"textAlign": "center"}, className="subtitle mb-3",
             children='By Nathan Kirk for CS150 | nkirk@westmont.edu'),

    dbc.Row([
        dbc.Col(
            drc.Card(id="main card", children=[
                html.H4(id= "section_title1", className="m-2", children="A Complicated Issue"),
                html.P(id="text1", className="m-2", children="The issue of homelessness is one that plague's our nation and our"
                                            "state of California more severely. Billions of dollars are spent every year"
                                            "to try to help people get off the streets, but despite the actions of so many"
                                            "advocates and so much funding, the problem has gotten worse here despite"
                                            "improving overall in the nation. First lets look at the overall situation in"
                                            "two of the largest homeless populations centers in the US: LA and NY County."),
                dcc.Graph(id="comparison_graph1", figure=figures.comparison_visual1())
            ]
                     ), width=10
        )
    ], justify="center"),
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
    ]),
])

if __name__ == '__main__':
    app.run(debug=True)
