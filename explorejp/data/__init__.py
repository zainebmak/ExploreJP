"""City data for ExploreJP."""

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class City:
    name: str
    population: str
    region: str
    best_season: str
    known_for: list[str]


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
