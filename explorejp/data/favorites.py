"""Favorites management for ExploreJP - uses SQLite database."""

from explorejp.database import (
    add_favorite as db_add_favorite,
    get_favorites as db_get_favorites,
    get_favorite_city_ids,
    is_favorite as db_is_favorite,
    remove_favorite as db_remove_favorite,
)


def add_favorite(city_id: str) -> bool:
    """Add a city to favorites. Returns True if added, False if already exists."""
    return db_add_favorite(int(city_id))


def remove_favorite(city_id: str) -> bool:
    """Remove a city from favorites. Returns True if removed, False if not found."""
    return db_remove_favorite(int(city_id))


def is_favorite(city_id: str) -> bool:
    """Check if a city is in favorites."""
    return db_is_favorite(int(city_id))


def get_favorites() -> list[dict]:
    """Get all favorite cities with their details."""
    return db_get_favorites()


def load_favorites() -> list[str]:
    """Load all favorite city IDs as strings for legacy callers."""
    return [str(cid) for cid in get_favorite_city_ids()]


def get_favorite_ids() -> list[str]:
    """Get list of favorite city IDs as strings."""
    return [str(cid) for cid in get_favorite_city_ids()]
