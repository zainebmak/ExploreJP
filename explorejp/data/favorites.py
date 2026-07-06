"""Favorites management for ExploreJP."""

import json
from pathlib import Path


def _get_favorites_path() -> Path:
    """Get the path to the favorites JSON file."""
    return Path(__file__).parent.parent.parent / "data" / "favorites.json"


def load_favorites() -> set[str]:
    """Load favorite city IDs from JSON file."""
    favorites_path = _get_favorites_path()
    
    if not favorites_path.exists():
        return set()
    
    with open(favorites_path, encoding="utf-8") as f:
        data = json.load(f)
        return set(data.get("favorites", []))


def save_favorites(favorites: set[str]) -> None:
    """Save favorite city IDs to JSON file."""
    favorites_path = _get_favorites_path()
    favorites_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(favorites_path, "w", encoding="utf-8") as f:
        json.dump({"favorites": sorted(favorites)}, f, indent=2)


def add_favorite(city_id: str) -> bool:
    """Add a city to favorites. Returns True if added, False if already exists."""
    favorites = load_favorites()
    
    if city_id in favorites:
        return False
    
    favorites.add(city_id)
    save_favorites(favorites)
    return True


def remove_favorite(city_id: str) -> bool:
    """Remove a city from favorites. Returns True if removed, False if not found."""
    favorites = load_favorites()
    
    if city_id not in favorites:
        return False
    
    favorites.remove(city_id)
    save_favorites(favorites)
    return True


def is_favorite(city_id: str) -> bool:
    """Check if a city is in favorites."""
    favorites = load_favorites()
    return city_id in favorites
