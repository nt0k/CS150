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
                    "First, let's look at the overall situation in "
                    "two of the largest homeless population centers in the US: LA and NY City County."
                )
            ),

            drc.Card(
                id="main card",
                children=[
                    dcc.Graph(id="comparison_graph1", figure=figures.comparison_visual1()),
                ]
            ),
            html.P(id="intergraph_text1", className="m-2",
                   children="2023 and 2024 saw dramatic increases in the homeless population for NY "
                            "City County due to a major influx of Asylum seekers. LA County has had consistent "
                            "increases over the last decade. In total, LA County increased 112% and NY City County "
                            "increase 107% per capita from 2014 to 2024, whereas the U.S. as a whole increased "
                            "25%. Homelessness has gotten significantly worse, but NY city county and LA county have worsened four "
                            "times more than the overall nation. So what strategy have these two counties employed to care "
                            "for their homeless populations?"),
            html.H4("Housing First Approach", id="section_title2", className="m-2"),
            html.P(
                id="text3",
                className="m-2",
                children=(
                    "LA and NY both have a Housing First approach, which focuses on providing permanent housing without "
                    "preconditions like sobriety or treatment. LA has been criticized for its inefficiency in building "
                    "homes and shelters. A 2022 Los Angeles City Controller ",
                    html.A("audit",
                           href="https://ktla.com/news/los-angeles-is-spending-up-to-837000-to-house-a-single-homeless-person/",
                           target="_blank"),
                    " found that 14% of the planned supportive housing units were projected to cost more than $700,000 each, "
                    "with some developments reaching as high as $837,000 per unit. "
                    "In contrast, New York focuses more on providing temporary shelters. This is prioritized and legal enforced through "
                    "its right to shelter legal mandate."
                )
            ),
            drc.Card(
                id="graphs2",
                children=[
                    dcc.Graph(id="shelter_comparison_graph",
                              figure=figures.shelter_comparison("Total Year-Round Beds (ES, TH, SH)")),
                    drc.NamedDropdown(id="housing_segment_select", name="Select Shelter Segment",
                                      options={"Total Year-Round Beds (PSH)": "Permanent Supportive Housing",
                                               "Total Year-Round Beds (OPH)": "Other Permanent Housing",
                                               "Total Year-Round Beds (RRH)": "Year Round Rapid Rehousing",
                                               "Total Year-Round Beds (ES, TH, SH)": "Emergency Shelter, Transitional, Safe Haven Beds"},
                                      value="Total Year-Round Beds (PSH)"),
                    html.H4(id="definitions_title", className="m-2", children="Definitions of Shelter Types"),
                    html.Ul([
                        html.Li([
                            html.B("Permanent Supportive Housing (PSH): "),
                            "Long-term housing with ongoing supportive services to help people with disabilities, chronic health issues, or other challenges maintain housing stability."
                        ]),
                        html.Li([
                            html.B("Other Permanent Housing (OPH): "),
                            "Long-term housing options not designated as PSH but still provide stability without a time limit (e.g., subsidized housing, housing vouchers)."
                        ]),
                        html.Li([
                            html.B("Year Round Rapid Rehousing (RRH): "),
                            "Assistance to quickly move people experiencing homelessness into permanent housing through financial aid and short-term support services."
                        ]),
                        html.Li([
                            html.B("Emergency Shelter, Transitional, Safe Haven Beds (ES, TH, SH): "),
                            "Temporary, immediate shelter (ES); short-term housing with supportive services focused on moving to permanent housing (TH); and low-barrier, 24/7 shelter for individuals who are often unsheltered and have severe needs (SH)."
                        ])
                    ]),
                    html.Hr(),
                    dcc.Graph(id="stacked_bar1", figure=figures.stack_bargraph1()),
                ]
            ),
            html.H4("Significant Impact of Shelters", id="section_title3", className="m-2"),
            html.P(
                id="text5",
                className="m-2",
                children=(
                    "Having more shelters leads to several positive impacts including increased safety, better access to ",
                    "basic necessities, and reduced strain on emergency services. Half of homeless "
                    "deaths in LA are from drug overdose, traffic accidents, and murder. These deaths can be mitigated in a "
                    "sheltered environment."
                )
            ),
            drc.Card(
                id="graphs3",
                children=[
                    dcc.Graph(id="death_graph", figure=figures.death_graph()),
                    html.Hr(),
                    dcc.Graph(id="mortality_projection"),
                    html.Div(id="disclaimer", style={"marginLeft": "20px", "fontSize": "12px", "color": "gray"},
                             children="Note: This model assumes that the counties will behave similarly and is meant to be an estimate"),
                    html.Div(id="output_metrics", style={"margin": 10, "fontSize": "22px", "textAlign": "center"}),
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
            html.P(
                id="conclusionText",
                className="m-2",
                children=[
                    "The bottom line is, LA County needs to invest heavily in more shelters to get people off the street "
                    "and into safer environments. Getting people off the streets and mandating treatment will save many "
                    "lives, as we have already seen in New York. Scan the QR Code below to let City Controller Kenneth Mejia "
                    "know that you want more funding to be used to build more shelters.",
                    html.Br(),
                ],
            ),
            html.Div(
                "Scan NOW to send a populated email.",
                style={"fontWeight": "bold", "fontSize": "24px", "textAlign": "center", "margin": "3px"},
            ),
            html.Div(
                children=html.Img(src="/assets/qrcode.png", style={"width": "70%", "marginBottom": "2px"}),
                style={"display": "flex", "justifyContent": "center", "alignItems": "center"}
            ),
            html.Div(
                "Or manually send an email to: "
                "controller.mejia@lacity.org",
                style={"fontWeight": "bold", "fontSize": "24px", "textAlign": "center", "margin": "3px"},
            )
        ], width=8)
    ], justify="center"),
    html.Footer(
        children=[
            "© 2025 Nathan Kirk | Westmont College | ",
            html.A(
                "Sources",
                href="https://github.com/nt0k/CS150/blob/main/HomelessDataVisualization/README.md",
                target="_blank"
            )
        ],
        style={
            "textAlign": "center",
            "padding": "20px",
            "marginTop": "40px",
            "fontSize": "14px",
            "color": "#666",
            "borderTop": "1px solid #ccc"
        }
    )
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
