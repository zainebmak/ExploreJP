from explorejp.console import clear_screen, pause, print_line, read_choice
from explorejp.data import City, favorites, get_all_regions, get_cities_by_region, get_city


# Region emoji mapping
REGION_EMOJIS = {
    "Kanto": "🗼",
    "Kansai": "⛩",
    "Hokkaido": "❄",
    "Kyushu": "🌊",
    "Chugoku": "🏯",
    "Tohoku": "🌿",
}


def show_explore_by_region() -> None:
    """Allow users to explore cities by region."""
    while True:
        clear_screen()
        _render_region_menu()
        choice = read_choice("\nChoose a region: ")
        
        if choice == "0":
            return
        
        regions = get_all_regions()
        if choice.isdigit() and 1 <= int(choice) <= len(regions):
            region = regions[int(choice) - 1]
            _show_region_cities(region)
        else:
            clear_screen()
            print_line("\n  Invalid option.\n")
            pause("Press ENTER to try again...")


def _render_region_menu() -> None:
    regions = get_all_regions()
    region_list = "\n".join(
        f"{i + 1}. {REGION_EMOJIS.get(region, '📍')} {region}"
        for i, region in enumerate(regions)
    )
    print_line(
        f"""
═══════════════════════════════

      🌎 EXPLORE BY REGION

═══════════════════════════════

{region_list}

0. ⬅ Back

═══════════════════════════════"""
    )


def _show_region_cities(region: str) -> None:
    """Show cities in a specific region."""
    cities = get_cities_by_region(region)
    emoji = REGION_EMOJIS.get(region, "📍")
    
    while True:
        clear_screen()
        city_list = "\n".join(
            f"{i + 1}. {city.name}" for i, (city_id, city) in enumerate(cities)
        )
        print_line(
            f"""
═══════════════════════════════

        {emoji} {region.upper()}

═══════════════════════════════

Cities

{city_list}

0. Back

═══════════════════════════════"""
        )
        
        choice = read_choice("\nChoose a city: ")
        
        if choice == "0":
            return
        
        if choice.isdigit() and 1 <= int(choice) <= len(cities):
            city_id, city = cities[int(choice) - 1]
            _show_city_details(city_id, city, emoji)
        else:
            clear_screen()
            print_line("\n  Invalid option.\n")
            pause("Press ENTER to try again...")


def _show_city_details(city_id: str, city: City, region_emoji: str) -> None:
    """Show city details with option to add to favorites."""
    known_for = "\n".join(city.known_for)
    is_fav = favorites.is_favorite(city_id)
    fav_option = "1. ❤️ Add to My Japan" if not is_fav else "1. ❤️ Remove from My Japan"
    
    clear_screen()
    print_line(
        f"""
═══════════════════════════════

{region_emoji} {city.name.upper()}

═══════════════════════════════

Population

{city.population}

Best Season

{city.best_season}

Known For

{known_for}

═══════════════════════════════

{fav_option}

0. Back"""
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
    elif choice == "0":
        return
