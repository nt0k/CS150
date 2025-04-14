import pandas as pd
import pdfplumber


def fetch_and_clean_data():
    # Get first data source
    df1 = pd.read_csv("data/fy21-25 encounters.csv")

    # Define fiscal year month order
    month_order = ["OCT", "NOV", "DEC", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP"]

    # Filter for U.S. Border Patrol and Apprehension type
    filtered_df = df1[
        (df1["Component"] == "U.S. Border Patrol") &
        (df1["Encounter Type"] == "Apprehensions")
        ]

    # Group by Fiscal Year and Month, summing encounter counts
    monthly_encounters = (
        filtered_df.groupby(["Fiscal Year", "Month (abbv)"])["Encounter Count"]
        .sum()
        .reset_index()
    )

    # Sort months in fiscal year order
    monthly_encounters["Month (abbv)"] = pd.Categorical(
        monthly_encounters["Month (abbv)"], categories=month_order, ordered=True
    )
    df1 = monthly_encounters.sort_values(["Fiscal Year", "Month (abbv)"])

    # Get second data source
    df2 = pd.read_csv("data/BP_data_fy2000-2020.csv")

    # Specify the month columns (excluding the 'Yearly Total' column)
    month_cols = ["October", "November", "December", "January", "February",
                  "March", "April", "May", "June", "July", "August", "September"]

    # Use pd.melt() to transform the DataFrame
    df2_melted = df2.melt(
        id_vars=["Fiscal Year"],
        value_vars=month_cols,
        var_name="Month (abbv)",
        value_name="Encounter Count"
    )

    # Map full month names to abbreviations to match first CSV's structure
    month_mapping = {
        "January": "JAN", "February": "FEB", "March": "MAR", "April": "APR",
        "May": "MAY", "June": "JUN", "July": "JUL", "August": "AUG",
        "September": "SEP", "October": "OCT", "November": "NOV", "December": "DEC"
    }
    df2_melted["Month (abbv)"] = df2_melted["Month (abbv)"].map(month_mapping)

    # Ensure the 'Fiscal Year' is a string and sort the data by Fiscal Year and month order
    df1["Fiscal Year"] = df1["Fiscal Year"].astype(str)
    df2_melted["Fiscal Year"] = df2_melted["Fiscal Year"].astype(str)
    month_order = ["OCT", "NOV", "DEC", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP"]
    df2_melted["Month (abbv)"] = pd.Categorical(df2_melted["Month (abbv)"], categories=month_order, ordered=True)
    df2_melted = df2_melted.sort_values(["Fiscal Year", "Month (abbv)"])

    combined_df = pd.concat([df1, df2_melted], ignore_index=False, sort=False)

    # Apply the function to create the new Date column.
    combined_df["Date"] = combined_df.apply(get_date, axis=1)

    combined_df = combined_df.sort_values("Date")

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', 50)
    return combined_df


def get_date(row):
    # Created with help from ChatGPT
    # Prompt: Help me to adjust for FY data where the FY begins in Oct
    month_to_num = {
        "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4,
        "MAY": 5, "JUN": 6, "JUL": 7, "AUG": 8,
        "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12
    }
    fy = int(row["Fiscal Year"])
    m = month_to_num[row["Month (abbv)"]]
    # For October, November, and December, subtract 1 from the fiscal year.
    if m >= 10:
        year = fy - 1
    else:
        year = fy
    # Create a date with the first day of the month.
    return pd.to_datetime(f"{year}-{m:02d}-01", format="%Y-%m-%d")


def parsePdf():
    # This was just used to help create BP_data_fy2000-2020 and then not used again
    # I used this to scrape the pdf and then paste the data into the csv with excel
    data = []
    with pdfplumber.open("data/US_BP_2000-2020.pdf") as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if row and "Southwest Border" in row[0]:
                        data.append(row)
    df = pd.DataFrame(data)
    return df
