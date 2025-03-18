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
    [Data source:](http://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html)
    Historical Returns on Stocks, Bonds and Bills from NYU Stern School of
    Business
    """
)

asset_allocation_text = dcc.Markdown(
    """
> **Asset allocation** is one of the main factors that drive portfolio risk and returns.   Play with the app and see for yourself!

> Change the allocation to cash, bonds and stocks on the sliders and see how your portfolio performs over time in the graph.
  Try entering different time periods and dollar amounts too.
"""
)

learn_text = dcc.Markdown(
    """
    Past performance certainly does not determine future results, but you can still
    learn a lot by reviewing how various asset classes have performed over time.

    Use the sliders to change the asset allocation (how much you invest in cash vs
    bonds vs stock) and see how this affects your returns.

    Note that the results shown in "My Portfolio" assumes rebalancing was done at
    the beginning of every year.  Also, this information is based on the S&P 500 index
    as a proxy for "stocks", the 10 year US Treasury Bond for "bonds" and the 3 month
    US Treasury Bill for "cash."  Your results of course,  would be different based
    on your actual holdings.

    This is intended to help you determine your investment philosophy and understand
    what sort of risks and returns you might see for each asset category.

    The  data is from [Aswath Damodaran](http://people.stern.nyu.edu/adamodar/New_Home_Page/home.htm)
    who teaches  corporate finance and valuation at the Stern School of Business
    at New York University.

    Check out his excellent on-line course in
    [Investment Philosophies.](http://people.stern.nyu.edu/adamodar/New_Home_Page/webcastinvphil.htm)
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
        and entertainment purposes only and is not a substitute for professional advice and
        services from qualified financial services providers familiar with your financial
        situation.    
        """
    ),
    className="p-2 mt-5 bg-primary text-white small",
)

