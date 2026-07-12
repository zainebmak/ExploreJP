"""Data visualization functions for ExploreJP."""

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_population_by_city_data() -> list[tuple[str, float, str]]:
    """Get population data for all cities sorted by population."""
    csv_path = Path(__file__).parent.parent.parent / "data" / "cities.csv"
    df = pd.read_csv(csv_path)
    
    # Convert population to numeric (handle both "X Million" and "360,000" formats)
    def parse_population(pop_str: str) -> float:
        pop_str = str(pop_str).strip()
        if 'Million' in pop_str:
            return float(pop_str.replace(' Million', '').strip()) * 1_000_000
        else:
            # Remove commas and convert to float
            return float(pop_str.replace(',', '').strip())
    
    df['population_num'] = df['population'].apply(parse_population)
    
    # Sort by population descending
    df_sorted = df.sort_values('population_num', ascending=False)
    
    return [
        (row['name'], row['population_num'], row['population'])
        for _, row in df_sorted.iterrows()
    ]


def get_cities_by_region_data() -> dict[str, int]:
    """Get count of cities per region."""
    csv_path = Path(__file__).parent.parent.parent / "data" / "cities.csv"
    df = pd.read_csv(csv_path)
    
    region_counts = df['region'].value_counts().to_dict()
    return region_counts


def get_top_5_cities_data() -> list[tuple[str, float, str]]:
    """Get top 5 most populated cities."""
    csv_path = Path(__file__).parent.parent.parent / "data" / "cities.csv"
    df = pd.read_csv(csv_path)
    
    # Convert population to numeric (handle both "X Million" and "360,000" formats)
    def parse_population(pop_str: str) -> float:
        pop_str = str(pop_str).strip()
        if 'Million' in pop_str:
            return float(pop_str.replace(' Million', '').strip()) * 1_000_000
        else:
            # Remove commas and convert to float
            return float(pop_str.replace(',', '').strip())
    
    df['population_num'] = df['population'].apply(parse_population)
    
    # Sort and get top 5
    df_sorted = df.sort_values('population_num', ascending=False).head(5)
    
    return [
        (row['name'], row['population_num'], row['population'])
        for _, row in df_sorted.iterrows()
    ]


def get_population_by_region_data() -> dict[str, float]:
    """Get total population per region."""
    csv_path = Path(__file__).parent.parent.parent / "data" / "cities.csv"
    df = pd.read_csv(csv_path)
    
    # Convert population to numeric (handle both "X Million" and "360,000" formats)
    def parse_population(pop_str: str) -> float:
        pop_str = str(pop_str).strip()
        if 'Million' in pop_str:
            return float(pop_str.replace(' Million', '').strip()) * 1_000_000
        else:
            # Remove commas and convert to float
            return float(pop_str.replace(',', '').strip())
    
    df['population_num'] = df['population'].apply(parse_population)
    
    # Group by region and sum
    region_pop = df.groupby('region')['population_num'].sum().to_dict()
    return region_pop


def create_population_bar_chart_html() -> str:
    """Create HTML bar chart for population by city using plotly."""
    data = get_population_by_city_data()
    
    cities = [item[0] for item in data]
    populations = [item[1] for item in data]
    
    fig = px.bar(
        x=cities,
        y=populations,
        title="Population by City",
        labels={"x": "City", "y": "Population"},
        color=populations,
        color_continuous_scale="Viridis"
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=600,
        width=1000
    )
    
    return fig.to_html()


def create_region_pie_chart_html() -> str:
    """Create HTML pie chart for cities by region using plotly."""
    data = get_cities_by_region_data()
    
    fig = px.pie(
        values=list(data.values()),
        names=list(data.keys()),
        title="Cities by Region",
        hole=0.3
    )
    
    fig.update_layout(height=600, width=800)
    
    return fig.to_html()


def create_top_5_chart_html() -> str:
    """Create HTML bar chart for top 5 most populated cities using plotly."""
    data = get_top_5_cities_data()
    
    cities = [item[0] for item in data]
    populations = [item[1] for item in data]
    
    fig = px.bar(
        x=cities,
        y=populations,
        title="Top 5 Most Populated Cities",
        labels={"x": "City", "y": "Population"},
        color=populations,
        color_continuous_scale="Reds"
    )
    
    fig.update_layout(height=600, width=1000)
    
    return fig.to_html()


def create_population_by_region_chart_html() -> str:
    """Create HTML bar chart for population by region using plotly."""
    data = get_population_by_region_data()
    
    regions = list(data.keys())
    populations = list(data.values())
    
    fig = px.bar(
        x=regions,
        y=populations,
        title="Population by Region",
        labels={"x": "Region", "y": "Total Population"},
        color=populations,
        color_continuous_scale="Blues"
    )
    
    fig.update_layout(height=600, width=1000)
    
    return fig.to_html()


def save_chart_html(html_content: str, filename: str) -> str:
    """Save chart HTML to file and return the file path."""
    output_dir = Path(__file__).parent.parent.parent / "charts"
    output_dir.mkdir(exist_ok=True)
    
    output_path = output_dir / filename
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return str(output_path)
