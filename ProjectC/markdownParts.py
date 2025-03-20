from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import dataProcessing

"""
==========================================================================
Markdown Text
"""

learn_text = dcc.Markdown(
    """
    Idaho falls just below average in its costs of living compared to other States. I created a tool to explore different trends
    over time and see how costs and wages have increased or decreased.
    """
)

footer = html.Div(
    dcc.Markdown(
        """
         This information is intended solely as general information for educational
        and entertainment purposes only. Data pulled from fred.stlouisfed.org, www.eia.gov, 
        www.collegetuitioncompare.com, and data.bls.gov.
        """
    ),
    className="p-2 mt-3 bg-primary text-white small d-flex justify-content-center align-items-center",
)
