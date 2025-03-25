# -*- coding: utf-8 -*-
import dash_bootstrap_components
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

def grab_COC_Data():
    # Rows of interest CoC Number (CA-600, NY-600), columns of interest
    # Total Year-Round Beds (ES, TH, SH)
    # Total Year-Round Beds (RRH & DEM)
    # Total Year-Round Beds (PSH)
    # Total Year-Round Beds (OPH)
    # Total Total (sum all together)

    excel_file = "2007-2024-HIC-Counts-by-CoC.xlsx"
    sheets = [sheet for sheet in pd.ExcelFile(excel_file).sheet_names if sheet != "Revisions"]  # Exclude "Revisions"

    data = {}

    for sheet in sheets:
        df = pd.read_excel(excel_file, sheet_name=sheet, header=1)  # Read each sheet
        coc_col = next((col for col in df.columns if col.startswith("CoC")), None)  # Find column that starts with "CoC"

        if coc_col:  # Ensure column exists
            df_filtered = df[df[coc_col].isin(["CA-600", "NY-600"])]  # Filter rows of interest
            data[sheet] = df_filtered  # Store filtered data by sheet name

    return data

print(grab_COC_Data())