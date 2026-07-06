from explorejp.console import clear_screen, pause, print_line, read_choice
from explorejp.data import City, favorites, get_city, load_cities_from_csv


def _render_city_list() -> None:
    cities = load_cities_from_csv()
    city_list = "\n".join(
        f"{city_id} {city.name}" for city_id, city in sorted(cities.items())
    )
    print_line(
        f"""
══════════════════════

Explore Cities

══════════════════════

{city_list}

0 Back"""
    )


def _show_city(city_id: str, city: City) -> None:
    is_fav = favorites.is_favorite(city_id)
    fav_option = "1. ❤️ Remove from Favorites" if is_fav else "1. ❤️ Add to Favorites"
    
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

═══════════════════════════════

{fav_option}

2. ← Back"""
    )
    
    choice = read_choice("\nChoose an option: ")
    
    if choice == "1":
        if is_fav:
            if favorites.remove_favorite(city_id):
                clear_screen()
                print_line(f"\n  ✅ {city.name} removed from favorites.\n")
            else:
                clear_screen()
                print_line(f"\n  Failed to remove {city.name} from favorites.\n")
        else:
            if favorites.add_favorite(city_id):
                clear_screen()
                print_line(f"\n  ✅ {city.name} has been added to your favorites.\n")
            else:
                clear_screen()
                print_line(f"\n  {city.name} is already in favorites.\n")
        pause("Press ENTER to continue...")
    elif choice == "2":
        return


def show_explore_cities() -> None:
    while True:
        clear_screen()
        _render_city_list()
        choice = read_choice("\nChoose a city: ")

        if choice == "0":
            return

        city = get_city(choice)
        if city is None:
            clear_screen()
            print_line("\n  Invalid option. Please choose a city from the list.\n")
            pause("Press ENTER to try again...")
            continue

        _show_city(choice, city)
