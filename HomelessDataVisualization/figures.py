import pandas as pd
import plotly.graph_objs as go
from matplotlib.typing import RGBColorType

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

    fig.add_trace(go.Scatter(
        x=df_ca["Year"],
        y=df_ca["Per Capita Homeless"],
        mode="lines+markers",
        name="LA County Per Capita Homeless",
        line=dict(color="rgb(232,183,78)"),
        marker=dict(color="rgb(232,183,78)")
    ))

    fig.add_trace(go.Scatter(
        x=df_ny["Year"],
        y=df_ny["Per Capita Homeless"],
        mode="lines+markers",
        name="NY County Per Capita Homeless",
        line=dict(color="rgb(32,72,88)"),
        marker=dict(color="rgb(32,72,88)")
    ))

    base_style = {
        "xref": "x",
        "yref": "y",
        "showarrow": True,
        "arrowhead": 2,
        "font": dict(size=12, color="black"),
        "bgcolor": "white",
        "bordercolor": "lightgray",
        "borderwidth": 0.5
    }

    # Update the layout with a title and axis labels
    fig.update_layout(
        title="Recent Increase in Homelessness Diverges from Previous Plateau",
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
        annotations=[
            {**base_style, "x": "2021", "y": 190,
             "text": "Drop due to decrease in reporting during Pandemic", "ax": -10, "ay": -150},
        ]
    )

    return fig


def us_percapita_homeless():
    fig = go.Figure()
    df_us_pop = pd.read_excel("Data/US_Population.xlsx")
    df_us_homeless = pd.read_excel("Data/Nationwide_Homeless.xlsx")

    # Merge and calculate per capita
    df_us_pop = df_us_pop.merge(df_us_homeless, on="Year", suffixes=("", "_pop"))
    df_us_pop["Per Capita Homeless"] = (df_us_pop["Estimated Homeless Population"] / df_us_pop["Population"]) * 100000

    # Get first and last year only
    df_slope = df_us_pop[df_us_pop["Year"].isin([df_us_pop["Year"].min(), df_us_pop["Year"].max()])]

    # Add slope line
    fig.add_trace(go.Scatter(
        x=df_slope["Year"],
        y=df_slope["Per Capita Homeless"],
        mode="lines+markers+text",
        name="US Per Capita Homeless",
        textposition="top center",
        line=dict(color="black"),
        marker=dict(color="black")
    ))

    base_style = {
        "xref": "x",
        "yref": "y",
        "showarrow": False,
        "arrowhead": 2,
        "font": dict(size=12, color="black"),
        "bgcolor": "white",
        "bordercolor": "gray",
        "borderwidth": 0.5
    }

    fig.update_layout(
        title="USA Homeless Population Per Capita",
        template="plotly_white",
        xaxis=dict(
            title="Year",
            tickvals=[2014, 2024],
            showline=True,
            showgrid=False,
            linecolor="lightgray",
            linewidth=1,
            dtick=1
        ),
        yaxis=dict(
            title="Homeless per 100k People",
            range=[0, df_slope["Per Capita Homeless"].max() * 1.25],
            gridcolor="lightgray",
            showgrid=True,
            showline=True,
            linecolor="lightgray",
            linewidth=1,
        ),
        legend=dict(
            orientation="h",  # Horizontal legend
            x=0.5,  # Center it horizontally
            y=-0.2,  # Move it below the x-axis (negative y)
            xanchor="center",  # Anchor x at the center of the legend
            yanchor="top"  # Anchor y at the top of the legend box
        ),
        annotations=[
            {**base_style, "x": "2019", "y": 125,
             "text": "25% increase over the last decade.", "ax": 0, "ay": 0},
        ]
    )

    return fig


def shelter_comparison(segment):
    df = HIC_data

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

    # Create a figure for a line chart
    fig = go.Figure()

    # Add a line trace for Total Year-Round Beds (ES, TH, SH)
    fig.add_trace(go.Scatter(
        x=df_ca["Year"],
        y=df_ca[segment],
        mode="lines+markers",
        name=f"LA {segment}",
        line=dict(color="rgb(232,183,78)"),
        marker=dict(color="rgb(232,183,78)")
    ))

    # Add a line trace for Total Year-Round Beds (RRH)
    fig.add_trace(go.Scatter(
        x=df_ny["Year"],
        y=df_ny[segment],
        mode="lines+markers",
        name=f"NY {segment}",
        line=dict(color="rgb(32,72,88)"),
        marker=dict(color="rgb(32,72,88)")
    ))

    # Update the layout with a title and axis labels
    fig.update_layout(
        title="LA vs NY Shelter Segment Comparison",
        xaxis_title="Year",
        yaxis_title="Number of Beds",
        template="plotly_white",
        legend=dict(
            orientation="h",  # Horizontal legend
            x=0.5,  # Center it horizontally
            y=-0.2,  # Move it below the x-axis (negative y)
            xanchor="center",  # Anchor x at the center of the legend
            yanchor="top"  # Anchor y at the top of the legend box
        ),
    )

    return fig

def stack_bargraph1():
    fig = go.Figure()
    df = PIT_data

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
    df_ca = df_ca[df_ca["Year"] == 2024]
    df_ny = df_ny[df_ny["Year"] == 2024]

    # Calculate Unsheltered Homeless
    df_ca["Unsheltered Homeless"] = df_ca["Overall Homeless"] - df_ca["Sheltered Total Homeless"]
    df_ny["Unsheltered Homeless"] = df_ny["Overall Homeless"] - df_ny["Sheltered Total Homeless"]


    # Add LA and NY data to grouped stacked bar chart with composite x-axis
    fig.add_trace(go.Bar(
        x=["2024 LA"],
        y=df_ca["Sheltered Total Homeless"],
        name="LA Sheltered",
        marker_color="rgb(232,183,78)"
    ))

    fig.add_trace(go.Bar(
        x=["2024 LA"],
        y=df_ca["Unsheltered Homeless"],
        name="LA Unsheltered",
        marker_color="rgb(255,221,157)"
    ))

    fig.add_trace(go.Bar(
        x=["2024 NY"],
        y=df_ny["Sheltered Total Homeless"],
        name="NY Sheltered",
        marker_color="rgb(32,72,88)",
    ))

    fig.add_trace(go.Bar(
        x=["2024 NY"],
        y=df_ny["Unsheltered Homeless"],
        name="NY Unsheltered",
        marker_color="rgb(169,194,206)"
    ))

    # Update layout
    fig.update_layout(
        barmode='stack',
        title="Sheltered vs Unsheltered Homeless: LA vs NY",
        xaxis_title="Year",
        yaxis_title="Number of Homeless Individuals",
        template="plotly_white",
        legend=dict(
            orientation="h",
            x=0.5,
            y=-0.2,
            xanchor="center",
            yanchor="top"
        )
    )
    return fig

