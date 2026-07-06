from explorejp.console import clear_screen, pause, print_line, read_choice
from explorejp.screens.compare_cities import show_compare_cities
from explorejp.screens.explore_by_region import show_explore_by_region
from explorejp.screens.explore_cities import show_explore_cities
from explorejp.screens.favorites import show_favorites
from explorejp.screens.search_cities import show_search_cities


def show_explore_cities_menu() -> None:
    """Show the Explore Cities submenu with Discover, Browse, Region, Compare, My Japan options."""
    while True:
        clear_screen()
        _render_menu()
        choice = read_choice("\nChoose an option: ")

        if choice == "0":
            return

        if choice == "1":
            show_search_cities()
            continue

        if choice == "2":
            show_explore_cities()
            continue

        if choice == "3":
            show_explore_by_region()
            continue

        if choice == "4":
            show_compare_cities()
            continue

        if choice == "5":
            show_favorites()
            continue

        clear_screen()
        print_line("\n  Invalid option. Please choose a number from the menu.\n")
        pause("Press ENTER to try again...")


def _render_menu() -> None:
    print_line(
        """
═══════════════════════════════
      🗾 EXPLORE CITIES
═══════════════════════════════

1. 🌸 Discover a City

2. 📍 Browse All Cities

3. 🌎 Explore by Region

4. 📊 Compare Cities

5. ❤️ My Japan

0. Back

═══════════════════════════════"""
    )


