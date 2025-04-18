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
    html.H1(
        children='A Homeless Policy Case Study: NY vs LA',
        style={"textAlign": "center"},
        className="title mb-3 mt-2"
    ),

    html.Div(
        children='By Nathan Kirk for CS150 | nkirk@westmont.edu',
        style={"textAlign": "center"},
        className="subtitle mb-3"
    ),

    dbc.Row([
        dbc.Col([
            html.Img(src="/assets/cover_image.jpg", style={"width": "100%", "margin-bottom": "10px"}),
            html.H4("A Complicated Issue", id="section_title1", className="m-2"),

            html.P(
                id="text1",
                className="m-2",
                children=(
                    "The issue of homelessness is one that plagues our nation and our "
                    "state of California more severely. Billions of dollars are spent every year "
                    "to try to help people get off the streets, but despite the actions of so many "
                    "advocates and so much funding, the problem has gotten worse. "
                    "First let's look at the overall situation in "
                    "two of the largest homeless population centers in the US: LA and NY City County."
                )
            ),

            drc.Card(
                id="main card",
                children=[
                    dcc.Graph(id="comparison_graph1", figure=figures.comparison_visual1()),
                    html.P(id="intergraph_text1", className="m-2",
                           children="The last two years saw dramatic increases in the homeless population for NY "
                                    "City County whereas LA County has had consistent growth over the last decade. "
                                    "LA County increased 112% and NY City County "
                                    "increase 107% per capita from 2014 to 2024."),
                    dcc.Graph(id="usa_capita_graph", figure=figures.us_percapita_homeless()),
                    html.P(
                        id="text2",
                        className="m-2",
                        children=(
                            "The issue of homelessness has gotten significantly worse, but NY city county and LA county have "
                            "worsened four "
                            "times more than the overall nation. "
                        )
                    )
                ]
            ),
            drc.Card(
                id="graphs2",
                children=[
                    dcc.Graph(id="shelter_comparison_graph",
                              figure=figures.shelter_comparison("Total Year-Round Beds (ES, TH, SH)")),
                    drc.NamedDropdown(id="housing_segment_select", name="Select Housing Segment",
                                      options={"Total Year-Round Beds (OPH)": "Other Permanent Housing",
                                               "Total Year-Round Beds (PSH)": "Permanent Supportive Housing",
                                               "Total Year-Round Beds (RRH)": "Year Round Rapid Rehousing",
                                               "Total Year-Round Beds (ES, TH, SH)": "Emergency Shelter, Transitional, Safe Haven Beds"},
                                      value="Total Year-Round Beds (ES, TH, SH)"),
                    html.Hr(),
                    dcc.Graph(id="stacked_bar1", figure=figures.stack_bargraph1()),
                    html.P(
                        id="text2",
                        className="m-2",
                        children=(
                            "NY County has twice as many homeless people as LA County, yet it is still "
                            "able to shelter nearly all of them. LA shelters only a third of its homeless "
                            "population. "
                        )
                    )
                ]
            ),

        ], width=8)
    ], justify="center"),
])


@app.callback(Output("shelter_comparison_graph", "figure"),
              Input("housing_segment_select", "value"))
def update_segment_graph(segment):
    return figures.shelter_comparison(segment)


if __name__ == '__main__':
    app.run(debug=True)
