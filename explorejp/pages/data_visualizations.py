"""Data visualizations page for ExploreJP Streamlit app."""

import streamlit as st
import plotly.express as px
import pandas as pd

from explorejp.config import COLORS
from explorejp.database import (
    get_all_cities,
    get_cities_count_by_region,
    get_cities_count_by_season,
)


def _parse_population(pop_str):
    pop_str = str(pop_str).strip()

    if "Million" in pop_str:
        return float(pop_str.replace(" Million", "")) * 1_000_000

    return float(pop_str.replace(",", ""))


def get_cities_df() -> pd.DataFrame:
    cities_df = pd.DataFrame(get_all_cities())
    cities_df["population_num"] = cities_df["population"].apply(_parse_population)
    return cities_df


def render_population_distribution(cities_df: pd.DataFrame) -> None:
    st.subheader("🏙️ Population Distribution")

    fig = px.bar(
        cities_df.sort_values("population_num"),
        x="population_num",
        y="name",
        orientation="h",
        color="population_num",
        color_continuous_scale="Reds",
        title="Population by City",
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, width='stretch')

    fig = px.pie(
        cities_df,
        values="population_num",
        names="name",
        title="Population Share",
    )
    st.plotly_chart(fig, width='stretch')


def render_cost_of_living(cities_df: pd.DataFrame) -> None:
    st.subheader("💰 Cost of Living")

    cost_counts = cities_df["cost_of_living"].value_counts()
    fig = px.pie(
        values=cost_counts.values,
        names=cost_counts.index,
        color_discrete_sequence=[
            COLORS["burgundy"],
            COLORS["cherry_blossom_pink"],
            COLORS["silver_lake_blue"],
        ],
    )
    st.plotly_chart(fig, width='stretch')

    cost_region = (
        cities_df.groupby(["region", "cost_of_living"]).size().reset_index(name="count")
    )
    fig = px.bar(
        cost_region,
        x="region",
        y="count",
        color="cost_of_living",
        barmode="group",
        color_discrete_map={
            "High": COLORS["burgundy"],
            "Medium": COLORS["cherry_blossom_pink"],
            "Low": COLORS["silver_lake_blue"],
        },
    )
    st.plotly_chart(fig, width='stretch')


def render_regional_overview(cities_df: pd.DataFrame, region_counts: dict[str, int]) -> None:
    st.subheader("🗾 Regional Overview")

    fig = px.treemap(
        cities_df,
        path=["region", "name"],
        values="population_num",
        color="region",
    )
    st.plotly_chart(fig, width='stretch')

    region_df = pd.DataFrame(region_counts.items(), columns=["Region", "Cities"])
    fig = px.bar(
        region_df,
        x="Region",
        y="Cities",
        color="Cities",
        color_continuous_scale="Reds",
    )
    st.plotly_chart(fig, width='stretch')


def render_seasonal_preferences(cities_df: pd.DataFrame, season_counts: dict[str, int]) -> None:
    st.subheader("🌸 Seasonal Preferences")

    season_df = pd.DataFrame(season_counts.items(), columns=["Season", "Cities"])
    fig = px.bar(
        season_df,
        x="Season",
        y="Cities",
        color="Cities",
        color_continuous_scale="Pinkyl",
    )
    st.plotly_chart(fig, width='stretch')

    fig = px.pie(
        season_df,
        values="Cities",
        names="Season",
        color_discrete_sequence=[
            COLORS["burgundy"],
            COLORS["cherry_blossom_pink"],
            COLORS["misty_rose"],
            COLORS["silver_lake_blue"],
        ],
    )
    st.plotly_chart(fig, width='stretch')


def render_city_comparison_chart(city1_data: pd.Series, city2_data: pd.Series, city1: str, city2: str) -> None:
    chart_df = pd.DataFrame(
        {
            "City": [city1, city2],
            "Population": [city1_data["population_num"], city2_data["population_num"]],
        }
    )

    fig = px.bar(
        chart_df,
        x="City",
        y="Population",
        color="City",
        title="Population Comparison",
        color_discrete_map={city1: COLORS["burgundy"], city2: COLORS["cherry_blossom_pink"]},
    )
    st.plotly_chart(fig, width='stretch')


def show():
    cities_df = get_cities_df()
    region_counts = get_cities_count_by_region()
    season_counts = get_cities_count_by_season()

    chart_type = st.selectbox(
        "Select Analytics",
        ["Population Distribution", "Cost of Living"],
        key="city_analytics_type",
    )

    if chart_type == "Population Distribution":
        render_population_distribution(cities_df)
    elif chart_type == "Cost of Living":
        render_cost_of_living(cities_df)
