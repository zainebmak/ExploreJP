from explorejp.console import clear_screen, pause, print_line, read_choice
from explorejp.data import CITIES, City


def _render_city_list() -> None:
    print_line(
        """
══════════════════════

Explore Cities

══════════════════════

1 Tokyo

2 Kyoto

3 Osaka

4 Hiroshima

5 Sapporo

6 Fukuoka

0 Back"""
    )


def _show_city(city: City) -> None:
    known_for = "\n".join(city.known_for)
    clear_screen()
    print_line(
        f"""
═══════════════════════════════

{city.name}

═══════════════════════════════

Population

{city.population}

Region

{city.region}

Best Season

{city.best_season}

Known For

{known_for}

Press ENTER..."""
    )
    pause("")


def show_explore_cities() -> None:
    while True:
        clear_screen()
        _render_city_list()
        choice = read_choice("\nChoose a city: ")

        if choice == "0":
            return

        city = CITIES.get(choice)
        if city is None:
            clear_screen()
            print_line("\n  Invalid option. Please choose a city from the list.\n")
            pause("Press ENTER to try again...")
            continue

        _show_city(city)
