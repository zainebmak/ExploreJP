from explorejp.console import clear_screen, pause, print_line, read_choice
from explorejp.data import City, favorites, get_city


def show_favorites() -> None:
    """Allow users to view and manage their favorite cities."""
    while True:
        clear_screen()
        favorite_ids = favorites.load_favorites()
        
        if not favorite_ids:
            print_line(
                """
═══════════════════════════

❤️ FAVORITES

═══════════════════════════

You haven't saved any cities yet.

Go explore Japan!

0. Back"""
            )
            choice = read_choice("\nChoose an option: ")
            
            if choice == "0":
                return
            continue
        
        # Load favorite cities
        city_list = []
        city_map = {}
        index = 1
        for city_id in sorted(favorite_ids):
            city = get_city(city_id)
            if city:
                city_list.append(f"{index}. {city.name}")
                city_map[str(index)] = city_id
                index += 1
        
        city_display = "\n".join(city_list)
        print_line(
            f"""
═══════════════════════════

❤️ FAVORITES

═══════════════════════════

{city_display}

0. Back"""
        )
        
        choice = read_choice("\nRemove which city? ")
        
        if choice == "0":
            return
        
        # Find the selected city
        city_id = city_map.get(choice)
        if not city_id:
            clear_screen()
            print_line("\n  Invalid option.\n")
            pause("Press ENTER to try again...")
            continue
        
        city = get_city(city_id)
        if city:
            if favorites.remove_favorite(city_id):
                clear_screen()
                print_line(f"\n  ✅ {city.name} removed successfully.\n")
            else:
                clear_screen()
                print_line(f"\n  Failed to remove {city.name}.\n")
            pause("Press ENTER to continue...")
