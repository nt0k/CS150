from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

df1 = pd.read_csv("assets/Median Income.csv")
df3 = pd.read_csv("assets/Natural Gas Prices.csv")
df2 = pd.read_csv("assets/Minimum Wage.csv")
df4 = pd.read_csv("assets/Median House Price.csv")
df5 = pd.read_csv("assets/Energy Cost.csv")


"""
==========================================================================
Tables
"""
store = dcc.Store(id="past_settings_store", data=[])
past_settings_table = dash_table.DataTable(
    id="past_settings",
    columns=[
        {"name": "Cash Allocation", "id": "cash_allocation"},
        {"name": "Stock Allocation", "id": "stock_allocation"},
        {"name": "Bond Allocation", "id": "bond_allocation"},
        {"name": "Start Amount", "id": "start_amount"},
        {"name": "Start Year", "id": "start_year"},
        {"name": "Number of Years", "id": "number_of_years"},
    ],
    page_size=15,
    style_table={"overflowX": "scroll"},
    data=[],  # Dynamically updated
)

"""
==========================================================================
Helper functions to calculate investment results, cagr and worst periods
"""

def cagr(dff):
    """calculate Compound Annual Growth Rate for a series and returns a formated string"""

    start_bal = dff.iat[0]
    end_bal = dff.iat[-1]
    planning_time = len(dff) - 1
    cagr_result = ((end_bal / start_bal) ** (1 / planning_time)) - 1
    return f"{cagr_result:.1%}"


def worst(dff, asset):
    """calculate worst returns for asset in selected period returns formated string"""

    worst_yr_loss = min(dff[asset])
    worst_yr = dff.loc[dff[asset] == worst_yr_loss, "Year"].iloc[0]
    return f"{worst_yr_loss:.1%} in {worst_yr}"