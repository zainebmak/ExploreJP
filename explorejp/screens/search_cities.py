from explorejp.console import clear_screen, pause, print_line, read_choice
from explorejp.data import City, favorites, search_cities


def show_search_cities() -> None:
    """Allow users to search for cities by name."""
    while True:
        clear_screen()
        print_line(
            """
═══════════════════════════════════

        🔍 SEARCH CITY

═══════════════════════════════════

Enter a city name:

>"""
        )
        query = read_choice("> ").strip()
        
        if query == "0":
            return
        
        if not query:
            clear_screen()
            print_line("\n  Please enter a city name.\n")
            pause("Press ENTER to try again...")
            continue
        
        results = search_cities(query)
        
        if not results:
            clear_screen()
            print_line(f"\n  No cities found matching '{query}'.\n")
            pause("Press ENTER to try again...")
            continue
        
        # Show first result directly
        city_id, city = results[0]
        _show_city_result(city_id, city)


def _show_city_result(city_id: str, city: City) -> None:
    known_for = "\n".join(city.known_for)
    is_fav = favorites.is_favorite(city_id)
    fav_option = "1. ❤️ Add to My Japan" if not is_fav else "1. ❤️ Remove from My Japan"
    
    clear_screen()
    print_line(
        f"""
═══════════════════════════════════

🗼 {city.name.upper()}

═══════════════════════════════════

📍 Region
{city.region}

👥 Population
{city.population}

🌸 Best Season
{city.best_season}

🏯 Famous For
{known_for}

═══════════════════════════════════

{fav_option}

2. 🔍 Search Again

0. ⬅ Back"""
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
        return  # Search again
    elif choice == "0":
        return  # Back to menu
