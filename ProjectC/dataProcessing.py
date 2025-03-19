from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

df1 = pd.read_csv("assets/Natural Gas Prices.csv")
df2 = pd.read_csv("assets/Minimum Wage.csv")
df3 = pd.read_csv("assets/Median Income.csv")
df4 = pd.read_csv("assets/Median House Price.csv")
df5 = pd.read_csv("assets/Energy Cost.csv")

print(df5.to_string())

#  make dataframe from  spreadsheet:
df = pd.read_csv("assets/historic.csv")

MAX_YR = df.Year.max()
MIN_YR = df.Year.min()
START_YR = 2007

# since data is as of year end, need to add start year
df = (
    pd.concat(
        [pd.DataFrame({"Year": [MIN_YR - 1]}), df]
    )
    .sort_values("Year", ignore_index=True)
    .fillna(0)
)

"""
==========================================================================
Tables
"""

total_returns_table = dash_table.DataTable(
    id="total_returns",
    columns=[{"id": "Year", "name": "Year", "type": "text"}]
            + [
                {"id": col, "name": col, "type": "numeric", "format": {"specifier": "$,.0f"}}
                for col in ["Cash", "Bonds", "Stocks", "Total"]
            ],
    page_size=15,
    style_table={"overflowX": "scroll"},
)
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

annual_returns_pct_table = dash_table.DataTable(
    id="annual_returns_pct",
    columns=(
            [{"id": "Year", "name": "Year", "type": "text"}]
            + [
                {"id": col, "name": col, "type": "numeric", "format": {"specifier": ".1%"}}
                for col in df.columns[1:]
            ]
    ),
    data=df.to_dict("records"),
    sort_action="native",
    page_size=15,
    style_table={"overflowX": "scroll"},
)


def make_summary_table(dff):
    """Make html table to show cagr and  best and worst periods"""

    table_class = "h5 text-body text-nowrap"
    cash = html.Span(
        [html.I(className="fa fa-money-bill-alt"), " Cash"], className=table_class
    )
    bonds = html.Span(
        [html.I(className="fa fa-handshake"), " Bonds"], className=table_class
    )
    stocks = html.Span(
        [html.I(className="fa fa-industry"), " Stocks"], className=table_class
    )
    inflation = html.Span(
        [html.I(className="fa fa-ambulance"), " Inflation"], className=table_class
    )

    start_yr = dff["Year"].iat[0]
    end_yr = dff["Year"].iat[-1]

    df_table = pd.DataFrame(
        {
            "": [cash, bonds, stocks, inflation],
            f"Rate of Return (CAGR) from {start_yr} to {end_yr}": [
                cagr(dff["all_cash"]),
                cagr(dff["all_bonds"]),
                cagr(dff["all_stocks"]),
                cagr(dff["inflation_only"]),
            ],
            f"Worst 1 Year Return": [
                worst(dff, "3-mon T.Bill"),
                worst(dff, "10yr T.Bond"),
                worst(dff, "S&P 500"),
                "",
            ],
        }
    )
    return dbc.Table.from_dataframe(df_table, bordered=True, hover=True)

"""
==========================================================================
Helper functions to calculate investment results, cagr and worst periods
"""


def backtest(stocks, cash, start_bal, nper, start_yr):
    """calculates the investment returns for user selected asset allocation,
    rebalanced annually and returns a dataframe
    """

    end_yr = start_yr + nper - 1
    cash_allocation = cash / 100
    stocks_allocation = stocks / 100
    bonds_allocation = (100 - stocks - cash) / 100

    # Select time period - since data is for year end, include year prior
    # for start ie year[0]
    dff = df[(df.Year >= start_yr - 1) & (df.Year <= end_yr)].set_index(
        "Year", drop=False
    )
    dff["Year"] = dff["Year"].astype(int)

    # add columns for My Portfolio returns
    dff["Cash"] = cash_allocation * start_bal
    dff["Bonds"] = bonds_allocation * start_bal
    dff["Stocks"] = stocks_allocation * start_bal
    dff["Total"] = start_bal
    dff["Rebalance"] = True

    # calculate My Portfolio returns
    for yr in dff.Year + 1:
        if yr <= end_yr:
            # Rebalance at the beginning of the period by reallocating
            # last period's total ending balance
            if dff.loc[yr, "Rebalance"]:
                dff.loc[yr, "Cash"] = dff.loc[yr - 1, "Total"] * cash_allocation
                dff.loc[yr, "Stocks"] = dff.loc[yr - 1, "Total"] * stocks_allocation
                dff.loc[yr, "Bonds"] = dff.loc[yr - 1, "Total"] * bonds_allocation

            # calculate this period's  returns
            dff.loc[yr, "Cash"] = dff.loc[yr, "Cash"] * (
                    1 + dff.loc[yr, "3-mon T.Bill"]
            )
            dff.loc[yr, "Stocks"] = dff.loc[yr, "Stocks"] * (1 + dff.loc[yr, "S&P 500"])
            dff.loc[yr, "Bonds"] = dff.loc[yr, "Bonds"] * (
                    1 + dff.loc[yr, "10yr T.Bond"]
            )
            dff.loc[yr, "Total"] = dff.loc[yr, ["Cash", "Bonds", "Stocks"]].sum().astype(int)

    dff = dff.reset_index(drop=True)
    columns = ["Cash", "Stocks", "Bonds", "Total"]
    dff[columns] = dff[columns].round(0)

    # create columns for when portfolio is all cash, all bonds or  all stocks,
    #   include inflation too
    #
    # create new df that starts in yr 1 rather than yr 0
    dff1 = (dff[(dff.Year >= start_yr) & (dff.Year <= end_yr)]).copy()
    #
    # calculate the returns in new df:
    columns = ["all_cash", "all_bonds", "all_stocks", "inflation_only"]
    annual_returns = ["3-mon T.Bill", "10yr T.Bond", "S&P 500", "Inflation"]
    for col, return_pct in zip(columns, annual_returns):
        dff1[col] = round(start_bal * (1 + (1 + dff1[return_pct]).cumprod() - 1), 0)
    #
    # select columns in the new df to merge with original
    dff1 = dff1[["Year"] + columns]
    dff = dff.merge(dff1, how="left")
    # fill in the starting balance for year[0]
    dff.loc[0, columns] = start_bal
    return dff


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