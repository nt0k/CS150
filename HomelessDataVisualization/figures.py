import pandas as pd
import plotly.graph_objs as go

from HomelessDataVisualization import reusable

# Example: Load data from a pickle file named "PIT_Data.pkl"
HIC_data = reusable.load_pickle_data("HIC_data.pkl")
PIT_data = reusable.load_pickle_data("PIT_Data.pkl")

pd.set_option('display.max_columns', None)

def comparison_visual1(df=PIT_data):
    fig = go.Figure()

    df_la_pop = pd.read_excel("Data/LA_population.xlsx")
    df_ny_pop = pd.read_excel("Data/NY_population.xlsx")

    df_la_pop["Year"] = pd.to_numeric(df_la_pop["Year"])

    # Filter for CA-600 data
    df_ca = df[df["CoC Number"] == "CA-600"].copy()
    # Convert 'Year' to integer (if not already) and sort by Year
    df_ca["Year"] = df_ca["Year"].astype(int)
    df_ca.sort_values("Year", inplace=True)

    # Filter for NY-600 data
    df_ny = df[df["CoC Number"] == "NY-600"].copy()
    # Convert 'Year' to integer (if not already) and sort by Year
    df_ny["Year"] = df_ny["Year"].astype(int)
    df_ny.sort_values("Year", inplace=True)

    # Merge with population data, suffixing overlapping 'Year' column from population df
    # Calculate per capita
    df_ca = df_ca.merge(df_la_pop, on="Year", suffixes=("", "_pop"))
    df_ca["Per Capita Homeless"] = (df_ca["Overall Homeless"] / df_ca["Population"]) * 100000
    df_ny = df_ny.merge(df_ny_pop, on="Year", suffixes=("", "_pop"))
    df_ny["Per Capita Homeless"] = (df_ny["Overall Homeless"] / df_ny["Population"]) * 100000

    df_us_pop = pd.read_excel("Data/US_Population.xlsx")
    df_us_homeless = pd.read_excel("Data/Nationwide_Homeless.xlsx")

    df_us_pop = df_us_pop.merge(df_us_homeless, on="Year", suffixes=("", "_pop"))
    df_us_pop["Per Capita Homeless"] = (df_us_pop["Estimated Homeless Population"] / df_us_pop["Population"]) * 100000


    fig.add_trace(go.Scatter(
        x=df_ca["Year"],
        y=df_ca["Per Capita Homeless"],
        mode="lines+markers",
        name="LA County Per Capita Homeless",
    ))

    fig.add_trace(go.Scatter(
        x=df_ny["Year"],
        y=df_ny["Per Capita Homeless"],
        mode="lines+markers",
        name="NY County Per Capita Homeless",
    ))

    fig.add_trace(go.Scatter(
        x=df_us_pop["Year"],
        y=df_us_pop["Per Capita Homeless"],
        mode="lines+markers",
        name="US Per Capita Homeless",
    ))

    # Update the layout with a title and axis labels
    fig.update_layout(
        title="Per Capita Homeless Comparison",
        template="plotly_white",
        xaxis=dict(
            title="Year",
            showline=True,  # Show axis line
            showgrid=False,
            linecolor="lightgray",  # Color of the axis line
            linewidth=1,
            dtick=1
        ),
        yaxis=dict(
            title="Number of Homeless People Per 100k",
            range=[0, 2050],
            gridcolor="lightgray",
            showgrid=True,
            showline=True,  # Show axis line
            linecolor="lightgray",  # Color of the axis line
            linewidth=1,
        ),
        legend=dict(
            orientation="h",  # Horizontal legend
            x=0.5,  # Center it horizontally
            y=-0.2,  # Move it below the x-axis (negative y)
            xanchor="center",  # Anchor x at the center of the legend
            yanchor="top"  # Anchor y at the top of the legend box
        ),
    )

    return fig


def us_percapita_homeless():
    fig = go.Figure()
    df_us_pop = pd.read_excel("Data/US_Population.xlsx")
    df_us_homeless = pd.read_excel("Data/Nationwide_Homeless.xlsx")

    df_us_pop = df_us_pop.merge(df_us_homeless, on="Year", suffixes=("", "_pop"))
    df_us_pop["Per Capita Homeless"] = (df_us_pop["Estimated Homeless Population"] / df_us_pop["Population"]) * 100000
    print(df_us_pop)


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

us_percapita_homeless()