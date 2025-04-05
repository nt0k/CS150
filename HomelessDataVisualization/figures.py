import pandas as pd
import plotly.graph_objs as go

from HomelessDataVisualization import reusable

# Example: Load data from a pickle file named "PIT_Data.pkl"
HIC_data = reusable.load_pickle_data("HIC_data.pkl")
PIT_data = reusable.load_pickle_data("PIT_Data.pkl")

pd.set_option('display.max_columns', None)
print(PIT_data.head())

def comparison_visual1(df=PIT_data):
    fig = go.Figure()

    # Filter for CA-600 data
    df_ca = df[df["CoC Number"] == "CA-600"].copy()
    # Convert 'Year' to integer (if not already) and sort by Year
    df_ca["Year"] = df_ca["Year"].astype(int)
    df_ca.sort_values("Year", inplace=True)

    # Filter for NY-600 data
    df_ny = df[df["CoC Number"] == "NY-600"].copy()
    # Convert 'Year' to integer (if not already) and sort by Year
    df_ca["Year"] = df_ca["Year"].astype(int)
    df_ca.sort_values("Year", inplace=True)

    fig.add_trace(go.Scatter(
        x=df_ca["Year"],
        y=df_ca["Overall Homeless"],
        mode="lines+markers",
        name="CA Overall Homeless",
    ))

    fig.add_trace(go.Scatter(
        x=df_ny["Year"],
        y=df_ny["Overall Homeless"],
        mode="lines+markers",
        name="NY Overall Homeless",
    ))

    # Update the layout with a title and axis labels
    fig.update_layout(
        title="LA vs NY Overall Homeless",
        xaxis_title="Year",
        yaxis_title="Number of Homeless People",
        template="plotly_white"
    )

    return fig


def ca_visual_1(df=HIC_data):
    # Filter for CA-600 data
    df_ca = df[df["CoC Number"] == "CA-600"].copy()
    # Convert 'Year' to integer (if not already) and sort by Year
    df_ca["Year"] = df_ca["Year"].astype(int)
    df_ca.sort_values("Year", inplace=True)

    # Create a figure for a line chart
    fig = go.Figure()

    # Add a line trace for Total Year-Round Beds (ES, TH, SH)
    fig.add_trace(go.Scatter(
        x=df_ca["Year"],
        y=df_ca["Total Year-Round Beds (ES, TH, SH)"],
        mode="lines+markers",
        name="Beds (ES, TH, SH)"
    ))

    # Add a line trace for Total Year-Round Beds (RRH)
    fig.add_trace(go.Scatter(
        x=df_ca["Year"],
        y=df_ca["Total Year-Round Beds (RRH)"],
        mode="lines+markers",
        name="Beds (RRH)"
    ))

    # Add a line trace for Total Year-Round Beds (PSH)
    fig.add_trace(go.Scatter(
        x=df_ca["Year"],
        y=df_ca["Total Year-Round Beds (PSH)"],
        mode="lines+markers",
        name="Beds (PSH)"
    ))

    # Add a line trace for Total Year-Round Beds (OPH)
    fig.add_trace(go.Scatter(
        x=df_ca["Year"],
        y=df_ca["Total Year-Round Beds (OPH)"],
        mode="lines+markers",
        name="Beds (OPH)"
    ))

    # Update the layout with a title and axis labels
    fig.update_layout(
        title="LA CoC Beds Over Time",
        xaxis_title="Year",
        yaxis_title="Number of Beds",
        template="plotly_white"
    )

    return fig

def ny_visual_1(df=HIC_data):
    # Filter for NY-600 data
    df_ca = df[df["CoC Number"] == "NY-600"].copy()
    # Convert 'Year' to integer (if not already) and sort by Year
    df_ca["Year"] = df_ca["Year"].astype(int)
    df_ca.sort_values("Year", inplace=True)

    # Create a figure for a line chart
    fig = go.Figure()

    # Add a line trace for Total Year-Round Beds (ES, TH, SH)
    fig.add_trace(go.Scatter(
        x=df_ca["Year"],
        y=df_ca["Total Year-Round Beds (ES, TH, SH)"],
        mode="lines+markers",
        name="Beds (ES, TH, SH)"
    ))

    # Add a line trace for Total Year-Round Beds (RRH)
    fig.add_trace(go.Scatter(
        x=df_ca["Year"],
        y=df_ca["Total Year-Round Beds (RRH)"],
        mode="lines+markers",
        name="Beds (RRH)"
    ))

    # Add a line trace for Total Year-Round Beds (PSH)
    fig.add_trace(go.Scatter(
        x=df_ca["Year"],
        y=df_ca["Total Year-Round Beds (PSH)"],
        mode="lines+markers",
        name="Beds (PSH)"
    ))

    # Add a line trace for Total Year-Round Beds (OPH)
    fig.add_trace(go.Scatter(
        x=df_ca["Year"],
        y=df_ca["Total Year-Round Beds (OPH)"],
        mode="lines+markers",
        name="Beds (OPH)"
    ))

    # Update the layout with a title and axis labels
    fig.update_layout(
        title="NY City CoC Beds Over Time",
        xaxis_title="Year",
        yaxis_title="Number of Beds",
        template="plotly_white"
    )

    return fig