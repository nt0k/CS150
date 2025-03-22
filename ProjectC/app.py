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
    "blue": "#008cba",
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
                marker_color=COLORS["blue"],
            )
        )
        # Generated with help from ChatGPT prompt "have my graph function only display certain months"
        fig.update_layout(
            title=f"{dff.columns[1]}",
            template="none",
            height=350,
            margin=dict(l=40, r=10, t=30, b=35),
            yaxis=dict(range=[0, None], tickprefix="$", fixedrange=True),
            xaxis=dict(
                title="Year",
                fixedrange=True,
                dtick="M12",  # Every 6 months to reduce clutter
                tickformat="%m-%Y",  # Format to display Month-Year (MM-YYYY)
            )
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
                marker_color=COLORS["blue"],
            )
        )
        fig.update_layout(
            title=f"{dff.columns[1]} in Idaho over the last {yrs} years",
            template="none",
            height=350,
            margin=dict(l=40, r=10, t=30, b=35),
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
        # I found myself unable to get this functionality working in time :(
        #
        # dbc.Button("Use Consistent Years", id="consistent_button", color="primary", className="me-2", n_clicks=0,
        #           disabled=False),
        # dbc.Button("Use All Available Data", id="all_button", color="primary", className="me-2", n_clicks=0,
        #           disabled=True),
    ],
    body=True,
    className="mt-4",
)

# ========= Learn Tab  Components
learn_card = dbc.Card(
    [
        dbc.CardHeader("An Introduction to this project"),
        dbc.CardBody(learn_text),
    ],
    className="mt-4",
)

# ========= Raw Data Tab
tables_card = dbc.Card(
    [
        dbc.CardHeader("Raw Data"),
        dbc.CardBody([
            generate_table(df, f"{df.columns[1]}") for df in [df1, df2, df3, df4, df5, df6, df7]
        ]),
    ],
    className="mt-4",
)

# ========= Build tabs
tabs = dbc.Tabs(
    [
        dbc.Tab(learn_card, tab_id="tab1", label="About"),
        dbc.Tab(
            [slider_card],
            tab_id="tab-2",
            label="Play",
            className="pb-4",
        ),
        dbc.Tab(tables_card, tab_id="tab3", label="Raw Data", className="pb-4"),
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
                        html.P(percent_calculation(df1, None, "Idaho Median Income"), style={"textAlign": "center"}),
                        dcc.Graph(id="comparison_graph", figure=make_line_chart(df4), className="pb-2"),
                        html.P(id="comparison_text",
                               children=percent_calculation(df4, "Date", "Idaho Median House Price of Listings"),
                               style={"textAlign": "center"}),
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

'''
I found myself unable to get this functionality working in time :(

@app.callback(
    Output("all_button", "disabled", allow_duplicate=True),
    Output("consistent_button", "disabled", allow_duplicate=True),
    Output("comparison_graph", "figure", allow_duplicate=True),
    Output("income_graph", "figure", allow_duplicate=True),
    Input("consistent_button", "n_clicks"),
    State("comparison_graph", "figure"),
    State("income_graph", "figure"),
    prevent_initial_call=True,
)
def toggle_all(n_clicks, fig1, fig2):
    if n_clicks == 0:
        return True  # Keep "All" button disabled initially

    comparison_graph = go.Figure(fig1)
    income_graph = go.Figure(fig2)

    comparison_graph.update_layout(
        xaxis=dict(
            range=["2017-01-01", "2023-12-31"]  # Limit x-axis to 2017-2023
        )
    )
    income_graph.update_layout(
        xaxis=dict(
            range=["2017-01-01", "2023-12-31"]  # Limit x-axis to 2017-2023
        )
    )
    return False, True, comparison_graph, income_graph # Enable "All" button when "Consistent" is clicked


@app.callback(
    Output("consistent_button", "disabled", allow_duplicate=True),
    Output("all_button", "disabled", allow_duplicate=True),
    Output("comparison_graph", "figure", allow_duplicate=True),
    Output("income_graph", "figure", allow_duplicate=True),
    Input("all_button", "n_clicks"),
    State("comparison_graph", "figure"),
    State("income_graph", "figure"),
    prevent_initial_call=True,
)
def toggle_consistent(n_clicks, fig1, fig2):
    if n_clicks == 0:
        return False  # Keep "Consistent" button enabled initially

    comparison_graph = go.Figure(fig1)
    income_graph = go.Figure(fig2)

    comparison_graph.update_layout(
        xaxis=dict(
            range=None  # This will remove the custom range and let Plotly auto-calculate
        )
    )
    income_graph.update_layout(
        xaxis=dict(
            range=None  # This will remove the custom range and let Plotly auto-calculate
        )
    )
    return False, True, comparison_graph, income_graph  # Disable "Consistent" button when "All" is clicked
'''


@app.callback(
    Output("comparison_graph", "figure"),
    Output("comparison_text", "children"),
    Input("segment_dropdown", "value"),
    prevent_initial_call=True,
)
def update_comparison_graph(selected_val):
    if selected_val == "Median Home Price" or selected_val == "Ground Beef Price":
        return make_line_chart(dataframes[selected_val]), percent_calculation(dataframes[selected_val], "Date",
                                                                              dataframes[selected_val].columns[1])
    else:
        return make_line_chart(dataframes[selected_val]), percent_calculation(dataframes[selected_val], None,
                                                                              dataframes[selected_val].columns[1])


if __name__ == "__main__":
    app.run_server(debug=True)
