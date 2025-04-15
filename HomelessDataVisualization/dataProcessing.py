# -*- coding: utf-8 -*-
import pandas as pd
import pickle
import warnings

warnings.filterwarnings("ignore", message="Cannot parse header or footer")


def grab_HIC_Data():
    # Rows of interest CoC Number (CA-600, NY-600), columns of interest
    # Total Year-Round Beds (ES, TH, SH)
    # Total Year-Round Beds (RRH & DEM)
    # Total Year-Round Beds (PSH)
    # Total Year-Round Beds (OPH)
    # Total Total (sum all together)

    excel_file = "Data/2007-2024-HIC-Counts-by-CoC.xlsx"
    sheets = [sheet for sheet in pd.ExcelFile(excel_file).sheet_names if
              sheet.isdigit() and int(sheet) in range(2014, 2025)]
    data = {}

    columns_needed = ["Total Year-Round Beds (ES, TH, SH)", "Total Year-Round Beds (RRH)",
                      "Total Year-Round Beds (PSH)",
                      "Total Year-Round Beds (OPH)"]

    for sheet in sheets:
        df = pd.read_excel(excel_file, sheet_name=sheet, header=1)  # Read each sheet
        coc_col = "CoC Number"  # Find column that starts with "CoC"
        print(f"current COC sheet: {sheet}")
        if coc_col:  # Ensure column exists
            df_filtered = df[df[coc_col].isin(["CA-600", "NY-600"])]  # Filter rows of interest

            # Select only the needed columns, ensuring "CoC Number" is correctly referenced
            cols_to_keep = [coc_col] + [col for col in columns_needed if col in df.columns]
            df_filtered = df_filtered[cols_to_keep]

            data[sheet] = df_filtered

    return data


def grab_PIT_Data():
    # CoC Number, CoC Name, Overall Homeless, Sheltered ES Homeless, Sheltered TH Homeless, Sheltered Total Homeless,
    # Unsheltered Homeless
    excel_file = "Data/2007-2024-PIT-Counts-by-CoC.xlsb"
    sheets = [sheet for sheet in pd.ExcelFile(excel_file).sheet_names if
              sheet.isdigit() and int(sheet) in range(2014, 2025)]
    data = {}
    columns_needed = ["CoC Number", "Overall Homeless", "Sheltered ES Homeless", "Sheltered TH Homeless",
                      "Sheltered Total Homeless"]
    for sheet in sheets:
        df = pd.read_excel(excel_file, sheet_name=sheet, header=0)
        print(f"current PIT sheet: {sheet}")
        df_filtered = df[df["CoC Number"].isin(["CA-600", "NY-600"])]  # Filter rows of interest

        # Select only the needed columns, ensuring "CoC Number" is correctly referenced
        cols_to_keep = [col for col in columns_needed if col in df.columns]
        df_filtered = df_filtered[cols_to_keep]

        data[sheet] = df_filtered  # Store filtered data by sheet name
    return data


def save_data(data, filename="PIT_Data.pkl"):
    with open("Data/"+filename, "wb") as f:
        pickle.dump(data, f)


def combine_data(data):
    df_list = []

    for year, df in data.items():
        df["Year"] = int(year)  # Add a 'Year' column to indicate the source sheet
        df_list.append(df)

    return pd.concat(df_list, ignore_index=True)  # Merge all DataFrames

'''
HIC_data = grab_HIC_Data()
HIC_combined = combine_data(HIC_data)
pd.set_option('display.max_columns', None)
print(HIC_combined.head())
save_data(HIC_combined, "HIC_data.pkl")
PIT_data = grab_PIT_Data()
PIT_combined = combine_data(PIT_data)
print(PIT_combined.head())
save_data(PIT_combined, "PIT_data.pkl")
'''


