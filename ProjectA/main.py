"""
Author: Nathan Kirk, nkirk@westmont.edu
Class: CS150 - Community Action Computing
Instructor: Mike Ryu, Dongyub.Ryu@gmail.com
Credit: Based on twitter_app.py from The Book of Dash
"""
import random

import pandas as pd
import plotly.express as px

from dash import Dash, dcc, html, Input, Output

# Preparing your data for usage *******************************************

df1 = pd.read_csv("Idaho_2023_CO.csv", usecols=["Date", "Daily Max 8-hour CO Concentration", "Daily AQI Value"])
df2 = pd.read_csv("Idaho_2023_NO2.csv", usecols=["Date", "Daily Max 1-hour NO2 Concentration"])
df3 = pd.read_csv("Idaho_2023_Ozone.csv", usecols=["Date", "Daily Max 8-hour Ozone Concentration"])
df4 = pd.read_csv("Idaho_2023_PM25.csv", usecols=["Date", "Daily Mean PM2.5 Concentration"])
df5 = pd.read_csv("Idaho_2023_SO2.csv", usecols=["Date", "Daily Max 1-hour SO2 Concentration"])
df_list = [df1, df2, df3, df4, df5]

df = df_list[0]
for other_df in df_list[1:]:
    df = df.merge(other_df, on="Date", how="outer")  # Adjust 'how' based on needs

# Sort by date
df = df.sort_values(by="Date")

# Adjust data so that it can filter for user input easier
df_long = pd.melt(df, id_vars=["Date"],
                  value_vars=["Daily Max 8-hour CO Concentration", "Daily AQI Value",
                    "Daily Max 1-hour NO2 Concentration", "Daily Max 8-hour Ozone Concentration",
                    "Daily Mean PM2.5 Concentration", "Daily Max 1-hour SO2 Concentration"],
                    var_name="Pollutant", value_name="Concentration")

# App Layout **************************************************************

stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(__name__, external_stylesheets=stylesheets)

app.layout = html.Div(
    [
        html.Div(
            html.H1(
                "Idaho Air Pollutant Levels", style={"textAlign": "center"}
            ),
            className="row",
        ),
        html.Div(dcc.Graph(id="line-chart", figure={}), className="row"),
        html.Div(
            html.H3("Select Pollutant", style={"textAlign": "center"})
        ),
        html.Div(
            [
                html.Div(
                    dcc.Dropdown(
                        id="my-dropdown",
                        options=[
                            {"label": x, "value": x}
                            for x in sorted(df_long["Pollutant"].unique())
                        ],
                        value="Daily AQI Value"
                    ),
                    className="three columns",
                ),
            ],
            className="row",
            style={"display": "flex", "justifyContent": "center"}
        ),
    ]
)


# Callbacks ***************************************************************
@app.callback(
    Output(component_id="line-chart", component_property="figure"),
    [Input(component_id="my-dropdown", component_property="value")],
)
def update_graph(chosen_value):
    print(f"Values chosen by user: {chosen_value}")

    if len(chosen_value) == 0:
        return {}
    else:
        df_filtered = df_long[df_long["Pollutant"] == chosen_value]
        fig = px.line(
            data_frame=df_filtered,
            x= "Date",
            y= "Concentration",
            line_shape= "spline"
        )
        fig.update_layout(
            yaxis=dict(
                tickmode="linear",  # Auto-tick mode to avoid clutter
                dtick=30  # Adjust this number to control how many y-axis labels appear
            )
        )
        return fig

if __name__ == "__main__":
    app.run_server(debug=True)
