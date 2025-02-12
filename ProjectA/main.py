"""
Author: Nathan Kirk, nkirk@westmont.edu
Class: CS150 - Community Action Computing
Instructor: Mike Ryu, Dongyub.Ryu@gmail.com
Credit: Based on twitter_app.py from The Book of Dash
"""
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Preparing your data for usage *******************************************

df1 = pd.read_csv("assets/Idaho_2023_CO.csv", usecols=["Date", "Daily Max 8-hour CO Concentration", "Daily AQI Value"])
df2 = pd.read_csv("assets/Idaho_2023_NO2.csv", usecols=["Date", "Daily Max 1-hour NO2 Concentration"])
df3 = pd.read_csv("assets/Idaho_2023_Ozone.csv", usecols=["Date", "Daily Max 8-hour Ozone Concentration"])
df4 = pd.read_csv("assets/Idaho_2023_PM25.csv", usecols=["Date", "Daily Mean PM2.5 Concentration"])
df5 = pd.read_csv("assets/Idaho_2023_SO2.csv", usecols=["Date", "Daily Max 1-hour SO2 Concentration"])
df_list = [df1, df2, df3, df4, df5]

df = df_list[0]
# Merge CSVs together
for other_df in df_list[1:]:
    df = df.merge(other_df, on="Date", how="outer")

df = df.sort_values(by="Date")

# Adjust data so that it can filter for user input easier, keeping date as is but grouping all the pollutants under a
# single columns
df_long = pd.melt(df, id_vars=["Date"],
                  value_vars=["Daily Max 8-hour CO Concentration", "Daily AQI Value",
                              "Daily Max 1-hour NO2 Concentration", "Daily Max 8-hour Ozone Concentration",
                              "Daily Mean PM2.5 Concentration", "Daily Max 1-hour SO2 Concentration"],
                  var_name="Pollutant", value_name="Concentration")

df_long['Date'] = pd.to_datetime(df_long['Date'], format="%m/%d/%Y")

# App Layout **************************************************************

stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(__name__, external_stylesheets=stylesheets)

app.layout = html.Div(
    [
        html.Div(
            html.H1(
                "Boise - Idaho Air Pollutant Levels", style={"textAlign": "center"}
            ),
            className="row",
        ),
        html.Div(dcc.Graph(id="line-chart", figure={}), className="row"),
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Select Pollutant", style={"textAlign": "center"}),
                        dcc.Dropdown(
                            id="my-dropdown",
                            options=[
                                {"label": x, "value": x}
                                for x in sorted(df_long["Pollutant"].unique())
                            ],
                            value="Daily AQI Value",
                        ),
                    ],
                    className="three columns",
                ),
                html.Div(
                    html.Div(id="storyText",
                             children="Idaho's AQI ranges from 2-7, significantly under the national average of 35!"
                                      " Other pollutants are also under the average."),
                    className="three columns",
                    style={"border": "1px solid #ccc", "padding": "5px", "text-align": "center"}
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
    if len(chosen_value) == 0:
        return {}
    else:
        df_filtered = df_long[df_long["Pollutant"] == chosen_value]
        fig = px.line(
            data_frame=df_filtered,
            x="Date",
            y="Concentration",
            labels={
                "Date": "",
                "Concentration": "Concentration / Level",
            },
        )
        # Declutter x-axis, written with help from Gemini prompt: "here is my update_graph function please
        # help me declutter my x-axis by only showing a label for each month"
        months = df_filtered['Date'].dt.to_period('M')  # Extract year-month periods
        unique_months = months.unique()  # Get unique months
        tick_values = [m.to_timestamp() for m in unique_months]  # Convert back to timestamps
        fig.update_xaxes(
            tickvals=tick_values,
            tickformat="%m-%Y"
        )
        return fig
if __name__ == "__main__":
    app.run_server(debug=True)
