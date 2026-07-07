"""City data for ExploreJP."""

import csv
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class City:
    name: str
    population: str
    region: str
    best_season: str
    known_for: list[str]
    cost_of_living: str


def load_cities_from_csv() -> dict[str, City]:
    """Load city data from CSV file."""
    csv_path = Path(__file__).parent.parent.parent / "data" / "cities.csv"
    cities = {}
    
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            city_id = row["id"]
            known_for = row["known_for"].split("|")
            cities[city_id] = City(
                name=row["name"],
                population=row["population"],
                region=row["region"],
                best_season=row["best_season"],
                known_for=known_for,
                cost_of_living=row["cost_of_living"],
            )
    
    return cities


def get_city(city_id: str) -> City | None:
    """Load CSV and return a specific city by ID."""
    cities = load_cities_from_csv()
    return cities.get(city_id)


def search_cities(query: str) -> list[tuple[str, City]]:
    """Load CSV and search cities by name (case-insensitive partial match)."""
    cities = load_cities_from_csv()
    query_lower = query.lower()
    results = []
    
    for city_id, city in cities.items():
        if query_lower in city.name.lower():
            results.append((city_id, city))
    
    return results


def get_cities_by_region(region: str) -> list[tuple[str, City]]:
    """Load CSV and return cities in a specific region."""
    cities = load_cities_from_csv()
    results = []
    
    for city_id, city in cities.items():
        if city.region.lower() == region.lower():
            results.append((city_id, city))
    
    return results


def get_all_regions() -> list[str]:
    """Load CSV and return list of unique regions."""
    cities = load_cities_from_csv()
    regions = set()
    
    for city in cities.values():
        regions.add(city.region)
    
    return sorted(regions)


def get_cities_by_season(season: str) -> list[tuple[str, City]]:
    """Load CSV and return cities with a specific best season."""
    cities = load_cities_from_csv()
    results = []
    
    for city_id, city in cities.items():
        if season.lower() in city.best_season.lower():
            results.append((city_id, city))
    
    return results


def get_all_seasons() -> list[str]:
    """Load CSV and return list of unique seasons."""
    cities = load_cities_from_csv()
    seasons = set()
    
    for city in cities.values():
        # Extract season from best_season (e.g., "Spring 🌸" -> "Spring")
        season = city.best_season.split()[0]
        seasons.add(season)
    
    return sorted(seasons)


def get_regional_statistics() -> dict[str, dict[str, str]]:
    """Load CSV and calculate regional statistics using pandas."""
    csv_path = Path(__file__).parent.parent.parent / "data" / "cities.csv"
    df = pd.read_csv(csv_path)
    
    # Convert population to numeric (remove " Million" and convert)
    df['population_num'] = df['population'].str.replace(' Million', '').astype(float) * 1_000_000
    
    # Group by region and calculate statistics
    stats = df.groupby('region').agg({
        'name': 'count',
        'population_num': 'sum'
    }).reset_index()
    
    # Format results
    result = {}
    for _, row in stats.iterrows():
        region = row['region']
        city_count = int(row['name'])
        total_pop = int(row['population_num'])
        
        # Format population with commas
        pop_str = f"{total_pop:,}"
        
        result[region] = {
            'cities': city_count,
            'population': pop_str
        }
    
    return result
