import dash
import numpy as np
import scipy
from dash import *
import plotly.graph_objs as go
import pandas as pd
from Lab5 import *
from Lab5 import reusable as drc
from Lab5 import figures as figgy
from Lab5 import utilities
import plotly.figure_factory as ff
import dash_bootstrap_components as dbc
from sklearn import metrics
from sklearn.decomposition import PCA
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])

app.layout = html.Div(className="app-container", children=[
    html.H1(style={"textAlign": "center"}, className="title mb-3 mt-2", children='Credit Card Approval SVM Prediction'),
    html.Div(style={"textAlign": "center"}, className="subtitle mb-3",
             children='By Nathan Kirk for CS150 | nkirk@westmont.edu'),

    dbc.Row([
        dbc.Col(html.Div(id="left-column", children=[
            drc.Card(id="first-card", children=[
                html.H4(id="description-title", children="Description", className="m-2"),
                html.P(id="description-text", className="m-2",
                       children="This model tries to predict if a person will get approved for a"
                                "credit card by looking at factors such as age, income, employment"
                                "and many others. Try playing around with the factors below and see"
                                "how it impacts the confusion matrix and ROC curve! The test percentage"
                                " controls how much of the data is used for training the model. The regulation"
                                " parameter controls the trade-off between the model's complexity and its ability "
                                "to classify training data correctly. And the function type determines what type "
                                "of function the model should use to separate the data."),
                drc.NamedSlider("Test Percentage", id="test_size_slider", min=0.1, max=0.9, step=0.1, value=0.2),
                drc.NamedSlider("Regulation Parameter", id="c_param_slider", min=0.1, max=1, step=0.1, value=1),
                drc.NamedDropdown("Function Type (Kernel)", id="kernel_dropdown",
                                  options=['linear', 'poly', 'sigmoid', 'rbf'],
                                  value="rbf"),
                dbc.Button("Reset Settings", id="reset_button", n_clicks=0, className="m-2"),
            ])
        ]), width=6),

        dbc.Col(html.Div(id="right-column", children=[
            drc.Card(id="second-card", children=[
                dcc.Graph(id="model_graph", figure={}),
                dcc.Graph(id="roc_graph", figure={}),
                html.Hr(),
                html.Div(id="confusion_matrix")
            ])
        ]), width=6),
    ])
])


@app.callback(Output("model_graph", "figure"),
              Output("roc_graph", "figure"),
              Output("confusion_matrix", "children"),
              Input("test_size_slider", "value"),
              Input("c_param_slider", "value"),
              Input("kernel_dropdown", "value"),
              )
def update_model_graph(test_size, c_param, kernel_dropdown):
    df = utilities.pull_and_clean_data()
    accuracy, TP, FP, TN, FN, model, X_test, y_test = utilities.classify_svm(df, test_size, c_param, kernel_dropdown)

    table = html.Div([
        html.H4("Confusion Matrix", style={"textAlign": "center"}),
        dash_table.DataTable(
            columns=[{"name": "", "id": "index"}, {"name": "Predicted Negative", "id": "neg"},
                     {"name": "Predicted Positive", "id": "pos"}],
            data=[
                {"index": "Actual Negative", "neg": TN, "pos": FP},
                {"index": "Actual Positive", "neg": FN, "pos": TP}
            ],
            style_cell={'textAlign': 'center'}
        )
    ])

    # --- Create Scatter Plot Visualization for Classifier ---
    X_test_df = pd.DataFrame(X_test, columns=df.drop(columns=["label"]).columns).reset_index(drop=True)

    feature1 = "Annual_income"
    feature2 = "Employed_days"

    # Get predicted labels for X_test
    y_pred = model.predict(X_test)

    # Identify correct and incorrect predictions
    correct_idx = np.where(y_pred == y_test)[0]
    incorrect_idx = np.where(y_pred != y_test)[0]


    trace_correct = go.Scatter(
        x=X_test_df.loc[correct_idx, feature1],
        y=X_test_df.loc[correct_idx, feature2],
        mode='markers',
        name='Correctly Classified',
        marker=dict(color='green', symbol='circle', size=10)
    )

    trace_incorrect = go.Scatter(
        x=X_test_df.loc[incorrect_idx, feature1],
        y=X_test_df.loc[incorrect_idx, feature2],
        mode='markers',
        name='Misclassified',
        marker=dict(color='red', symbol='x', size=10)
    )

    fig1 = go.Figure(data=[trace_correct, trace_incorrect])
    fig1.update_layout(
        title="Classifier Visualization",
        xaxis_title=feature1,
        yaxis_title=feature2,
        margin=dict(l=50, r=50, t=50, b=50)
    )

    decision_test = model.decision_function(X_test)
    fpr, tpr, threshold = metrics.roc_curve(y_test, decision_test)

    # Ensure unique FPR values
    fpr, unique_indices = np.unique(fpr, return_index=True)
    tpr = tpr[unique_indices]

    fpr_smooth = np.linspace(fpr.min(), fpr.max(), 200)
    tpr_smooth = scipy.interpolate.make_interp_spline(fpr, tpr, k=3)(fpr_smooth)

    auc_score = metrics.roc_auc_score(y_true=y_test, y_score=decision_test)

    trace0 = go.Scatter(
        x=fpr_smooth, y=tpr_smooth, mode="lines", name="Test Data"
    )

    layout = go.Layout(
        title=f"ROC Curve (AUC = {auc_score:.3f})",
        xaxis=dict(title="False Positive Rate"),
        yaxis=dict(title="True Positive Rate"),
        legend=dict(x=0, y=1.05, orientation="h"),
        margin=dict(l=100, r=10, t=45, b=40),
    )

    data = [trace0]
    fig2 = go.Figure(data=data, layout=layout)

    return fig1, fig2, table


@app.callback(
    Output("test_size_slider", "value"),
    Output("c_param_slider", "value"),
    Output("kernel_dropdown", "value"),
    Input("reset_button", "n_clicks"),
)
def reset(clicks):
    return 0.2, 1, "rbf"


if __name__ == '__main__':
    app.run(debug=True)
