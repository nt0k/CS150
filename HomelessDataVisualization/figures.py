import pandas as pd
import plotly.graph_objs as go
from matplotlib.typing import RGBColorType

from HomelessDataVisualization import reusable

# Example: Load data from a pickle file named "PIT_Data.pkl"
HIC_data = reusable.load_pickle_data("HIC_data.pkl")
PIT_data = reusable.load_pickle_data("PIT_Data.pkl")

pd.set_option('display.max_columns', None)


def add_scatter(fig, df, x_col, y_col, name, color, width=4, textposition=None):
    mode = "lines+markers" + ("+text" if textposition else "")
    trace_args = {
        "x": df[x_col],
        "y": round(df[y_col], 0),  # Round the y values here
        "mode": mode,
        "hoverinfo": "x+y",
        "name": name,
        "line": dict(color=color, width=width),
        "marker": dict(color=color)
    }
    if textposition:
        trace_args["textposition"] = textposition
    fig.add_trace(go.Scatter(**trace_args))


def add_bar(fig, x_vals, y_vals, name, color):
    fig.add_trace(go.Bar(
        x=x_vals,
        y=round(y_vals, 0),  # Round the y values here
        hoverinfo="x+y",
        name=name,
        marker_color=color
    ))


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
    df_ca["Per Capita Homeless"] = round((df_ca["Overall Homeless"] / df_ca["Population"]) * 100000, 0)
    df_ny = df_ny.merge(df_ny_pop, on="Year", suffixes=("", "_pop"))
    df_ny["Per Capita Homeless"] = round((df_ny["Overall Homeless"] / df_ny["Population"]) * 100000, 0)

    df_us_pop = pd.read_excel("Data/US_Population.xlsx")
    df_us_homeless = pd.read_excel("Data/Nationwide_Homeless.xlsx")

    # Merge and calculate per capita
    df_us_pop = df_us_pop.merge(df_us_homeless, on="Year", suffixes=("", "_pop"))
    df_us_pop["Per Capita Homeless"] = round(
        (df_us_pop["Estimated Homeless Population"] / df_us_pop["Population"]) * 100000, 0)
    add_scatter(fig, df_ny, "Year", "Per Capita Homeless", "NY County", "rgb(32,72,88)", width=4)
    add_scatter(fig, df_ca, "Year", "Per Capita Homeless", "LA County", "rgb(232,183,78)", width=4)
    add_scatter(fig, df_us_pop, "Year", "Per Capita Homeless", "United States", "black", width=4,
                textposition="top center")

    base_style = {
        "xref": "x",
        "yref": "y",
        "showarrow": True,
        "arrowhead": 2,
        "font": dict(size=12, color="black"),
        "bgcolor": "white",
        "bordercolor": "white",
        "borderwidth": 0.5
    }

    # Update the layout with a title and axis labels
    fig.update_layout(
        title="LA and NY Outpace Nation in Homeless Population Growth",
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
            title="Homeless People Per Capita",
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
            {**base_style, "x": "2021", "y": 830,
             "text": "Drop due to decrease in reporting during Pandemic", "ax": -20, "ay": -50},
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

    df_la_pop = pd.read_excel("Data/LA_population.xlsx")
    df_ny_pop = pd.read_excel("Data/NY_population.xlsx")
    # Merge population data and calculate per capita for chosen segment
    df_ca = df_ca.merge(df_la_pop, on="Year")
    df_ca[f"{segment} Per Capita"] = round((df_ca[segment] / df_ca["Population"]) * 100000, 0)

    df_ny = df_ny.merge(df_ny_pop, on="Year")
    df_ny[f"{segment} Per Capita"] = round((df_ny[segment] / df_ny["Population"]) * 100000, 0)

    # Create a figure for a line chart
    fig = go.Figure()
    add_scatter(fig, df_ny, "Year", f"{segment} Per Capita", f"NY City County", "rgb(32,72,88)", width=4)
    add_scatter(fig, df_ca, "Year", f"{segment} Per Capita", f"LA County", "rgb(232,183,78)", width=4)
    # Update the layout with a title and axis labels
    fig.update_layout(
        title="NY County's Resources Dwarf LA's",
        xaxis_title="Year",
        template="plotly_white",
        legend=dict(
            orientation="h",
            x=0.5,
            y=-0.2,
            xanchor="center",
            yanchor="top"
        ),
        yaxis=dict(
            title="Beds Per 100,000 People",
            range=[0, None],
            gridcolor="lightgray",
            showgrid=True,
            showline=True,  # Show axis line
            linecolor="lightgray",  # Color of the axis line
            linewidth=1,
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
    df_ca["Unsheltered Homeless"] = round(df_ca["Overall Homeless"] - df_ca["Sheltered Total Homeless"], 0)
    df_ny["Unsheltered Homeless"] = round(df_ny["Overall Homeless"] - df_ny["Sheltered Total Homeless"], 0)

    # Add LA and NY data to grouped stacked bar chart with composite x-axis
    add_bar(fig, ["2024 LA"], df_ca["Sheltered Total Homeless"], "LA Sheltered", "rgb(232,183,78)")
    add_bar(fig, ["2024 LA"], df_ca["Unsheltered Homeless"], "LA Unsheltered", "rgb(255,221,157)")
    add_bar(fig, ["2024 NY"], df_ny["Sheltered Total Homeless"], "NY Sheltered", "rgb(32,72,88)")
    add_bar(fig, ["2024 NY"], df_ny["Unsheltered Homeless"], "NY Unsheltered", "rgb(169,194,206)")

    # Update layout
    fig.update_layout(
        barmode='stack',
        title="NY City County Shelters 96% of its Homeless Population",
        xaxis_title="Year",
        yaxis_title="Number of Homeless Individuals",
        template="plotly_white",
        legend=dict(
            orientation="h",
            x=0.5,
            y=-0.2,
            xanchor="center",
            yanchor="top",
            traceorder="normal"
        )
    )
    return fig


def death_graph():
    df_la = pd.read_excel("Data/LA_homeless_deaths.xlsx")
    df_ny = pd.read_excel("Data/NY_homeless_deaths.xlsx")

    fig = go.Figure()

    add_bar(fig, df_la["Year"], round(df_la["Mortality Rate"], 0), "LA County", "rgb(232,183,78)")
    add_bar(fig, df_ny["Year"], round(df_ny["Mortality Rate"], 0), "NY City County", "rgb(32,72,88)")

    fig.update_layout(
        # barmode='stack',
        title="LA County's Death Rate is 3 times higher than New York's",
        xaxis=dict(
            title="Year",
            tickmode='linear',  # Ensure all values are shown
            dtick=1,  # Set the interval between ticks to 1 year
            showline=True,
            showgrid=False,
            linecolor="lightgray",
            linewidth=1,
        ),
        yaxis_title="Deaths per 100,000 Homeless",
        template="plotly_white",
        legend=dict(
            orientation="h",
            x=0.5,
            y=-0.2,
            xanchor="center",
            yanchor="top",
            traceorder="normal"
        )
    )
    return fig


def projection_graph(shelter_percent):
    # Linear model coefficients from earlier: mortality = a * unsheltered_rate + b
    a = 2902.26
    b = 221.94

    # LA baseline stats
    la_total = 71201
    la_current_sheltered = 21692
    la_current_mortality = 2240

    shelter_rate = shelter_percent / 100
    unsheltered_rate = 1 - shelter_rate

    projected_mortality = round((a * unsheltered_rate + b), 0)
    lives_lost_per_100k = la_current_mortality - projected_mortality
    estimated_lives_saved = (lives_lost_per_100k / 100_000) * la_total

    text_output = (
        f"At a shelter rate of {shelter_percent}%, "
        f"an estimated {estimated_lives_saved:.0f} fewer people would die."
    )

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Projected Death Rate", "Current Death Rate"],
        y=[projected_mortality, la_current_mortality],
        marker_color=["rgb(255,221,157)", "rgb(232,183,78)"],
        name="Mortality Rate"
    ))

    fig.update_layout(
        xaxis_title="Scenario",
        yaxis_title="Deaths per 100,000 Homeless",
        title="Building More Shelters Saves Hundreds of Lives",
        template="plotly_white",
        yaxis=dict(range=[0, 2500]),
    )

    return text_output, fig
