# -*- coding: utf-8 -*-
import dash_bootstrap_components
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import pickle


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

    columns_needed = ["Total Year-Round Beds (ES, TH, SH)", "Total Year-Round Beds (RRH & DEM)", "Total Year-Round Beds (PSH)",
                      "Total Year-Round Beds (OPH)"]

    for sheet in sheets:
        df = pd.read_excel(excel_file, sheet_name=sheet, header=1)  # Read each sheet
        coc_col = next((col for col in df.columns if col.startswith("CoC")), None)  # Find column that starts with "CoC"
        print(f"current COC sheet: {sheet}")
        if coc_col:  # Ensure column exists
            df_filtered = df[df[coc_col].isin(["CA-600", "NY-600"])]  # Filter rows of interest

            # Select only the needed columns, ensuring "CoC Number" is correctly referenced
            cols_to_keep = [coc_col] + [col for col in columns_needed if col in df.columns]
            df_filtered = df_filtered[cols_to_keep]

            data[sheet] = df_filtered  # Store filtered data by sheet name

    return data


def grab_PIT_Data():
    # CoC Number, CoC Name, Overall Homeless, Sheltered ES Homeless, Sheltered TH Homeless, Sheltered Total Homeless,
    # Unsheltered Homeless
    excel_file = "2007-2024-PIT-Counts-by-CoC.xlsb"
    sheets = [sheet for sheet in pd.ExcelFile(excel_file).sheet_names if
              sheet.isdigit() and int(sheet) in range(2007, 2025)]
    data = {}
    columns_needed = ["CoC Number", "Overall Homeless", "Sheltered ES Homeless", "Sheltered TH Homeless",
                      "Sheltered Total Homeless"]
    for sheet in sheets:
        df = pd.read_excel(excel_file, sheet_name=sheet, header=0)
        print(f"current PIT sheet: {sheet}")
        df_filtered = df[df["CoC Number"].isin(["CA-600", "NY-600"])]  # Filter rows of interest

        # Select only the needed columns, ensuring "CoC Number" is correctly referenced
        cols_to_keep = ["CoC Number"] + [col for col in columns_needed if col in df.columns]
        df_filtered = df_filtered[cols_to_keep]

        data[sheet] = df_filtered  # Store filtered data by sheet name
    return data

def save_data(data, filename="PIT_Data.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(data, f)

def combine_data(data):
    df_list = []

    for year, df in data.items():
        df["Year"] = int(year)  # Add a 'Year' column to indicate the source sheet
        df_list.append(df)

    return pd.concat(df_list, ignore_index=True)  # Merge all DataFrames

COC_data = grab_COC_Data()
COC_combined = combine_data(COC_data)
COC_combined.set_option("display.max_columns", None)  # Show all columns
print(COC_combined.head())
#save_data(COC_combined, "COC_data.pkl")
PIT_data = grab_PIT_Data()
PIT_combined = combine_data(PIT_data)
PIT_combined.set_option("display.max_columns", None)
print(PIT_combined.head().head())
#save_data(PIT_combined, "PIT_data.pkl")
