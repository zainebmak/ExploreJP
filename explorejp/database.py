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
    """Initialize the database with the cities and favorites tables."""
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
    
    # Create favorites table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            city_id INTEGER PRIMARY KEY,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create itineraries table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itineraries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            season TEXT NOT NULL,
            interests TEXT NOT NULL,
            budget REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create itinerary_cities table (junction table for many-to-many)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itinerary_cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            itinerary_id INTEGER NOT NULL,
            city_id INTEGER NOT NULL,
            day_number INTEGER NOT NULL,
            notes TEXT,
            FOREIGN KEY (itinerary_id) REFERENCES itineraries(id) ON DELETE CASCADE,
            FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
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


# Favorites functions
def add_favorite(city_id: int) -> bool:
    """Add a city to favorites. Returns True if added, False if already exists."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO favorites (city_id) VALUES (?)", (city_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # City already in favorites
        conn.close()
        return False


def remove_favorite(city_id: int) -> bool:
    """Remove a city from favorites. Returns True if removed, False if not found."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM favorites WHERE city_id = ?", (city_id,))
    rows_affected = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    return rows_affected > 0


def is_favorite(city_id: int) -> bool:
    """Check if a city is in favorites."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT 1 FROM favorites WHERE city_id = ?", (city_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    return result is not None


def get_favorites() -> list[dict]:
    """Get all favorite cities with their details."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT c.* FROM cities c
        JOIN favorites f ON c.id = f.city_id
        ORDER BY f.added_at DESC
    """)
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]


def get_favorite_city_ids() -> list[int]:
    """Get list of favorite city IDs."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT city_id FROM favorites ORDER BY added_at DESC")
    rows = cursor.fetchall()
    
    conn.close()
    
    return [row["city_id"] for row in rows]


# Statistics functions using SQL
def get_regional_statistics_sql() -> list[dict]:
    """Get regional statistics using SQL aggregation."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            region,
            COUNT(*) as city_count,
            population
        FROM cities
        GROUP BY region
        ORDER BY region
    """)
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]


def get_cities_count_by_region() -> dict[str, int]:
    """Get count of cities per region using SQL."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT region, COUNT(*) as count
        FROM cities
        GROUP BY region
        ORDER BY region
    """)
    rows = cursor.fetchall()
    
    conn.close()
    
    return {row["region"]: row["count"] for row in rows}


def get_cities_count_by_season() -> dict[str, int]:
    """Get count of cities per season using SQL."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            SUBSTR(best_season, 1, INSTR(best_season, ' ') - 1) as season,
            COUNT(*) as count
        FROM cities
        GROUP BY season
        ORDER BY season
    """)
    rows = cursor.fetchall()
    
    conn.close()
    
    return {row["season"]: row["count"] for row in rows}


def get_total_cities() -> int:
    """Get total number of cities using SQL."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as count FROM cities")
    result = cursor.fetchone()
    
    conn.close()
    
    return result["count"] if result else 0


# Itinerary CRUD functions
def create_itinerary(name: str, start_date: str, end_date: str, season: str, interests: str, budget: float | None = None) -> int:
    """Create a new itinerary and return its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO itineraries (name, start_date, end_date, season, interests, budget)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, start_date, end_date, season, interests, budget))
    
    itinerary_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return itinerary_id


def get_all_itineraries() -> list[dict]:
    """Get all itineraries."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM itineraries ORDER BY created_at DESC")
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]


def get_itinerary_by_id(itinerary_id: int) -> dict | None:
    """Get an itinerary by its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM itineraries WHERE id = ?", (itinerary_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    return dict(row) if row else None


def update_itinerary(itinerary_id: int, name: str | None = None, start_date: str | None = None, 
                     end_date: str | None = None, season: str | None = None, 
                     interests: str | None = None, budget: float | None = None) -> bool:
    """Update an itinerary. Returns True if updated."""
    conn = get_connection()
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if name is not None:
        updates.append("name = ?")
        params.append(name)
    if start_date is not None:
        updates.append("start_date = ?")
        params.append(start_date)
    if end_date is not None:
        updates.append("end_date = ?")
        params.append(end_date)
    if season is not None:
        updates.append("season = ?")
        params.append(season)
    if interests is not None:
        updates.append("interests = ?")
        params.append(interests)
    if budget is not None:
        updates.append("budget = ?")
        params.append(budget)
    
    if not updates:
        conn.close()
        return False
    
    params.append(itinerary_id)
    cursor.execute(f"UPDATE itineraries SET {', '.join(updates)} WHERE id = ?", params)
    
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    return rows_affected > 0


def delete_itinerary(itinerary_id: int) -> bool:
    """Delete an itinerary. Returns True if deleted."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM itineraries WHERE id = ?", (itinerary_id,))
    rows_affected = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    return rows_affected > 0


# Itinerary cities functions
def add_city_to_itinerary(itinerary_id: int, city_id: int, day_number: int, notes: str | None = None) -> int:
    """Add a city to an itinerary and return the entry ID."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO itinerary_cities (itinerary_id, city_id, day_number, notes)
        VALUES (?, ?, ?, ?)
    """, (itinerary_id, city_id, day_number, notes))
    
    entry_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return entry_id


def get_itinerary_cities(itinerary_id: int) -> list[dict]:
    """Get all cities in an itinerary with their details, ordered by day number."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT ic.day_number, ic.notes, c.*
        FROM itinerary_cities ic
        JOIN cities c ON ic.city_id = c.id
        WHERE ic.itinerary_id = ?
        ORDER BY ic.day_number
    """, (itinerary_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def remove_city_from_itinerary(itinerary_id: int, city_id: int) -> bool:
    """Remove a city from an itinerary. Returns True if removed."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "DELETE FROM itinerary_cities WHERE itinerary_id = ? AND city_id = ?",
        (itinerary_id, city_id)
    )
    rows_affected = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    return rows_affected > 0


def clear_itinerary_cities(itinerary_id: int) -> bool:
    """Remove all cities from an itinerary. Returns True if cleared."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM itinerary_cities WHERE itinerary_id = ?", (itinerary_id,))
    rows_affected = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    return rows_affected > 0
