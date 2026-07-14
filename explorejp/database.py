"""Database module for ExploreJP using SQLite."""

import sqlite3
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent.parent / "database" / "explorejp.db"


def get_connection() -> sqlite3.Connection:
    """Get a database connection."""
    # Ensure database directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
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
    
    # Create cherry_blossom_cities table for sakura-specific data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cherry_blossom_cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER NOT NULL UNIQUE,
            peak_bloom_start TEXT,
            peak_bloom_end TEXT,
            latitude REAL,
            longitude REAL,
            crowd_level TEXT,
            travel_tips TEXT,
            FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
        )
    """)
    
    # Create sakura_spots table for best viewing locations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sakura_spots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            image_url TEXT,
            FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
        )
    """)

    # Add nearby_attractions column if it doesn't exist yet (migration)
    try:
        cursor.execute("ALTER TABLE cherry_blossom_cities ADD COLUMN nearby_attractions TEXT")
        conn.commit()
    except Exception:
        pass  # Column already exists
    
    # Create sakura_forecasts table for bloom predictions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sakura_forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER NOT NULL,
            forecast_date TEXT NOT NULL,
            bloom_percentage INTEGER,
            FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
        )
    """)

    # Create weather_data table for climate information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER NOT NULL UNIQUE,
            january_avg_temp REAL,
            february_avg_temp REAL,
            march_avg_temp REAL,
            april_avg_temp REAL,
            may_avg_temp REAL,
            june_avg_temp REAL,
            july_avg_temp REAL,
            august_avg_temp REAL,
            september_avg_temp REAL,
            october_avg_temp REAL,
            november_avg_temp REAL,
            december_avg_temp REAL,
            annual_avg_temp REAL,
            annual_precipitation REAL,
            humidity_avg REAL,
            climate_type TEXT,
            best_months TEXT,
            FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
        )
    """)

    # ── User authentication tables ────────────────────────────────────────────

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            preferred_theme TEXT DEFAULT 'light',
            favorite_season TEXT DEFAULT '',
            preferred_budget TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            city_id INTEGER NOT NULL,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, city_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recently_viewed (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            city_id INTEGER NOT NULL,
            viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bucket_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            city_id INTEGER NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, city_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
        )
    """)

    # Create reviews table for community reviews and ratings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            city_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            review_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, city_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
        )
    """)

    # Add user_id to itineraries if not present (migration)
    try:
        cursor.execute("ALTER TABLE itineraries ADD COLUMN user_id INTEGER REFERENCES users(id) ON DELETE CASCADE")
        conn.commit()
    except Exception:
        pass

    conn.commit()
    conn.close()

    # Seed cherry blossom data if not already present
    _seed_cherry_blossom_data()


def _seed_cherry_blossom_data() -> None:
    """Seed sample cherry blossom data if the tables are empty."""
    conn = get_connection()
    cursor = conn.cursor()

    # Only seed if no data exists yet
    cursor.execute("SELECT COUNT(*) as count FROM cherry_blossom_cities")
    if cursor.fetchone()["count"] > 0:
        conn.close()
        return

    # ── cherry_blossom_cities ─────────────────────────────────────────────────
    cb_cities = [
        # city_id, peak_start, peak_end, lat, lon, crowd_level, tips, nearby_attractions
        (1, "2024-03-25", "2024-04-05", 35.6762, 139.6503, "Very High",
         "Visit Shinjuku Gyoen or Ueno Park early morning to beat the crowds.",
         "Senso-ji Temple, Shibuya Crossing, Tokyo Skytree, Meiji Shrine"),
        (2, "2024-04-01", "2024-04-10", 35.0116, 135.7681, "Very High",
         "Philosopher's Path and Maruyama Park are best at dawn.",
         "Fushimi Inari Shrine, Kinkaku-ji (Golden Pavilion), Arashiyama Bamboo Grove, Gion District"),
        (3, "2024-03-28", "2024-04-08", 34.6937, 135.5023, "High",
         "Osaka Castle Park is a local favourite with fewer tourists than Kyoto.",
         "Dotonbori, Universal Studios Japan, Shinsekai District, Kuromon Market"),
        (4, "2024-04-01", "2024-04-12", 34.3853, 132.4553, "Medium",
         "Hiroshima Peace Park sakura creates a powerful and moving atmosphere.",
         "Peace Memorial Museum, Miyajima Island, Itsukushima Shrine, Atomic Bomb Dome"),
        (5, "2024-04-25", "2024-05-05", 43.0618, 141.3545, "Low",
         "Hokkaido blooms late — perfect for those who miss the southern season.",
         "Odori Park, Sapporo Beer Museum, Hokkaido University, Clock Tower"),
        (6, "2024-03-25", "2024-04-05", 33.5904, 130.4017, "Medium",
         "Maizuru Park inside Fukuoka Castle ruins is the top spot.",
         "Dazaifu Tenmangu Shrine, Canal City, Hakata Old Town, Ohori Park"),
        (7, "2024-04-01", "2024-04-10", 34.6851, 135.8048, "Medium",
         "Watch deer wander under blossoming trees in Nara Park.",
         "Todai-ji Temple, Kasuga Grand Shrine, Horyu-ji Temple, Isuien Garden"),
        (8, "2024-04-10", "2024-04-20", 38.2682, 140.8694, "Low",
         "Sendai is less crowded — enjoy the Western-style zelkova avenues too.",
         "Zuihoden Mausoleum, Sendai Castle Ruins, Tanabata Festival sites, Matsushima Bay"),
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO cherry_blossom_cities
        (city_id, peak_bloom_start, peak_bloom_end, latitude, longitude, crowd_level, travel_tips, nearby_attractions)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, cb_cities)

    # Backfill nearby_attractions for existing rows that have NULL
    attractions_update = [
        ("Senso-ji Temple, Shibuya Crossing, Tokyo Skytree, Meiji Shrine", 1),
        ("Fushimi Inari Shrine, Kinkaku-ji (Golden Pavilion), Arashiyama Bamboo Grove, Gion District", 2),
        ("Dotonbori, Universal Studios Japan, Shinsekai District, Kuromon Market", 3),
        ("Peace Memorial Museum, Miyajima Island, Itsukushima Shrine, Atomic Bomb Dome", 4),
        ("Odori Park, Sapporo Beer Museum, Hokkaido University, Clock Tower", 5),
        ("Dazaifu Tenmangu Shrine, Canal City, Hakata Old Town, Ohori Park", 6),
        ("Todai-ji Temple, Kasuga Grand Shrine, Horyu-ji Temple, Isuien Garden", 7),
        ("Zuihoden Mausoleum, Sendai Castle Ruins, Tanabata Festival sites, Matsushima Bay", 8),
    ]
    cursor.executemany("""
        UPDATE cherry_blossom_cities SET nearby_attractions = ?
        WHERE city_id = ? AND (nearby_attractions IS NULL OR nearby_attractions = '')
    """, attractions_update)

    # ── sakura_spots ──────────────────────────────────────────────────────────
    spots = [
        # city_id, name, description, image_url
        (1, "Shinjuku Gyoen", "One of Japan's largest parks with 1,100+ cherry trees.",
         "https://i.pinimg.com/1200x/7b/0a/3b/7b0a3bdce4604379fa847476756b2050.jpg"),
        (1, "Ueno Park", "Tokyo's most popular hanami destination.",
         "https://i.pinimg.com/736x/02/f6/24/02f6246888da9cfda7024d52b62f7463.jpg"),
        (1, "Chidorigafuchi", "Stunning canal lined with over 260 cherry trees.",
         "https://i.pinimg.com/1200x/c6/70/d9/c670d985b022020c837b5186259f3aa7.jpg"),
        (2, "Philosopher's Path", "A stone path lined with hundreds of cherry trees.",
         "https://i.pinimg.com/1200x/3d/c5/e9/3dc5e90782bcb686b53b20290b9258f9.jpg"),
        (2, "Maruyama Park", "Kyoto's most famous hanami spot with a weeping cherry centrepiece.",
         "https://i.pinimg.com/1200x/e9/d6/38/e9d6381765807102cb75b3a52a15d9fe.jpg"),
        (3, "Osaka Castle Park", "500 cherry trees surround the iconic castle.",
         "https://i.pinimg.com/1200x/c4/d3/4e/c4d34e7da3d9d560186ce665a15e3de4.jpg"),
        (4, "Hiroshima Peace Park", "Sakura blossoms alongside the Peace Memorial.",
         "https://i.pinimg.com/1200x/ab/63/76/ab6376e22553ef8d84cda90fd56eea0b.jpg"),
        (5, "Maruyama Park Sapporo", "Hokkaido's most beloved cherry blossom park.",
         "https://i.pinimg.com/1200x/93/70/4c/93704c6171b38186e5466718f64d3c2d.jpg"),
        (6, "Maizuru Park", "Ruins of Fukuoka Castle surrounded by cherry trees.",
         "https://i.pinimg.com/1200x/6b/35/f7/6b35f7ad90a61fa78141dbfef75d03ea.jpg"),
        (7, "Nara Park", "Walk among free-roaming deer under cherry blossoms.",
         "https://i.pinimg.com/736x/e2/9e/2d/e29e2dfc8e4151fe394d1ba75b1816bf.jpg"),
        (8, "Tsutsujigaoka Park", "Sendai's top spot with 1,200 cherry trees.",
         "https://i.pinimg.com/1200x/c8/49/f1/c849f1a39c73a15a906107bd0c67b28c.jpg"),
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO sakura_spots (city_id, name, description, image_url)
        VALUES (?, ?, ?, ?)
    """, spots)

    # ── sakura_forecasts (daily entries for peak windows) ─────────────────────
    import datetime
    forecasts = []
    # For each city, generate daily forecast entries spanning ±3 weeks around peak
    peak_dates = {
        1: datetime.date(2024, 3, 30),
        2: datetime.date(2024, 4, 5),
        3: datetime.date(2024, 4, 2),
        4: datetime.date(2024, 4, 6),
        5: datetime.date(2024, 4, 30),
        6: datetime.date(2024, 3, 30),
        7: datetime.date(2024, 4, 5),
        8: datetime.date(2024, 4, 15),
    }
    for city_id, peak in peak_dates.items():
        for delta in range(-20, 21):
            d = peak + datetime.timedelta(days=delta)
            # Bell-curve percentage centred on peak
            pct = max(0, int(100 - (abs(delta) ** 1.8)))
            forecasts.append((city_id, d.strftime("%Y-%m-%d"), pct))

    cursor.executemany("""
        INSERT OR IGNORE INTO sakura_forecasts (city_id, forecast_date, bloom_percentage)
        VALUES (?, ?, ?)
    """, forecasts)

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


# Cherry Blossom functions
def add_cherry_blossom_city(city_id: int, peak_bloom_start: str, peak_bloom_end: str, 
                           latitude: float, longitude: float, crowd_level: str, 
                           travel_tips: str) -> int:
    """Add cherry blossom data for a city."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO cherry_blossom_cities 
        (city_id, peak_bloom_start, peak_bloom_end, latitude, longitude, crowd_level, travel_tips)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (city_id, peak_bloom_start, peak_bloom_end, latitude, longitude, crowd_level, travel_tips))
    
    cb_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return cb_id


def get_cherry_blossom_cities() -> list[dict]:
    """Get all cities with cherry blossom data."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT cbc.*, c.name, c.region 
        FROM cherry_blossom_cities cbc
        JOIN cities c ON cbc.city_id = c.id
        ORDER BY cbc.peak_bloom_start
    """)
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]


def get_cherry_blossom_city_by_id(city_id: int) -> dict | None:
    """Get cherry blossom data for a specific city."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT cbc.*, c.name, c.region 
        FROM cherry_blossom_cities cbc
        JOIN cities c ON cbc.city_id = c.id
        WHERE cbc.city_id = ?
    """, (city_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    return dict(row) if row else None


def add_sakura_spot(city_id: int, name: str, description: str, image_url: str) -> int:
    """Add a sakura viewing spot for a city."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO sakura_spots (city_id, name, description, image_url)
        VALUES (?, ?, ?, ?)
    """, (city_id, name, description, image_url))
    
    spot_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return spot_id


def get_sakura_spots(city_id: int) -> list[dict]:
    """Get all sakura viewing spots for a city."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM sakura_spots 
        WHERE city_id = ?
        ORDER BY id
    """, (city_id,))
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]


def add_sakura_forecast(city_id: int, forecast_date: str, bloom_percentage: int) -> int:
    """Add a bloom forecast for a city."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO sakura_forecasts (city_id, forecast_date, bloom_percentage)
        VALUES (?, ?, ?)
    """, (city_id, forecast_date, bloom_percentage))
    
    forecast_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return forecast_id


def get_sakura_forecast(city_id: int, forecast_date: str) -> dict | None:
    """Get bloom forecast for a city on a specific date."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT sf.*, c.name 
        FROM sakura_forecasts sf
        JOIN cities c ON sf.city_id = c.id
        WHERE sf.city_id = ? AND sf.forecast_date = ?
    """, (city_id, forecast_date))
    row = cursor.fetchone()
    
    conn.close()
    
    return dict(row) if row else None


def get_cities_by_bloom_month(month: str) -> list[dict]:
    """Get cities that have peak bloom in a specific month."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT cbc.*, c.name, c.region 
        FROM cherry_blossom_cities cbc
        JOIN cities c ON cbc.city_id = c.id
        WHERE strftime('%m', cbc.peak_bloom_start) = ?
        ORDER BY cbc.peak_bloom_start
    """, (month,))
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]


# ── User auth functions ───────────────────────────────────────────────────────

import bcrypt as _bcrypt


def create_user(username: str, email: str, password: str) -> int | None:
    """Create a new user. Returns user id or None if username/email taken."""
    conn = get_connection()
    cursor = conn.cursor()
    password_hash = _bcrypt.hashpw(password.encode(), _bcrypt.gensalt()).decode()
    try:
        cursor.execute("""
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        """, (username.strip(), email.strip().lower(), password_hash))
        user_id = cursor.lastrowid
        conn.commit()
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def get_user_by_username(username: str) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username.strip(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id: int) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def verify_password(username: str, password: str) -> dict | None:
    """Verify credentials. Returns user dict on success, None on failure."""
    user = get_user_by_username(username)
    if not user:
        return None
    if _bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return user
    return None


def update_user_settings(user_id: int, username: str | None = None,
                         email: str | None = None, password: str | None = None,
                         preferred_theme: str | None = None,
                         favorite_season: str | None = None,
                         preferred_budget: str | None = None) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    updates, params = [], []
    if username is not None:
        updates.append("username = ?"); params.append(username.strip())
    if email is not None:
        updates.append("email = ?"); params.append(email.strip().lower())
    if password is not None:
        h = _bcrypt.hashpw(password.encode(), _bcrypt.gensalt()).decode()
        updates.append("password_hash = ?"); params.append(h)
    if preferred_theme is not None:
        updates.append("preferred_theme = ?"); params.append(preferred_theme)
    if favorite_season is not None:
        updates.append("favorite_season = ?"); params.append(favorite_season)
    if preferred_budget is not None:
        updates.append("preferred_budget = ?"); params.append(preferred_budget)
    if not updates:
        conn.close(); return False
    params.append(user_id)
    try:
        cursor.execute(f"UPDATE users SET {', '.join(updates)} WHERE id = ?", params)
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def delete_user(user_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0


# ── User favorites ────────────────────────────────────────────────────────────

def add_user_favorite(user_id: int, city_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO user_favorites (user_id, city_id) VALUES (?, ?)",
                       (user_id, city_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def remove_user_favorite(user_id: int, city_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_favorites WHERE user_id = ? AND city_id = ?",
                   (user_id, city_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0


def is_user_favorite(user_id: int, city_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM user_favorites WHERE user_id = ? AND city_id = ?",
                   (user_id, city_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def get_user_favorites(user_id: int) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.*, uf.date_added FROM cities c
        JOIN user_favorites uf ON c.id = uf.city_id
        WHERE uf.user_id = ?
        ORDER BY uf.date_added DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_user_favorite_ids(user_id: int) -> list[int]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT city_id FROM user_favorites WHERE user_id = ? ORDER BY date_added DESC",
                   (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [row["city_id"] for row in rows]


# ── Recently viewed ───────────────────────────────────────────────────────────

def add_recently_viewed(user_id: int, city_id: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    # Remove old entry if exists so latest bubbles to top
    cursor.execute("DELETE FROM recently_viewed WHERE user_id = ? AND city_id = ?",
                   (user_id, city_id))
    cursor.execute("INSERT INTO recently_viewed (user_id, city_id) VALUES (?, ?)",
                   (user_id, city_id))
    # Keep only last 20 per user
    cursor.execute("""
        DELETE FROM recently_viewed WHERE id NOT IN (
            SELECT id FROM recently_viewed WHERE user_id = ?
            ORDER BY viewed_at DESC LIMIT 20
        ) AND user_id = ?
    """, (user_id, user_id))
    conn.commit()
    conn.close()


def get_recently_viewed(user_id: int, limit: int = 6) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.*, rv.viewed_at FROM cities c
        JOIN recently_viewed rv ON c.id = rv.city_id
        WHERE rv.user_id = ?
        ORDER BY rv.viewed_at DESC
        LIMIT ?
    """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ── Bucket list ───────────────────────────────────────────────────────────────

def add_to_bucket_list(user_id: int, city_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO bucket_list (user_id, city_id) VALUES (?, ?)",
                       (user_id, city_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def remove_from_bucket_list(user_id: int, city_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bucket_list WHERE user_id = ? AND city_id = ?",
                   (user_id, city_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0


def is_in_bucket_list(user_id: int, city_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM bucket_list WHERE user_id = ? AND city_id = ?",
                   (user_id, city_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def get_bucket_list(user_id: int) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.*, bl.added_at FROM cities c
        JOIN bucket_list bl ON c.id = bl.city_id
        WHERE bl.user_id = ?
        ORDER BY bl.added_at DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ── User-scoped itineraries ───────────────────────────────────────────────────

def create_user_itinerary(user_id: int, name: str, start_date: str, end_date: str,
                          season: str, interests: str, budget: float | None = None) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO itineraries (user_id, name, start_date, end_date, season, interests, budget)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, name, start_date, end_date, season, interests, budget))
    itinerary_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return itinerary_id


def get_user_itineraries(user_id: int) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM itineraries WHERE user_id = ? ORDER BY created_at DESC",
                   (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ── Weather data functions ───────────────────────────────────────────────────────

def add_weather_data(city_id: int, january_avg_temp: float, february_avg_temp: float,
                    march_avg_temp: float, april_avg_temp: float, may_avg_temp: float,
                    june_avg_temp: float, july_avg_temp: float, august_avg_temp: float,
                    september_avg_temp: float, october_avg_temp: float, november_avg_temp: float,
                    december_avg_temp: float, annual_avg_temp: float, annual_precipitation: float,
                    humidity_avg: float, climate_type: str, best_months: str) -> int:
    """Add weather data for a city."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO weather_data 
        (city_id, january_avg_temp, february_avg_temp, march_avg_temp, april_avg_temp,
         may_avg_temp, june_avg_temp, july_avg_temp, august_avg_temp, september_avg_temp,
         october_avg_temp, november_avg_temp, december_avg_temp, annual_avg_temp,
         annual_precipitation, humidity_avg, climate_type, best_months)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (city_id, january_avg_temp, february_avg_temp, march_avg_temp, april_avg_temp,
          may_avg_temp, june_avg_temp, july_avg_temp, august_avg_temp, september_avg_temp,
          october_avg_temp, november_avg_temp, december_avg_temp, annual_avg_temp,
          annual_precipitation, humidity_avg, climate_type, best_months))
    
    weather_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return weather_id


def get_weather_data_by_city(city_id: int) -> dict | None:
    """Get weather data for a specific city."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT wd.*, c.name, c.region 
        FROM weather_data wd
        JOIN cities c ON wd.city_id = c.id
        WHERE wd.city_id = ?
    """, (city_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    return dict(row) if row else None


def get_all_weather_data() -> list[dict]:
    """Get all cities with weather data."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT wd.*, c.name, c.region 
        FROM weather_data wd
        JOIN cities c ON wd.city_id = c.id
        ORDER BY c.name
    """)
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]


def get_weather_data_by_climate_type(climate_type: str) -> list[dict]:
    """Get cities by climate type."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT wd.*, c.name, c.region 
        FROM weather_data wd
        JOIN cities c ON wd.city_id = c.id
        WHERE wd.climate_type LIKE ?
        ORDER BY c.name
    """, (f"%{climate_type}%",))
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]


def get_cities_by_best_month(month: str) -> list[dict]:
    """Get cities that have a specific month in their best months."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT wd.*, c.name, c.region 
        FROM weather_data wd
        JOIN cities c ON wd.city_id = c.id
        WHERE wd.best_months LIKE ?
        ORDER BY c.name
    """, (f"%{month}%",))
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]


def update_weather_data(city_id: int, **kwargs) -> bool:
    """Update weather data for a city. Returns True if updated."""
    conn = get_connection()
    cursor = conn.cursor()
    
    valid_fields = [
        'january_avg_temp', 'february_avg_temp', 'march_avg_temp', 'april_avg_temp',
        'may_avg_temp', 'june_avg_temp', 'july_avg_temp', 'august_avg_temp',
        'september_avg_temp', 'october_avg_temp', 'november_avg_temp', 'december_avg_temp',
        'annual_avg_temp', 'annual_precipitation', 'humidity_avg', 'climate_type', 'best_months'
    ]
    
    updates = []
    params = []
    
    for key, value in kwargs.items():
        if key in valid_fields and value is not None:
            updates.append(f"{key} = ?")
            params.append(value)
    
    if not updates:
        conn.close()
        return False
    
    params.append(city_id)
    cursor.execute(f"UPDATE weather_data SET {', '.join(updates)} WHERE city_id = ?", params)
    
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    return rows_affected > 0


# ── Reviews and Ratings functions ───────────────────────────────────────────────

def add_review(user_id: int, city_id: int, rating: int, review_text: str | None = None) -> int | None:
    """Add a review for a city. Returns review id or None if already reviewed."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO reviews (user_id, city_id, rating, review_text)
            VALUES (?, ?, ?, ?)
        """, (user_id, city_id, rating, review_text))
        
        review_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return review_id
    except sqlite3.IntegrityError:
        # User already reviewed this city
        conn.close()
        return None


def get_reviews_by_city(city_id: int) -> list[dict]:
    """Get all reviews for a city with user info."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT r.*, u.username, c.name as city_name
        FROM reviews r
        JOIN users u ON r.user_id = u.id
        JOIN cities c ON r.city_id = c.id
        WHERE r.city_id = ?
        ORDER BY r.created_at DESC
    """, (city_id,))
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]


def get_reviews_by_user(user_id: int) -> list[dict]:
    """Get all reviews by a user with city info."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT r.*, c.name as city_name, c.region
        FROM reviews r
        JOIN cities c ON r.city_id = c.id
        WHERE r.user_id = ?
        ORDER BY r.created_at DESC
    """, (user_id,))
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]


def get_user_review_for_city(user_id: int, city_id: int) -> dict | None:
    """Get a specific user's review for a city."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT r.*, c.name as city_name
        FROM reviews r
        JOIN cities c ON r.city_id = c.id
        WHERE r.user_id = ? AND r.city_id = ?
    """, (user_id, city_id))
    row = cursor.fetchone()
    
    conn.close()
    
    return dict(row) if row else None


def update_review(user_id: int, city_id: int, rating: int | None = None, 
                  review_text: str | None = None) -> bool:
    """Update an existing review. Returns True if updated."""
    conn = get_connection()
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if rating is not None:
        updates.append("rating = ?")
        params.append(rating)
    if review_text is not None:
        updates.append("review_text = ?")
        params.append(review_text)
    
    if not updates:
        conn.close()
        return False
    
    updates.append("updated_at = CURRENT_TIMESTAMP")
    params.extend([user_id, city_id])
    
    cursor.execute(f"""
        UPDATE reviews 
        SET {', '.join(updates)}
        WHERE user_id = ? AND city_id = ?
    """, params)
    
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    return rows_affected > 0


def delete_review(user_id: int, city_id: int) -> bool:
    """Delete a review. Returns True if deleted."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        DELETE FROM reviews 
        WHERE user_id = ? AND city_id = ?
    """, (user_id, city_id))
    
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    return rows_affected > 0


def get_city_average_rating(city_id: int) -> float:
    """Get the average rating for a city."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT AVG(rating) as avg_rating
        FROM reviews
        WHERE city_id = ?
    """, (city_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    return round(result["avg_rating"], 1) if result and result["avg_rating"] else 0.0


def get_city_rating_count(city_id: int) -> int:
    """Get the number of reviews for a city."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM reviews
        WHERE city_id = ?
    """, (city_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    return result["count"] if result else 0


def get_all_reviews() -> list[dict]:
    """Get all reviews with user and city info."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT r.*, u.username, c.name as city_name, c.region
        FROM reviews r
        JOIN users u ON r.user_id = u.id
        JOIN cities c ON r.city_id = c.id
        ORDER BY r.created_at DESC
    """)
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]


def delete_weather_data(city_id: int) -> bool:
    """Delete weather data for a city. Returns True if deleted."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM weather_data WHERE city_id = ?", (city_id,))
    rows_affected = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    return rows_affected > 0
