from explorejp.console import clear_screen, pause, print_line


def show_welcome() -> None:
    clear_screen()
    print_line(
        """
═══════════════════════════════════════════════

              🌸 ExploreJP 🌸

          Discover Japan Through Data

═══════════════════════════════════════════════

Explore cities
Analyze culture
Discover destinations
Plan your journey

Press ENTER to continue..."""
    )
    pause("")
