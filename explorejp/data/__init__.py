"""City data for ExploreJP - ONLY talks to SQLite database."""

from dataclasses import dataclass

import pandas as pd
from explorejp.database import (
    get_all_cities as db_get_all_cities,
    get_all_regions as db_get_all_regions,
    get_all_seasons as db_get_all_seasons,
    get_city_by_id,
    get_cities_by_region as db_get_cities_by_region,
    get_cities_by_season as db_get_cities_by_season,
    search_cities as db_search_cities,
)


@dataclass(frozen=True)
class City:
    name: str
    population: str
    region: str
    best_season: str
    known_for: list[str]
    cost_of_living: str


def get_city(city_id: str) -> City | None:
    """Get a city by its ID using database."""
    city_dict = get_city_by_id(int(city_id))
    if not city_dict:
        return None
    
    known_for = city_dict["known_for"].split("|")
    return City(
        name=city_dict["name"],
        population=city_dict["population"],
        region=city_dict["region"],
        best_season=city_dict["best_season"],
        known_for=known_for,
        cost_of_living=city_dict["cost_of_living"],
    )


def search_cities(query: str) -> list[tuple[str, City]]:
    """Search cities by name (partial match) using database."""
    results = []
    for city_dict in db_search_cities(query):
        city_id = str(city_dict["id"])
        known_for = city_dict["known_for"].split("|")
        city = City(
            name=city_dict["name"],
            population=city_dict["population"],
            region=city_dict["region"],
            best_season=city_dict["best_season"],
            known_for=known_for,
            cost_of_living=city_dict["cost_of_living"],
        )
        results.append((city_id, city))
    return results


def get_cities_by_region(region: str) -> list[tuple[str, City]]:
    """Get cities by region using database."""
    results = []
    for city_dict in db_get_cities_by_region(region):
        city_id = str(city_dict["id"])
        known_for = city_dict["known_for"].split("|")
        city = City(
            name=city_dict["name"],
            population=city_dict["population"],
            region=city_dict["region"],
            best_season=city_dict["best_season"],
            known_for=known_for,
            cost_of_living=city_dict["cost_of_living"],
        )
        results.append((city_id, city))
    return results


def get_all_regions() -> list[str]:
    """Get all unique regions using database."""
    return db_get_all_regions()


def get_cities_by_season(season: str) -> list[tuple[str, City]]:
    """Get cities by season using database."""
    results = []
    for city_dict in db_get_cities_by_season(season):
        city_id = str(city_dict["id"])
        known_for = city_dict["known_for"].split("|")
        city = City(
            name=city_dict["name"],
            population=city_dict["population"],
            region=city_dict["region"],
            best_season=city_dict["best_season"],
            known_for=known_for,
            cost_of_living=city_dict["cost_of_living"],
        )
        results.append((city_id, city))
    return results


def get_all_seasons() -> list[str]:
    """Get all unique seasons using database."""
    return db_get_all_seasons()


def get_all_cities() -> dict[str, City]:
    """Get all cities from database as dict of City objects."""
    cities = {}
    for city_dict in db_get_all_cities():
        city_id = str(city_dict["id"])
        known_for = city_dict["known_for"].split("|")
        cities[city_id] = City(
            name=city_dict["name"],
            population=city_dict["population"],
            region=city_dict["region"],
            best_season=city_dict["best_season"],
            known_for=known_for,
            cost_of_living=city_dict["cost_of_living"],
        )
    return cities


def get_regional_statistics() -> dict[str, dict[str, str]]:
    """Calculate regional statistics using database and pandas."""
    from explorejp.database import get_all_cities as db_get_all_cities
    
    cities_data = db_get_all_cities()
    
    # Convert to pandas DataFrame
    df = pd.DataFrame(cities_data)
    
    # Convert population to numeric (handle both "X Million" and "360,000" formats)
    def parse_population(pop_str: str) -> float:
        pop_str = str(pop_str).strip()
        if 'Million' in pop_str:
            return float(pop_str.replace(' Million', '').strip()) * 1_000_000
        else:
            # Remove commas and convert to float
            return float(pop_str.replace(',', '').strip())
    
    df['population_num'] = df['population'].apply(parse_population)
    
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
