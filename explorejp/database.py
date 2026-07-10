"""Database module for ExploreJP using SQLite."""

import sqlite3
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent.parent / "database" / "explorejp.db"


def get_connection() -> sqlite3.Connection:
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allow column access by name
    return conn


def init_database() -> None:
    """Initialize the database with the cities table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create cities table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            population TEXT NOT NULL,
            region TEXT NOT NULL,
            best_season TEXT NOT NULL,
            known_for TEXT NOT NULL,
            cost_of_living TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()


def import_csv_to_db() -> None:
    """Import cities from CSV into the database."""
    from explorejp.csv_loader import load_cities_from_csv
    
    # First, clear existing data
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cities")
    conn.commit()
    
    # Load cities from CSV as DataFrame
    df = load_cities_from_csv()
    
    # Insert cities into database
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO cities (id, name, population, region, best_season, known_for, cost_of_living)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            int(row['id']),
            row['name'],
            row['population'],
            row['region'],
            row['best_season'],
            row['known_for'],
            row['cost_of_living']
        ))
    
    conn.commit()
    conn.close()


def get_all_cities() -> list[dict]:
    """Get all cities from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM cities ORDER BY name")
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]


def search_cities(query: str) -> list[dict]:
    """Search cities by name (partial match)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM cities WHERE name LIKE ? ORDER BY name",
        (f"%{query}%",)
    )
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]


def get_cities_by_region(region: str) -> list[dict]:
    """Get cities by region."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM cities WHERE region LIKE ? ORDER BY name",
        (f"%{region}%",)
    )
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]


def get_city_by_id(city_id: int) -> dict | None:
    """Get a city by its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM cities WHERE id = ?", (city_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    return dict(row) if row else None


def get_cities_by_season(season: str) -> list[dict]:
    """Get cities by best season."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM cities WHERE best_season LIKE ? ORDER BY name",
        (f"%{season}%",)
    )
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]


def get_all_regions() -> list[str]:
    """Get all unique regions."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT region FROM cities ORDER BY region")
    rows = cursor.fetchall()
    
    conn.close()
    
    return [row["region"] for row in rows]


def get_all_seasons() -> list[str]:
    """Get all unique seasons (extracted from best_season)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT best_season FROM cities")
    rows = cursor.fetchall()
    
    conn.close()
    
    # Extract season names (e.g., "Spring 🌸" -> "Spring")
    seasons = set()
    for row in rows:
        season = row["best_season"].split()[0]
        seasons.add(season)
    
    return sorted(seasons)
