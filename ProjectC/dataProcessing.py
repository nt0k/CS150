from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px


def load_and_process_data():
    # Load data
    df1 = pd.read_csv("assets/Median Income.csv")
    df2 = pd.read_csv("assets/Natural Gas Prices.csv")
    df3 = pd.read_csv("assets/Minimum Wage.csv")
    df4 = pd.read_csv("assets/Median House Price.csv")
    df5 = pd.read_csv("assets/Energy Cost.csv")
    df6 = pd.read_csv("assets/Ground Beef West Region.csv")
    df7 = pd.read_csv("assets/Boise State Cost.csv")

    # Fix date formatting
    df6['Date'] = pd.to_datetime(df6['Date'], format='%b %Y', errors='coerce')
    df4['Date'] = pd.to_datetime(df4['Date'], format="%Y-%m-%d", errors='coerce')
    df1['Year'] = pd.to_datetime(df1['Year'], format='%Y', errors='coerce')
    df2['Year'] = pd.to_datetime(df2['Year'], format='%Y', errors='coerce')
    df3['Year'] = pd.to_datetime(df3['Year'], format='%Y', errors='coerce')
    df5['Year'] = pd.to_datetime(df5['Year'], format='%Y', errors='coerce')
    df7['Year'] = pd.to_datetime(df7['Year'], format='%Y', errors='coerce')

    # Sort data
    df1 = df1.sort_values(by=['Year'], ascending=True)
    df2 = df2.sort_values(by=['Year'], ascending=True)
    df3 = df3.sort_values(by=['Year'], ascending=True)
    df4 = df4.sort_values(by=['Date'], ascending=True)
    df5 = df5.sort_values(by=['Year'], ascending=True)
    df6 = df6.sort_values(by=['Date'], ascending=True)
    df7 = df7.sort_values(by=['Year'], ascending=True)

    # Filter by year range
    dfs = [df1, df2, df3, df4, df5, df6, df7]
    # Generated with help from Grok prompt: "help me filter my dataframes"
    for i, df in enumerate(dfs):
        if 'Date' in df.columns:
            dfs[i] = df[df['Date'].notna() & (df['Date'].dt.year >= 2017) & (df['Date'].dt.year <= 2023)]
        elif 'Year' in df.columns:
            dfs[i] = df[df['Year'].notna() & (df['Year'].dt.year >= 2017) & (df['Year'].dt.year <= 2023)]

    return dfs[0], dfs[1], dfs[2], dfs[3], dfs[4], dfs[5], dfs[6]


"""
==========================================================================
Tables
"""

"""
==========================================================================
Helper functions
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

        dff_copy = dff.copy()
        # Extract the year and month
        dff_copy['Year'] = dff_copy[date_column].dt.year
        dff_copy['Month'] = dff_copy[date_column].dt.month

        # Calculate the percent change from first to last value
        start_val = dff[value_column].iloc[0]  # First value
        end_val = dff[value_column].iloc[-1]  # Last value
        percent_change = ((end_val - start_val) / start_val) * 100

        # Calculate the average yearly change
        yearly_data = dff_copy.groupby('Year')[value_column].last()  # Get the last value of each year
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
    result = f"Total Percent Change: {percent_change:.1f}% || Average Yearly Change: {avg_yearly_change:.1f}%"

    return result


def generate_table(df, title):
    return html.Div([
        html.H4(title),
        dash_table.DataTable(
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict("records"),
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left"},
            page_size=10
        )
    ])
