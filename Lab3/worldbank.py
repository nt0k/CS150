from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from pandas_datareader import wb
import datetime

app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

indicators = {
    "IT.NET.USER.ZS": "Individuals using the Internet (% of population)",
    "SG.GEN.PARL.ZS": "Proportion of seats held by women in national parliaments (%)",
    "SP.URB.TOTL.IN.ZS": "Urban population (% of total population)",
}

# get country name and ISO id for mapping on choropleth
countries = wb.get_countries()
countries["capitalCity"].replace({"": None}, inplace=True)
countries.dropna(subset=["capitalCity"], inplace=True)
countries = countries[["name", "iso3c"]]
countries = countries[countries["name"] != "Kosovo"]
countries = countries[countries["name"] != "Korea, Dem. People's Rep."]
countries = countries.rename(columns={"name": "country"})


def update_wb_data():
    # Retrieve specific world bank data from API
    df = wb.download(
        indicator=(list(indicators)), country=countries["iso3c"], start=2005, end=2016
    )
    df = df.reset_index()
    df.year = df.year.astype(int)

    # Add country ISO3 id to main df
    df = pd.merge(df, countries, on="country")
    df = df.rename(columns=indicators)
    return df


app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.H1(
                        "Comparison of World Bank Country Data",
                        style={"textAlign": "center"},
                    ),
                    html.H3(id="last-run", children="",
                            style={"textAlign": "center"},
                            ),
                    dcc.Graph(id="my-choropleth", figure={}),
                ],
                width=12,
            )
        ),
        dbc.Row([
            dbc.Col(
                [
                    dbc.Label(
                        "Select Data Set:",
                        className="fw-bold",
                        style={"textDecoration": "underline", "fontSize": 20},
                    ),
                    dcc.Dropdown(
                        id="dropdown-replacement",
                        options=[{"label": i, "value": i} for i in indicators.values()],
                        value=list(indicators.values())[0],
                    ),
                ],
                width=6,
            ),
            dbc.Col(
                [
                    dbc.Label(
                        "Select Years:",
                        className="fw-bold",
                        style={"textDecoration": "underline", "fontSize": 20},
                    ),
                    dcc.RangeSlider(
                        id="years-range",
                        min=2005,
                        max=2016,
                        step=1,
                        value=[2005, 2006],
                        marks={
                            2005: "2005",
                            2006: "'06",
                            2007: "'07",
                            2008: "'08",
                            2009: "'09",
                            2010: "'10",
                            2011: "'11",
                            2012: "'12",
                            2013: "'13",
                            2014: "'14",
                            2015: "'15",
                            2016: "2016",
                        },
                    ),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Span(id="click-count", children="Clicked 0 times"),
                        width="auto",
                        className="mt-4 align-items-center"
                    ),
                    dbc.Col(
                        dbc.Button(
                            id="my-button",
                            children="Submit",
                            n_clicks=0,
                            color="primary",
                            className="mt-4 fw-bold"
                        ),
                        width="auto"
                    ),
                ],
                justify="end"
            ),
            dcc.Store(id="storage", storage_type="session", data={}),
            dcc.Interval(id="timer", interval=1000 * 60, n_intervals=0),
        ],
        ),
    ],
)


@app.callback(Output("storage", "data"),
              Input("timer", "n_intervals")
              )
def store_data(n_time):
    dataframe = update_wb_data()
    return dataframe.to_dict("records")


@app.callback(
    Output("my-choropleth", "figure"),
    Output("last-run", "children"),
    Output("click-count", "children"),
    Output("years-range", "value"),
    Input("my-button", "n_clicks"),
    Input("storage", "data"),
    State("years-range", "value"),
    State("dropdown-replacement", "value"),
)
def update_graph(n_clicks, stored_dataframe, years_chosen, indct_chosen):
    dff = pd.DataFrame.from_records(stored_dataframe)

    currentDate = datetime.datetime.now().date().strftime("%m-%d-%Y")
    currentTime = datetime.datetime.now().time().strftime("%H:%M:%S")
    lastRun = f"{currentDate} {currentTime}"

    if n_clicks > 0:
        years_chosen = years_chosen[0], years_chosen[1] + 1

    if years_chosen[0] != years_chosen[1]:
        dff = dff[dff.year.between(years_chosen[0], years_chosen[1])]
        dff = dff.groupby(["iso3c", "country"])[indct_chosen].mean()
        dff = dff.reset_index()

        fig = px.choropleth(
            data_frame=dff,
            locations="iso3c",
            color=indct_chosen,
            scope="world",
            hover_data={"iso3c": False, "country": True},
            labels={
                indicators["SG.GEN.PARL.ZS"]: "% parliament women",
                indicators["IT.NET.USER.ZS"]: "pop % using internet",
            },
        )
        fig.update_layout(
            geo={"projection": {"type": "natural earth"}},
            margin=dict(l=50, r=50, t=50, b=50),
        )
        return fig, f"Data Last Fetched: {lastRun}", f"Clicked {n_clicks} times", years_chosen

    if years_chosen[0] == years_chosen[1]:
        dff = dff[dff.year.between(years_chosen[0], years_chosen[1])]
        dff = dff.groupby(["iso3c", "country"])[indct_chosen].mean()
        dff = dff.reset_index()

        fig = px.choropleth(
            data_frame=dff,
            locations="iso3c",
            color=indct_chosen,
            scope="world",
            hover_data={"iso3c": False, "country": True},
            labels={
                indicators["SG.GEN.PARL.ZS"]: "% parliament women",
                indicators["IT.NET.USER.ZS"]: "pop % using internet",
            },
        )
        fig.update_layout(
            geo={"projection": {"type": "natural earth"}},
            margin=dict(l=50, r=50, t=50, b=50),
        )
        return fig, f"Data Last Fetched: {lastRun}", f"Clicked {n_clicks} times", years_chosen


if __name__ == "__main__":
    app.run_server(debug=True)
