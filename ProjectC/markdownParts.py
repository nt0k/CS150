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

datasource_text = dcc.Markdown(
    """
    Data pulled from fred.stlouisfed.org and www.eia.gov.
    """
)

asset_allocation_text = dcc.Markdown(
    """
> Play with the app and see for yourself how prices of different basic items have changed over time in Idaho!
"""
)

learn_text = dcc.Markdown(
    """
    Idaho just below average in its costs of living compared to other States. I created a tool to explore different trends
    over time and see how costs and wages have increased or decreased.
    """
)

cagr_text = dcc.Markdown(
    """
    (CAGR) is the compound annual growth rate.  It measures the rate of return for an investment over a period of time, 
    such as 5 or 10 years. The CAGR is also called a "smoothed" rate of return because it measures the growth of
     an investment as if it had grown at a steady rate on an annually compounded basis.
    """
)

footer = html.Div(
    dcc.Markdown(
        """
         This information is intended solely as general information for educational
        and entertainment purposes only. 
        """
    ),
    className="p-2 mt-5 bg-primary text-white small",
)

