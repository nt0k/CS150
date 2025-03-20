from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

df1 = pd.read_csv("assets/Median Income.csv")
df2 = pd.read_csv("assets/Natural Gas Prices.csv")
df3 = pd.read_csv("assets/Minimum Wage.csv")
df4 = pd.read_csv("assets/Median House Price.csv")
df5 = pd.read_csv("assets/Energy Cost.csv")
df6 = pd.read_csv("assets/Ground Beef West Region.csv")
df7 = pd.read_csv("assets/Boise State Cost.csv")

# Fix date formatting
df6['Date'] = pd.to_datetime(df6['Date'], format='%b %Y')

df5 = df5.sort_values(by='Year', ascending=True)
df2 = df2.sort_values(by='Year', ascending=True)


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


def percent_calculation(dff, date_column=None, value_column=None):
    """Calculate the percent change from the first to last value and the average yearly change.

    Args:
    - dff: The dataframe with the data
    - date_column: The column containing dates (None for yearly data)
    - value_column: The column containing the values (e.g., prices or income)

    Returns:
    - A formatted string with the percent change and average yearly change
    """

    # If we are working with monthly data, extract the year and month from the date
    if date_column:
        # Convert the 'Date' column to datetime
        dff[date_column] = pd.to_datetime(dff[date_column])
        # Extract the year and month
        dff['Year'] = dff[date_column].dt.year
        dff['Month'] = dff[date_column].dt.month

        # Calculate the percent change from first to last value
        start_val = dff[value_column].iloc[0]  # First value
        end_val = dff[value_column].iloc[-1]  # Last value
        percent_change = ((end_val - start_val) / start_val) * 100

        # Calculate the average yearly change
        yearly_data = dff.groupby('Year')[value_column].last()  # Get the last value of each year
        yearly_change = yearly_data.pct_change() * 100  # Percent change between years
        avg_yearly_change = yearly_change.mean()  # Average yearly change

    else:
        # If working with yearly data, calculate directly from the years and values
        start_val = dff[value_column].iloc[0]  # First value
        end_val = dff[value_column].iloc[-1]  # Last value
        percent_change = ((end_val - start_val) / start_val) * 100

        # Calculate the average yearly change for yearly data directly
        yearly_change = dff[value_column].pct_change() * 100
        avg_yearly_change = yearly_change.mean()  # Average yearly change

    # Format the results
    result = f"Total Percent Change: {percent_change:.1f} || Average Yearly Change: {avg_yearly_change:.1f}%"

    return result