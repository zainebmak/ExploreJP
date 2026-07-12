"""Main entry point for ExploreJP."""

from explorejp.console import configure_console
from explorejp.screens import show_main_menu, show_welcome
from explorejp.database import init_database, import_csv_to_db


def main() -> None:
    """Start the ExploreJP application."""

    # Configure console
    configure_console()

    # Initialize the SQLite database
    init_database()

    # Import cities from CSV into the database
    import_csv_to_db()

    # Launch the application
    show_welcome()
    show_main_menu()


if __name__ == "__main__":
    main()