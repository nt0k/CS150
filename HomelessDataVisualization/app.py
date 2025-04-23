# -*- coding: utf-8 -*-
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context, dash
import dash_bootstrap_components as dbc
import reusable as drc
import figures

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])

app.layout = html.Div(className="app-container", children=[
    html.H1(
        children='A Tale of Two Cities',
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
            html.H4("Background", id="section_title1", className="m-2"),
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
                                    "City County due to a major influx of Asylum seekers. LA County has had consistent "
                                    "increases over the last decade. LA County increased 112% and NY City County "
                                    "increase 107% per capita from 2014 to 2024."),
                    html.Hr(),
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
            html.H4("Housing First Approach", id="section_title2", className="m-2"),
            html.P(
                id="text3",
                className="m-2",
                children=(
                    "LA and NY both have a Housing First approach, which focuses on providing permanent housing without "
                    "preconditions like sobriety or treatment. LA has been criticized for its inefficiency in building "
                    "homes and shelters. A city ",
                    html.A("audit",
                           href="https://ktla.com/news/los-angeles-is-spending-up-to-837000-to-house-a-single-homeless-person/",
                           target="_blank"),
                    " in 2022 revealed that 14% of the units built exceeded $700,000 each."
                    "In contrast, New York has a right to shelter legal mandate that requires the city to have shelters "
                    "for all who need them."
                )
            ),
            drc.Card(
                id="graphs2",
                children=[
                    dcc.Graph(id="shelter_comparison_graph",
                              figure=figures.shelter_comparison("Total Year-Round Beds (ES, TH, SH)")),
                    drc.NamedDropdown(id="housing_segment_select", name="Select Shelter Segment",
                                      options={"Total Year-Round Beds (OPH)": "Other Permanent Housing",
                                               "Total Year-Round Beds (PSH)": "Permanent Supportive Housing",
                                               "Total Year-Round Beds (RRH)": "Year Round Rapid Rehousing",
                                               "Total Year-Round Beds (ES, TH, SH)": "Emergency Shelter, Transitional, Safe Haven Beds"},
                                      value="Total Year-Round Beds (ES, TH, SH)"),
                    html.Hr(),
                    dcc.Graph(id="stacked_bar1", figure=figures.stack_bargraph1()),
                ]
            ),
            html.H4("Significant Impact of Shelters", id="section_title3", className="m-2"),
            drc.Card(
                id="graphs3",
                children=[
                    dcc.Graph(figure=figures.death_graph()),
                    html.P(
                        id="text5",
                        className="m-2",
                        children=(
                            "Having more shelters leads to several positive impacts including increased safety, better access to ",
                            "basic necessities, and reduced strain on emergency services. The bottom line is, LA County needs to "
                            "invest heavily in more shelters to get people off the street and into safer environments. Half of homeless "
                            "deaths in LA are from drug overdose, traffic accidents, and murder. Getting people off the streets and "
                            "mandating treatment will save many lives, as we have already seen in New York. "
                        )
                    ),
                    dcc.Graph(id="mortality_projection"),
                    html.P(id="disclaimer", style={"margin": 2, "fontSize": "12px", "color": "gray"},
                           children="Note: This model assumes that the counties will behave similarly and is meant to be an estimate"),
                    html.Div(id="output_metrics", style={"margin": 10, "fontSize": "17px", "textAlign": "center"}),
                    drc.NamedSlider(
                        id="shelter_rate_slider",
                        name="Select Sheltered Percentage",
                        min=40,
                        max=100,
                        step=1,
                        marks={i: f'{i}%' for i in range(40, 101, 10)},
                        value=40
                    ),
                ]),
        ], width=8)
    ], justify="center"),
])


@app.callback(Output("shelter_comparison_graph", "figure"),
              Input("housing_segment_select", "value"))
def update_segment_graph(segment):
    return figures.shelter_comparison(segment)


@app.callback(
    [Output("output_metrics", "children"),
     Output("mortality_projection", "figure")],
    Input("shelter_rate_slider", "value")
)
def update_projection_graph(input_value):
    return figures.projection_graph(input_value)


if __name__ == '__main__':
    app.run(debug=True)
