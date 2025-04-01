import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
from Lab5 import *
from Lab5 import reusable as drc
from Lab5 import figures as figgy
from Lab5 import utilities

app = dash.Dash(__name__)

app.layout = html.Div(className="app-container", children=[
    html.H1(className="title", children='Credit Card Approval SVM Prediction'),
    html.Div(className="subtitle", children='By Nathan Kirk for CS150'),

    html.Div(id="left-column", className="column", children=[
        drc.Card(id="first-card", children=[
            drc.NamedSlider("Test Size", id="test_size_slider", min=0.1, max=0.9, step=0.1, value=0.2),
            drc.NamedSlider("Second Parameter"),
            drc.NamedSlider("Third Parameter"),
        ])
    ]),

    html.Div(id="right-column", className="column", children=[
        drc.Card(id="second-card", children=[
            figgy.serve_prediction_plot(),
            figgy.serve_prediction_plot(),
            figgy.serve_prediction_plot(),
        ])
    ])
])


@app.callback(
    dash.Output('slider-1-output', 'children'),
    dash.Input('slider-1', 'value'))
def update_slider_1(value):
    return f'Slider 1 Value: {value}'


@app.callback(
    dash.Output('slider-2-output', 'children'),
    dash.Input('slider-2', 'value'))
def update_slider_2(value):
    return f'Slider 2 Value: {value}'


if __name__ == '__main__':
    app.run(debug=True)
