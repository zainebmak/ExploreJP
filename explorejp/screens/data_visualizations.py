"""Data visualization screens for ExploreJP."""

import webbrowser
from pathlib import Path

from explorejp.console import clear_screen, pause, print_line, read_choice
from explorejp.data.visualizations import (
    create_population_bar_chart_html,
    create_population_by_region_chart_html,
    create_region_pie_chart_html,
    create_top_5_chart_html,
    get_cities_by_region_data,
    get_population_by_city_data,
    get_population_by_region_data,
    get_top_5_cities_data,
    save_chart_html,
)


def show_data_visualizations_menu() -> None:
    """Show the data visualizations submenu."""
    while True:
        clear_screen()
        _render_menu()
        choice = read_choice("\nChoose an option: ")
        
        if choice == "0":
            return
        
        if choice == "1":
            show_population_by_city()
            continue
        
        if choice == "2":
            show_cities_by_region()
            continue
        
        if choice == "3":
            show_top_5_cities()
            continue
        
        if choice == "4":
            show_population_by_region()
            continue
        
        clear_screen()
        print_line("\n  Invalid option. Please choose a number from the menu.\n")
        pause("Press ENTER to try again...")


def _render_menu() -> None:
    print_line(
        """
═══════════════════════════════
      📊 DATA VISUALIZATIONS
═══════════════════════════════

1. 📈 Population by City

2. 🥧 Cities by Region

3. 🏆 Top 5 Most Populated Cities

4. 🗺️ Population by Region

0. Back

═══════════════════════════════"""
    )


def show_population_by_city() -> None:
    """Show population by city chart."""
    data = get_population_by_city_data()
    
    # Display ASCII chart
    clear_screen()
    print_line(
        """
═══════════════════════════════
      📈 POPULATION BY CITY
═══════════════════════════════

Population"""
    )
    
    max_pop = max(item[1] for item in data) if data else 1
    
    for city_name, pop_num, pop_str in data:
        bar_length = int((pop_num / max_pop) * 30)
        bar = "█" * bar_length
        print_line(f"{city_name:<12} {bar}")
    
    print_line("\n═══════════════════════════════")
    
    choice = read_choice("\nPress ENTER to view interactive chart, or 0 to go back: ")
    
    if choice == "0":
        return
    
    # Generate and open interactive chart
    html_content = create_population_bar_chart_html()
    file_path = save_chart_html(html_content, "population_by_city.html")
    webbrowser.open(f"file:///{file_path}")
    
    pause("\nPress ENTER to return to the menu...")


def show_cities_by_region() -> None:
    """Show cities by region pie chart."""
    data = get_cities_by_region_data()
    
    clear_screen()
    print_line(
        """
═══════════════════════════════
      🥧 CITIES BY REGION
═══════════════════════════════

Region Distribution"""
    )
    
    for region, count in sorted(data.items()):
        print_line(f"{region:<12} {count} cities")
    
    print_line("\n═══════════════════════════════")
    
    choice = read_choice("\nPress ENTER to view interactive chart, or 0 to go back: ")
    
    if choice == "0":
        return
    
    # Generate and open interactive chart
    html_content = create_region_pie_chart_html()
    file_path = save_chart_html(html_content, "cities_by_region.html")
    webbrowser.open(f"file:///{file_path}")
    
    pause("\nPress ENTER to return to the menu...")


def show_top_5_cities() -> None:
    """Show top 5 most populated cities."""
    data = get_top_5_cities_data()
    
    clear_screen()
    print_line(
        """
═══════════════════════════════
   🏆 TOP 5 MOST POPULATED CITIES
═══════════════════════════════

Population Ranking"""
    )
    
    for i, (city_name, pop_num, pop_str) in enumerate(data, 1):
        print_line(f"{i}. {city_name:<12} {pop_str}")
    
    print_line("\n═══════════════════════════════")
    
    choice = read_choice("\nPress ENTER to view interactive chart, or 0 to go back: ")
    
    if choice == "0":
        return
    
    # Generate and open interactive chart
    html_content = create_top_5_chart_html()
    file_path = save_chart_html(html_content, "top_5_cities.html")
    webbrowser.open(f"file:///{file_path}")
    
    pause("\nPress ENTER to return to the menu...")


def show_population_by_region() -> None:
    """Show population by region chart."""
    data = get_population_by_region_data()
    
    clear_screen()
    print_line(
        """
═══════════════════════════════
    🗺️ POPULATION BY REGION
═══════════════════════════════

Regional Population"""
    )
    
    max_pop = max(data.values()) if data else 1
    
    for region, pop_num in sorted(data.items(), key=lambda x: x[1], reverse=True):
        bar_length = int((pop_num / max_pop) * 30)
        bar = "█" * bar_length
        pop_str = f"{int(pop_num):,}"
        print_line(f"{region:<12} {bar} {pop_str}")
    
    print_line("\n═══════════════════════════════")
    
    choice = read_choice("\nPress ENTER to view interactive chart, or 0 to go back: ")
    
    if choice == "0":
        return
    
    # Generate and open interactive chart
    html_content = create_population_by_region_chart_html()
    file_path = save_chart_html(html_content, "population_by_region.html")
    webbrowser.open(f"file:///{file_path}")
    
    pause("\nPress ENTER to return to the menu...")
