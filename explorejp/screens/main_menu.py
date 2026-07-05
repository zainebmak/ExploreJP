from explorejp.console import clear_screen, pause, print_line, read_choice
from explorejp.screens.explore_cities import show_explore_cities

MENU_OPTIONS = {
    "1": ("Explore Cities", "🗾"),
    "2": ("Cherry Blossom Guide", "🌸"),
    "3": ("Famous Attractions", "🏯"),
    "4": ("Japanese Cuisine", "🍜"),
    "5": ("Transportation", "🚄"),
    "6": ("Cost of Living", "💴"),
    "7": ("Statistics", "📊"),
    "8": ("About ExploreJP", "ℹ️"),
    "0": ("Exit", None),
}


def _render_menu() -> None:
    print_line(
        """
═══════════════════════════════
           MAIN MENU
═══════════════════════════════

1. 🗾 Explore Cities

2. 🌸 Cherry Blossom Guide

3. 🏯 Famous Attractions

4. 🍜 Japanese Cuisine

5. 🚄 Transportation

6. 💴 Cost of Living

7. 📊 Statistics

8. ℹ️ About ExploreJP

0. Exit

═══════════════════════════════"""
    )


def _show_about() -> None:
    clear_screen()
    print_line(
        """
═══════════════════════════════
        ABOUT EXPLOREJP
═══════════════════════════════

ExploreJP is a data-driven platform that helps
people discover Japanese cities, compare living
costs, analyze weather, explore transportation,
and plan their journey through Japan.

Version: 0.1.0 (Console)
Status: Early development

═══════════════════════════════"""
    )
    pause("\nPress ENTER to return to the menu...")


def _show_placeholder(title: str) -> None:
    clear_screen()
    print_line(
        f"""
═══════════════════════════════
           {title.upper()}
═══════════════════════════════

This section is coming soon.

═══════════════════════════════"""
    )
    pause("\nPress ENTER to return to the menu...")


def show_main_menu() -> None:
    while True:
        clear_screen()
        _render_menu()
        choice = read_choice("\nChoose an option: ")

        if choice == "0":
            clear_screen()
            print_line("\n  Thank you for using ExploreJP. Sayōnara! 👋\n")
            break

        if choice == "8":
            _show_about()
            continue

        if choice == "1":
            show_explore_cities()
            continue

        if choice in {"2", "3", "4", "5", "6", "7"}:
            title, _ = MENU_OPTIONS[choice]
            _show_placeholder(title)
            continue

        clear_screen()
        print_line("\n  Invalid option. Please choose a number from the menu.\n")
        pause("Press ENTER to try again...")
