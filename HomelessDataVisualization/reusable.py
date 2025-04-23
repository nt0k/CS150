"""
Credit: Taken from dash-svm example app.
"""
import os
import pickle
from textwrap import dedent
from dash import dcc, html

# Display utility functions
def _merge(a, b):
    return dict(a, **b)


def _omit(omitted_keys, d):
    return {k: v for k, v in d.items() if k not in omitted_keys}


# Custom Display Components
def Card(children, **kwargs):
    return html.Section(className="card m-3", children=children, **_omit(["style"], kwargs))


def FormattedSlider(**kwargs):
    return html.Div(
        style=kwargs.get("style", {}), children=dcc.Slider(**_omit(["style"], kwargs))
    )


def NamedSlider(name, **kwargs):
    return html.Div(
        style={"padding": "10px 10px 10px 4px"},
        children=[
            html.P(f"{name}:"),
            html.Div(style={"margin-left": "6px"}, children=dcc.Slider(**kwargs)),
        ],
    )


def NamedDropdown(name, **kwargs):
    return html.Div(
        style={"padding": "10px 10px 10px 4px"},
        children=[
            html.P(children=f"{name}:", style={"margin": "1px", "textAlign": "center"}),
            dcc.Dropdown(**kwargs, style={"width": "80%", "margin": "0 auto"}),
        ],
    )


def NamedRadioItems(name, **kwargs):
    return html.Div(
        style={"padding": "20px 10px 25px 4px"},
        children=[html.P(children=f"{name}:"), dcc.RadioItems(**kwargs)],
    )

# Helper function to load a pickle file from the Data folder
def load_pickle_data(filename):
    # Construct full path to the file in the Data folder
    data_folder = "Data"
    file_path = os.path.join(data_folder, filename)
    # Open and load the pickle file
    with open(file_path, "rb") as f:
        data = pickle.load(f)
    return data

# Non-generic
def DemoDescription(filename, strip=False):
    with open(filename, "r") as file:
        text = file.read()

    if strip:
        text = text.split("<Start Description>")[-1]
        text = text.split("<End Description>")[0]

    return html.Div(
        className="row",
        style={
            "padding": "15px 30px 27px",
            "margin": "45px auto 45px",
            "width": "80%",
            "max-width": "1024px",
            "borderRadius": 5,
            "border": "thin lightgrey solid",
            "font-family": "Roboto, sans-serif",
        },
        children=dcc.Markdown(dedent(text)),
    )
