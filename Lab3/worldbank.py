from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from pandas_datareader import wb
import datetime

app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

indicators = {
    "EN.GHG.ALL.PC.CE.AR5": "Total greenhouse gas emissions per capita",
    "AG.LND.FRST.ZS": "Forest area (% of land area)",
    "EG.ELC.ACCS.ZS": "Access to electricity (% of population)",
    "SP.DYN.LE00.IN": "Life expectancy at birth, total (years)"
}

# get country name and ISO id for mapping on choropleth
countries = wb.get_countries()
countries["capitalCity"].replace({"": None}, inplace=True)
countries.dropna(subset=["capitalCity"], inplace=True)
countries = countries[["name", "iso3c"]]
countries = countries[countries["name"] != "Kosovo"]
countries = countries[countries["name"] != "Qatar"]
countries = countries[countries["name"] != "Kuwait"]
countries = countries[countries["name"] != "Korea, Dem. People's Rep."]
countries = countries.rename(columns={"name": "country"})


def update_wb_data():
    # Retrieve specific world bank data from API
    df = wb.download(
        indicator=(list(indicators)), country=countries["iso3c"], start=2000, end=2020
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
                        "Asian Development and Emissions",
                        style={"textAlign": "center"},
                    ),
                    dcc.Graph(id="my-choropleth", figure={}),
                    html.Div(id='hover-container', style={'display': 'none'}, children=[
                        dcc.Graph(
                            id='hover-graph',
                            config={'displayModeBar': False}
                        ),
                        dbc.Button(
                            'Close',
                            id='close-button',
                            n_clicks=0,
                            color='danger',
                            size='sm',
                            style={'marginLeft': '10px'}
                        ),
                    ])
                ],
                width=12,
            )
        ),
        dbc.Row([
            dbc.Col(
                [
                    dbc.Label(
                        "Select Data Set",
                        className="fw-bold text-center w-100",
                        style={"fontSize": 20},
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
                        "Select Years",
                        className="fw-bold text-center w-100",
                        style={"fontSize": 20},
                    ),
                    dcc.Slider(
                        id="years-range",
                        min=2000,
                        max=2020,
                        step=1,
                        value=2000,
                        marks={
                            2000: "2000",
                            2001: "'01",
                            2002: "'02",
                            2003: "'03",
                            2004: "'04",
                            2005: "'05",
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
                            2016: "'16",
                            2017: "'17",
                            2018: "'18",
                            2019: "'19",
                            2020: "'20",
                        },
                    ),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            id="my-button",
                            children="Advance Slider",
                            n_clicks=0,
                            color="primary",
                            className="mt-4 fw-bold mx-auto"
                        ),
                        width=6,
                        className="d-flex justify-content-end"
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
    Output("years-range", "value"),
    Input("my-button", "n_clicks"),
    Input("storage", "data"),
    State("years-range", "value"),
    State("dropdown-replacement", "value"),
)
def update_graph(n_clicks, stored_dataframe, years_chosen, indct_chosen):
    dff = pd.DataFrame.from_records(stored_dataframe)

    if n_clicks > 0:
        years_chosen = years_chosen + 1
    if n_clicks % 20 == 0:
        years_chosen = 2000

    dff = dff[dff.year == years_chosen]
    dff = dff.groupby(["iso3c", "country"])[indct_chosen].mean()
    dff = dff.reset_index()

    fig = px.choropleth(
        data_frame=dff,
        locations="iso3c",
        color=indct_chosen,
        scope="asia",
        hover_data={"iso3c": False, "country": True},
        labels={
            indicators["EN.GHG.ALL.PC.CE.AR5"]: "Total greenhouse gas emissions per capita",
            indicators["AG.LND.FRST.ZS"]: "Forest area (% of land area)",
            indicators["EG.ELC.ACCS.ZS"]: "Access to electricity (% of population)",
            indicators["SP.DYN.LE00.IN"]: "Life expectancy at birth, total (years)"
        },
        range_color=[0, dff[indct_chosen].quantile(0.95)]
    )
    fig.update_layout(
        geo={"projection": {"type": "natural earth"}},
        margin=dict(l=50, r=50, t=50, b=50),
    )
    return fig, years_chosen


@app.callback(
    Output('hover-graph', 'figure'),
    Output('hover-container', 'style'),
    Input("my-choropleth", "clickData"),
    Input("storage", "data"),
)
def update_output(clickData, stored_dataframe):
    default_style = {'display': 'none'}
    default_fig = px.line()

    if not clickData:
        return default_fig, default_style

    location = clickData['points'][0]['location']

    dff = pd.DataFrame.from_records(stored_dataframe)
    dff = dff[dff.iso3c == location]

    fig = px.line(
        data_frame=dff,
        x="year",
        y='Life expectancy at birth, total (years)',
        color="country",
    )

    style = {
        'display': 'block',  # Show the graph
        'position': 'absolute',  # Position it over the choropleth
        'top': '100px',  # Arbitrary position; adjust as needed
        'left': '75px',  # Arbitrary position; adjust as needed
        'zIndex': 1000  # Ensure it overlays the choropleth
    }

    return fig, style


@app.callback(
    Output('hover-graph', 'figure', allow_duplicate=True),
    Output('hover-container', 'style', allow_duplicate=True),
    Input('close-button', 'n_clicks'),
    prevent_initial_call=True
)
def closeGraph(n_clicks):
    default_style = {'display': 'none'}
    default_fig = px.line()
    return default_fig, default_style


if __name__ == "__main__":
    app.run_server(debug=True)
