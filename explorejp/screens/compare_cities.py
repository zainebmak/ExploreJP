from explorejp.console import clear_screen, pause, print_line, read_choice
from explorejp.data import City, favorites, get_city, get_all_cities


# Region emoji mapping
REGION_EMOJIS = {
    "Kanto": "🗼",
    "Kansai": "⛩",
    "Hokkaido": "❄",
    "Kyushu": "🌊",
    "Chugoku": "🏯",
    "Tohoku": "🌿",
}


def show_compare_cities() -> None:
    """Allow users to compare two cities side by side."""
    cities = get_all_cities()
    city_list = sorted(cities.items())
    
    # Select first city
    city_id_1 = _select_city(city_list, "first")
    if city_id_1 is None:
        return
    
    city_1 = cities[city_id_1]
    
    # Select second city
    city_id_2 = _select_city(city_list, "second")
    if city_id_2 is None:
        return
    
    city_2 = cities[city_id_2]
    
    # Show comparison
    _show_comparison(city_id_1, city_1, city_id_2, city_2)


def _select_city(city_list: list[tuple[str, City]], position: str) -> str | None:
    """Let user select a city from the list."""
    while True:
        clear_screen()
        city_display = "\n".join(
            f"{city_id}. {city.name}" for city_id, city in city_list
        )
        print_line(
            f"""
═══════════════════════════════
      ⚖️ COMPARE CITIES
═══════════════════════════════

Choose the {position} city:

{city_display}

0. Back"""
        )
        
        choice = read_choice("\n> ")
        
        if choice == "0":
            return None
        
        cities_dict = dict(city_list)
        if choice in cities_dict:
            return choice
        
        clear_screen()
        print_line("\n  Invalid option.\n")
        pause("Press ENTER to try again...")


def _show_comparison(city_id_1: str, city_1: City, city_id_2: str, city_2: City) -> None:
    """Display side-by-side comparison of two cities."""
    emoji_1 = REGION_EMOJIS.get(city_1.region, "📍")
    emoji_2 = REGION_EMOJIS.get(city_2.region, "📍")
    
    # Get first known_for item for display
    known_for_1 = city_1.known_for[0] if city_1.known_for else ""
    known_for_2 = city_2.known_for[0] if city_2.known_for else ""
    
    clear_screen()
    print_line(
        f"""
═══════════════════════════════════════════════════════

              ⚖️ CITY COMPARISON

═══════════════════════════════════════════════════════

                 {emoji_1} {city_1.name:<12}        {emoji_2} {city_2.name:<12}
-------------------------------------------------------
Region           {city_1.region:<14}        {city_2.region:<14}

Population       {city_1.population:<14}        {city_2.population:<14}

Best Season      {city_1.best_season:<14}        {city_2.best_season:<14}

Known For        {known_for_1:<14}        {known_for_2:<14}

Cost of Living   {city_1.cost_of_living:<14}        {city_2.cost_of_living:<14}

═══════════════════════════════════════════════════════

1. ❤️ Save {city_1.name}

2. ❤️ Save {city_2.name}

0. ⬅ Back"""
    )
    
    choice = read_choice("\nChoose an option: ")
    
    if choice == "1":
        if favorites.add_favorite(city_id_1):
            clear_screen()
            print_line(f"\n  ✅ {city_1.name} has been added to your favorites.\n")
        else:
            clear_screen()
            print_line(f"\n  {city_1.name} is already in favorites.\n")
        pause("Press ENTER to continue...")
    elif choice == "2":
        if favorites.add_favorite(city_id_2):
            clear_screen()
            print_line(f"\n  ✅ {city_2.name} has been added to your favorites.\n")
        else:
            clear_screen()
            print_line(f"\n  {city_2.name} is already in favorites.\n")
        pause("Press ENTER to continue...")
    elif choice == "0":
        return
