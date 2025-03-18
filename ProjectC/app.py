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
            y=dff["all_cash"],
            name="All Cash",
            marker_color=COLORS["cash"],
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dff["Year"],
            y=dff["all_bonds"],
            name="All Bonds (10yr T.Bonds)",
            marker_color=COLORS["bonds"],
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dff["Year"],
            y=dff["all_stocks"],
            name="All Stocks (S&P500)",
            marker_color=COLORS["stocks"],
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dff["Year"],
            y=dff["Total"],
            name="My Portfolio",
            marker_color="black",
            line=dict(width=6, dash="dot"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dff["Year"],
            y=dff["inflation_only"],
            name="Inflation",
            visible=True,
            marker_color=COLORS["inflation"],
        )
    )
    fig.update_layout(
        title=f"Returns for {yrs} years starting {start}",
        template="none",
        showlegend=True,
        legend=dict(x=0.01, y=0.99),
        height=400,
        margin=dict(l=40, r=10, t=60, b=55),
        yaxis=dict(tickprefix="$", fixedrange=True),
        xaxis=dict(title="Year Ended", fixedrange=True, dtick=dtick),
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

time_period_data = [
    {
        "label": f"2007-2008: Great Financial Crisis to {MAX_YR}",
        "start_yr": 2007,
        "planning_time": MAX_YR - START_YR + 1,
    },
    {
        "label": "1999-2010: The decade including 2000 Dotcom Bubble peak",
        "start_yr": 1999,
        "planning_time": 10,
    },
    {
        "label": "1969-1979:  The 1970s Energy Crisis",
        "start_yr": 1970,
        "planning_time": 10,
    },
    {
        "label": "1929-1948:  The 20 years following the start of the Great Depression",
        "start_yr": 1929,
        "planning_time": 20,
    },
    {
        "label": f"{MIN_YR}-{MAX_YR}",
        "start_yr": "1928",
        "planning_time": MAX_YR - MIN_YR + 1,
    },
]

time_period_card = dbc.Card(
    [
        html.H4(
            "Or select a time period:",
            className="card-title",
        ),
        dbc.RadioItems(
            id="time_period",
            options=[
                {"label": period["label"], "value": i}
                for i, period in enumerate(time_period_data)
            ],
            value=0,
            labelClassName="mb-2",
        ),
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
start_year = dbc.InputGroup(
    [
        dbc.InputGroupText("Start Year"),
        dbc.Input(
            id="start_yr",
            placeholder=f"min {MIN_YR}   max {MAX_YR}",
            type="number",
            min=MIN_YR,
            max=MAX_YR,
            value=START_YR,
        ),
    ],
    className="mb-3",
)
number_of_years = dbc.InputGroup(
    [
        dbc.InputGroupText("Number of Years:"),
        dbc.Input(
            id="planning_time",
            placeholder="# yrs",
            type="number",
            min=1,
            value=MAX_YR - START_YR + 1,
        ),
    ],
    className="mb-3",
)
end_amount = dbc.InputGroup(
    [
        dbc.InputGroupText("Ending Amount"),
        dbc.Input(id="ending_amount", disabled=True, className="text-black"),
    ],
    className="mb-3",
)
rate_of_return = dbc.InputGroup(
    [
        dbc.InputGroupText(
            "Rate of Return(CAGR)",
            id="tooltip_target",
            className="text-decoration-underline",
        ),
        dbc.Input(id="cagr", disabled=True, className="text-black"),
        dbc.Tooltip(cagr_text, target="tooltip_target"),
    ],
    className="mb-3",
)

input_groups = html.Div(
    [start_amount, start_year, number_of_years, end_amount, rate_of_return],
    className="mt-4 p-4",
)

# =====  Results Tab components

results_card = dbc.Card(
    [
        dbc.CardHeader("My Portfolio Returns - Rebalanced Annually"),
        html.Div(total_returns_table),
    ],
    className="mt-4",
)

data_source_card = dbc.Card(
    [
        dbc.CardHeader("Source Data: Annual Total Returns"),
        html.Div(annual_returns_pct_table),
    ],
    className="mt-4",
)

# ========= Learn Tab  Components
learn_card = dbc.Card(
    [
        dbc.CardHeader("An Introduction to Asset Allocation"),
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
            [asset_allocation_text, slider_card, input_groups, time_period_card],
            tab_id="tab-2",
            label="Play",
            className="pb-4",
        ),
        dbc.Tab([results_card, data_source_card], tab_id="tab-3", label="Results"),
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
                        "Asset Allocation Visualizer",
                        className="text-center bg-primary text-white p-2",
                    ),
                    html.H5(
                        "Nathan Kirk, CS150 taught by Mike Ryu",
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
                        dcc.Graph(id="allocation_tree_map", className="mb-2"),
                        dcc.Graph(id="returns_chart", className="pb-4"),
                        html.Hr(),
                        html.Div(id="summary_table"),
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


@app.callback(
    Output("allocation_tree_map", "figure"),
    Output("bond_amount", "children"),
    Input("stock_bond", "value"),
    Input("cash", "value"),
)
def update_tree_map(stocks, cash):
    bonds = 100 - stocks - cash
    slider_input = [cash, bonds, stocks]

    if stocks >= 70:
        investment_style = "Aggressive"
    elif stocks <= 30:
        investment_style = "Conservative"
    else:
        investment_style = "Moderate"
    figure = make_tree_map(slider_input, investment_style + " Asset Allocation")
    return figure, (str(bonds) + "%")


@app.callback(
    Output("stock_bond", "max"),
    Output("stock_bond", "marks"),
    Output("stock_bond", "value"),
    Input("cash", "value"),
    State("stock_bond", "value"),
)
def update_stock_slider(cash, initial_stock_value):
    max_slider = 100 - int(cash)
    stocks = min(max_slider, initial_stock_value)

    # formats the slider scale
    if max_slider > 50:
        marks_slider = {i: f"{i}%" for i in range(0, max_slider + 1, 10)}
    elif max_slider <= 15:
        marks_slider = {i: f"{i}%" for i in range(0, max_slider + 1, 1)}
    else:
        marks_slider = {i: f"{i}%" for i in range(0, max_slider + 1, 5)}
    return max_slider, marks_slider, stocks


@app.callback(
    Output("planning_time", "value"),
    Output("start_yr", "value"),
    Output("time_period", "value"),
    Input("planning_time", "value"),
    Input("start_yr", "value"),
    Input("time_period", "value"),
)
def update_time_period(planning_time, start_yr, period_number):
    """syncs inputs and selected time periods"""
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if input_id == "time_period":
        planning_time = time_period_data[period_number]["planning_time"]
        start_yr = time_period_data[period_number]["start_yr"]

    if input_id in ["planning_time", "start_yr"]:
        period_number = None

    return planning_time, start_yr, period_number


@app.callback(
    Output("total_returns", "data"),
    Output("returns_chart", "figure"),
    Output("summary_table", "children"),
    Output("ending_amount", "value"),
    Output("cagr", "value"),
    Output("past_settings", "data", allow_duplicate=True),
    Input("stock_bond", "value"),
    Input("cash", "value"),
    Input("starting_amount", "value"),
    Input("planning_time", "value"),
    Input("start_yr", "value"),
    State("past_settings", "data"),
    prevent_initial_call=True,
)
def update_totals(stocks, cash, start_bal, planning_time, start_yr, existing_data):
    # set defaults for invalid inputs
    start_bal = 10 if start_bal is None else start_bal
    planning_time = 1 if planning_time is None else planning_time
    start_yr = MIN_YR if start_yr is None else int(start_yr)

    # if button clicked, don't use this and return updated_settings, if not then append new row
    new_row = {
        "cash_allocation": cash,
        "stock_allocation": stocks,
        "bond_allocation": 100 - cash - stocks,
        "start_amount": start_bal,
        "start_year": start_yr,
        "number_of_years": planning_time
    }

    # calculate valid planning time start yr
    max_time = MAX_YR + 1 - start_yr
    planning_time = min(max_time, planning_time)
    if start_yr + planning_time > MAX_YR:
        start_yr = min(df.iloc[-planning_time, 0], MAX_YR)  # 0 is Year column

    # create investment returns dataframe
    dff = backtest(stocks, cash, start_bal, planning_time, start_yr)

    # create data for DataTable
    data = dff.to_dict("records")

    # create the line chart
    fig = make_line_chart(dff)

    summary_table = make_summary_table(dff)

    # format ending balance
    ending_amount = f"${dff['Total'].iloc[-1]:0,.0f}"

    # calcluate cagr
    ending_cagr = cagr(dff["Total"])

    return data, fig, summary_table, ending_amount, ending_cagr, existing_data + [new_row] if existing_data else [
        new_row]


@app.callback(
    Output("stock_bond", "value", allow_duplicate=True),
    Output("cash", "value", allow_duplicate=True),
    Output("starting_amount", "value", allow_duplicate=True),
    Output("planning_time", "value", allow_duplicate=True),
    Output("start_yr", "value", allow_duplicate=True),
    Output("past_settings", "data", allow_duplicate=True),
    Input("history_button", "n_clicks"),
    State("past_settings", "data"),
    prevent_initial_call=True,
)
def push_last_settings(clicks, past_settings):
    last_record = past_settings[-2]  # Get the second to last record
    updated_settings = past_settings[:-2]  # Create a new list without the last entry's
    return (
        last_record["stock_allocation"],
        last_record["cash_allocation"],
        last_record["start_amount"],
        last_record["number_of_years"],
        last_record["start_year"],
        updated_settings,
    )


@app.callback(Output("history_button", "disabled"),
              Input("past_settings", "data"),
              prevent_initial_call=True
              )
def button_check(past_settings):
    return len(past_settings) <= 1


if __name__ == "__main__":
    app.run_server(debug=True)
