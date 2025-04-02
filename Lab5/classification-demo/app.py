import dash
from dash import *
import plotly.graph_objs as go
import pandas as pd
from Lab5 import *
from Lab5 import reusable as drc
from Lab5 import figures as figgy
from Lab5 import utilities
import plotly.figure_factory as ff
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(className="app-container", children=[
    html.H1(style={"textAlign": "center"}, className="title mb-3", children='Credit Card Approval SVM Prediction'),
    html.Div(style={"textAlign": "center"}, className="subtitle mb-3", children='By Nathan Kirk for CS150'),

    dbc.Row([
        dbc.Col(html.Div(id="left-column", children=[
            drc.Card(id="first-card", children=[
                drc.NamedSlider("Test Size", id="test_size_slider", min=0.1, max=0.9, step=0.1, value=0.2),
                drc.NamedSlider("Regulation Parameter", id="c_param_slider", min=0.1, max=1, step=0.1, value=1),
                drc.NamedDropdown("Kernel", id="kernel_dropdown", options=["rbf"], value="rbf"),
            ])
        ]), width=6, align="center"),

        dbc.Col(html.Div(id="right-column", children=[
            drc.Card(id="second-card", children=[
                dcc.Graph(id="model_graph", figure={})
            ])
        ]), width=6, align="center"),
    ])
])


@app.callback(Output("model_graph", "figure"),
              Input("test_size_slider", "value"),
              Input("c_param_slider", "value"),
              Input("kernel_dropdown", "value"),
              )
def update_model_graph(test_size, c_param, kernel_dropdown):
    df = utilities.pull_and_clean_data()
    accuracy, results_df = utilities.classify_svm(df, test_size, c_param, kernel_dropdown)

    # Create confusion matrix
    cm = pd.crosstab(results_df['Actual'], results_df['Predicted'], rownames=['Actual'], colnames=['Predicted'])

    # Convert to a Plotly figure
    fig = ff.create_annotated_heatmap(
        z=cm.values,
        x=cm.columns.tolist(),
        y=cm.index.tolist(),
        colorscale="Blues",
        showscale=True
    )

    fig.update_layout(
        title=f"SVM Confusion Matrix (Accuracy: {accuracy:.2f})",
        xaxis_title="Predicted Label",
        yaxis_title="Actual Label"
    )

    return fig


if __name__ == '__main__':
    app.run(debug=True)
