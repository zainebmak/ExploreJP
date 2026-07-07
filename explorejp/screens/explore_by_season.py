from explorejp.console import clear_screen, pause, print_line, read_choice
from explorejp.data import City, favorites, get_all_seasons, get_cities_by_season, get_city


# Season data with descriptions and activities
SEASON_DATA = {
    "Spring": {
        "emoji": "🌸",
        "description": "Cherry Blossoms & Mild Weather",
        "quote": '"The season of cherry blossoms,\nfresh beginnings, and hanami."',
        "activities": [
            "🌸 Hanami Picnics",
            "🚶 Temple Walks",
            "📸 Photography"
        ]
    },
    "Summer": {
        "emoji": "☀️",
        "description": "Festivals & Beaches",
        "quote": '"The season of vibrant festivals,\nfireworks, and summer adventures."',
        "activities": [
            "🎆 Fireworks Festivals",
            "🏖️ Beach Visits",
            "🎪 Summer Matsuri"
        ]
    },
    "Autumn": {
        "emoji": "🍁",
        "description": "Colorful Leaves & Cozy Weather",
        "quote": '"The season of golden leaves,\ncomfort food, and scenic views."',
        "activities": [
            "🍂 Leaf Viewing",
            "🍜 Hot Springs",
            "🏯 Castle Tours"
        ]
    },
    "Winter": {
        "emoji": "❄️",
        "description": "Snow & Winter Festivals",
        "quote": '"The season of snow festivals,\nhot springs, and winter sports."',
        "activities": [
            "⛷️ Skiing & Snowboarding",
            "♨️ Onsen Visits",
            "🏔️ Snow Festivals"
        ]
    },
}

# Region emoji mapping
REGION_EMOJIS = {
    "Kanto": "🗼",
    "Kansai": "⛩",
    "Hokkaido": "❄️",
    "Kyushu": "🌊",
    "Chugoku": "🏯",
    "Tohoku": "🌿",
}


def show_explore_by_season() -> None:
    """Allow users to explore cities by season."""
    while True:
        clear_screen()
        _render_season_menu()
        choice = read_choice("\nChoose your journey: ")
        
        if choice == "0":
            return
        
        seasons = list(SEASON_DATA.keys())
        if choice.isdigit() and 1 <= int(choice) <= len(seasons):
            season = seasons[int(choice) - 1]
            _show_season_details(season)
        else:
            clear_screen()
            print_line("\n  Invalid option.\n")
            pause("Press ENTER to try again...")


def _render_season_menu() -> None:
    print_line(
        """
══════════════════════════════════════
       🌸 EXPLORE BY SEASON
══════════════════════════════════════

🌸 Spring
Cherry Blossoms & Mild Weather

☀️ Summer
Festivals & Beaches

🍂 Autumn
Colorful Leaves & Cozy Weather

❄️ Winter
Snow & Winter Festivals

0. Back

══════════════════════════════════════"""
    )


def _show_season_details(season: str) -> None:
    """Show detailed information for a specific season."""
    season_info = SEASON_DATA[season]
    emoji = season_info["emoji"]
    cities = get_cities_by_season(season)
    
    while True:
        clear_screen()
        
        # Get city list with region emojis
        city_list = "\n".join(
            f"{i + 1}. {REGION_EMOJIS.get(city.region, '📍')} {city.name}"
            for i, (city_id, city) in enumerate(cities)
        )
        
        # Get activities list
        activities_list = "\n".join(season_info["activities"])
        
        print_line(
            f"""
══════════════════════════════════════

        {emoji} {season.upper()} IN JAPAN

══════════════════════════════════════

{season_info["quote"]}

Recommended Cities

{city_list}

Best Activities

{activities_list}

0. Back

══════════════════════════════════════"""
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


def _show_city_details(city_id: str, city: City, season_emoji: str) -> None:
    """Show city details with option to add to favorites."""
    known_for = "\n".join(city.known_for)
    region_emoji = REGION_EMOJIS.get(city.region, "📍")
    is_fav = favorites.is_favorite(city_id)
    fav_option = "1. ❤️ Add to My Japan" if not is_fav else "1. ❤️ Remove from My Japan"
    
    clear_screen()
    print_line(
        f"""
═══════════════════════════════

{season_emoji} {city.name.upper()}

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
