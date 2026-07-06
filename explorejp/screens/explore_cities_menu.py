from explorejp.console import clear_screen, pause, print_line, read_choice
from explorejp.screens.explore_cities import show_explore_cities
from explorejp.screens.favorites import show_favorites
from explorejp.screens.search_cities import show_search_cities


def show_explore_cities_menu() -> None:
    """Show the Explore Cities submenu with View, Search, Favorites, Compare options."""
    while True:
        clear_screen()
        _render_menu()
        choice = read_choice("\nChoose an option: ")

        if choice == "0":
            return

        if choice == "1":
            show_explore_cities()
            continue

        if choice == "2":
            show_search_cities()
            continue

        if choice == "3":
            show_favorites()
            continue

        if choice == "4":
            _show_compare_placeholder()
            continue

        clear_screen()
        print_line("\n  Invalid option. Please choose a number from the menu.\n")
        pause("Press ENTER to try again...")


def _render_menu() -> None:
    print_line(
        """
═══════════════════════════════
        EXPLORE CITIES
═══════════════════════════════

1. View Cities

2. Search

3. Favorites

4. Compare

0. Back

═══════════════════════════════"""
    )


def _show_compare_placeholder() -> None:
    clear_screen()
    print_line(
        """
═══════════════════════════════
           COMPARE
═══════════════════════════════

This feature is coming soon.

Compare cities side by side to help
you decide where to visit or live.

═══════════════════════════════"""
    )
    pause("\nPress ENTER to return to the menu...")
