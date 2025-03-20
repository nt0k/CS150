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
    external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME],
)

COLORS = {
    "cash": "#3cb521",
    "bonds": "#fd7e14",
    "stocks": "#446e9b",
    "inflation": "#cd0200",
    "background": "whitesmoke",
}

"""
==========================================================================
Figures
"""


def make_tree_map(slider_input, title):
    fig = px.treemap(
        names=["Cash", "Bonds", "Stocks"],
        values=slider_input,
        parents=["", "", ""],
        color=["Cash", "Bonds", "Stocks"],
        color_discrete_map={
            "Cash": COLORS["cash"],
            "Bonds": COLORS["bonds"],
            "Stocks": COLORS["stocks"]
        }
    )
    fig.update_layout(
        title_text=title,
        title_x=0.5,
        margin=dict(b=25, t=75, l=35, r=25),
        height=325,
        paper_bgcolor=COLORS["background"],
    )
    return fig


def make_line_chart(dff):
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
        yaxis= dict(range=[0, None], tickprefix="$", fixedrange=True),
        xaxis=dict(title="Year", fixedrange=True, dtick=dtick),
    )
    return fig


"""
==========================================================================
Make Tabs
"""

# =======Play tab components

asset_allocation_card = dbc.Card(asset_allocation_text, className="mt-2")

slider_card = dbc.Card(
    [
        html.H4("First set cash allocation %:", className="card-title"),
        dcc.Slider(
            id="cash",
            marks={i: f"{i}%" for i in range(0, 101, 10)},
            min=0,
            max=100,
            step=5,
            value=10,
            included=False,
        ),
        html.H4(
            "Then set stock allocation % ",
            className="card-title mt-3",
        ),
        dcc.Slider(
            id="stock_bond",
            marks={i: f"{i}%" for i in range(0, 91, 10)},
            min=0,
            max=90,
            step=5,
            value=50,
            included=False,
        ),
        html.Div(
            [
                html.H4("Bond allocation: ", style={'display': 'inline-block', 'margin-right': '5px'}),
                html.H4(id="bond_amount", children="", style={'display': 'inline-block'})
            ],
            className="card-title mt-3"
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
            [asset_allocation_text, slider_card],
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
                        dcc.Graph(id="income_graph", figure = make_line_chart(df1), className="mb-2"),
                        dcc.Graph(id="returns_chart", className="pb-4"),
                        html.Hr(),
                        html.H6(datasource_text, className="my-2"),
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


if __name__ == "__main__":
    app.run_server(debug=True)
