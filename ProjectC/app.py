# -*- coding: utf-8 -*-
import dash_bootstrap_components
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

# Load processed data
df1, df2, df3, df4, df5, df6, df7 = load_and_process_data()

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
            margin=dict(l=40, r=10, t=30, b=50),
            yaxis=dict(range=[0, dff.iloc[:, 1].max() * 1.1], tickprefix="$", fixedrange=True, autorange=False),
            xaxis=dict(
                title="Year",
                fixedrange=True,
                dtick="M12",  # Every 12 months to reduce clutter
                tickformat="%Y",  # Format to display Month-Year (MM-YYYY)
            )
        )
        return fig
    else:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=dff["Year"],
                y=dff.iloc[:, 1],
                marker_color=COLORS["blue"],
            )
        )
        fig.update_layout(
            title=f"{dff.columns[1]}",
            template="none",
            height=350,
            margin=dict(l=40, r=10, t=30, b=50),
            yaxis=dict(range=[0, dff.iloc[:, 1].max() * 1.1], tickprefix="$", fixedrange=True, autorange=False),
            xaxis=dict(title="Year", fixedrange=True, tickformat="%Y"),
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
