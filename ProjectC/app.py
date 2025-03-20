# -*- coding: utf-8 -*-
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from dataProcessing import *
from markdownParts import *

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.YETI, dbc.icons.FONT_AWESOME],
)

COLORS = {
    "cash": "#008cba",
    "bonds": "#fd7e14",
    "stocks": "#446e9b",
    "inflation": "#cd0200",
    "background": "whitesmoke",
}

"""
==========================================================================
Figures
"""


def make_line_chart(dff):
    if "Year" not in dff.columns:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=dff["Date"],
                y=dff.iloc[:, 1],
                marker_color=COLORS["cash"],
            )
        )
        fig.update_layout(
            title=f"{dff.columns[1]}",
            template="none",
            height=400,
            margin=dict(l=40, r=10, t=60, b=55),
            yaxis=dict(range=[0, None], tickprefix="$", fixedrange=True),
            xaxis=dict(title="Year", fixedrange=True),
        )
        return fig
    else:
        start = dff.loc[1, "Year"]
        yrs = dff["Year"].size - 1
        dtick = 1 if yrs < 16 else 2 if yrs in range(16, 30) else 5

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=dff["Year"],
                y=dff.iloc[:, 1],
                marker_color=COLORS["cash"],
            )
        )
        fig.update_layout(
            title=f"{dff.columns[1]} in Idaho over the last {yrs} years",
            template="none",
            height=400,
            margin=dict(l=40, r=10, t=60, b=55),
            yaxis=dict(range=[0, None], tickprefix="$", fixedrange=True),
            xaxis=dict(title="Year", fixedrange=True, dtick=dtick),
        )
        return fig


"""
==========================================================================
Make Tabs
"""

# =======Play tab components

dataframes = {
    "Natural Gas Prices": df2,
    "Minimum Wage": df3,
    "Median Home Price": df4,
    "Energy Cost": df5,
    "Ground Beef Price": df6,
    "Boise State University Cost": df7,
}

slider_card = dbc.Card(
    [
        html.H4("Select Which Segment to Examine", className="card-title"),
        dcc.Dropdown(
            id='segment_dropdown',
            options=[{"label": label, "value": label} for label in dataframes.keys()],
            value="Median Home Price",  # Set default value
            className="mb-4",
        ),
        dbc.Button("Use Prior Setting", id="history_button", color="primary", className="me-2", n_clicks=0,
                   disabled=True),
    ],
    body=True,
    className="mt-4",
)

# ======= InputGroup components

start_amount = dbc.InputGroup(
    [
        dbc.InputGroupText("Start Amount $"),
        dbc.Input(
            id="starting_amount",
            placeholder="Min $10",
            type="number",
            min=10,
            value=10000,
        ),
    ],
    className="mb-3",
)

# =====  Results Tab components


# ========= Learn Tab  Components
learn_card = dbc.Card(
    [
        dbc.CardHeader("An Introduction to this project"),
        dbc.CardBody(learn_text),
    ],
    className="mt-4",
)

# ========= Past Settings Tab  Components
past_setting_card = dbc.Card(
    [
        dbc.CardHeader("Previous Settings"),
        dbc.CardBody(past_settings_table),
    ],
    className="mt-4",
)

# ========= Build tabs
tabs = dbc.Tabs(
    [
        dbc.Tab(learn_card, tab_id="tab1", label="Learn"),
        dbc.Tab(
            [slider_card],
            tab_id="tab-2",
            label="Play",
            className="pb-4",
        ),
        dbc.Tab(past_setting_card, tab_id="tab-4", label="Previous Settings"),
    ],
    id="tabs",
    active_tab="tab-2",
    className="mt-2",
)

"""
===========================================================================
Main Layout
"""

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.H2(
                        "Cost of Living in Idaho",
                        className="text-center bg-primary text-white p-2",
                    ),
                    html.H5(
                        "Created by Nathan Kirk for CS150 taught by Mike Ryu",
                        style={"textAlign": "center"},
                    ),
                ]
            )
        ),
        dbc.Row(
            [
                dbc.Col(tabs, width=12, lg=5, className="mt-4 border"),
                dbc.Col(
                    [
                        dcc.Graph(id="income_graph", figure=make_line_chart(df1), className="mb-2"),
                        html.P(percent_calculation(df1, None, "Idaho Median Income")),
                        html.Hr(),
                        dcc.Graph(id="comparison_graph", className="pb-4"),
                        html.P(id="comparison_text"),
                        html.Hr(),
                    ],
                    width=12,
                    lg=7,
                    className="pt-4",
                ),
            ],
            className="ms-1",
        ),
        dbc.Row(dbc.Col(footer)),
    ],
    fluid=True,
)

"""
==========================================================================
Callbacks
"""


@app.callback(Output("history_button", "disabled"),
              Input("past_settings", "data"),
              prevent_initial_call=True
              )
def button_check(past_settings):
    return len(past_settings) <= 1


@app.callback(Output("comparison_graph", "figure"),
              Output("comparison_text", "children"),
              Input("segment_dropdown", "value"),
              )
def update_comparison_graph(selected_val):
    print(selected_val)
    if selected_val == "Median Home Price" or selected_val == "Ground Beef Price":
        return make_line_chart(dataframes[selected_val]), percent_calculation(dataframes[selected_val], "Date",
                                                                              dataframes[selected_val].columns[1])
    else:
        return make_line_chart(dataframes[selected_val]), percent_calculation(dataframes[selected_val], None,
                                                                              dataframes[selected_val].columns[1])


if __name__ == "__main__":
    app.run_server(debug=True)
