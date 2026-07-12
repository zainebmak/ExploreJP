"""Initialize the ExploreJP database with CSV data."""

from explorejp.database import import_csv_to_db, init_database


if __name__ == "__main__":
    print("Initializing database...")
    init_database()
    print("Database initialized.")
    
    print("Importing CSV data...")
    import_csv_to_db()
    print("CSV data imported successfully.")
    
    print("Database setup complete!")
