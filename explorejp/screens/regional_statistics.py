from explorejp.console import clear_screen, pause, print_line, read_choice
from explorejp.data import get_regional_statistics


# Region emoji mapping
REGION_EMOJIS = {
    "Kanto": "🗼",
    "Kansai": "⛩",
    "Hokkaido": "❄",
    "Kyushu": "🌊",
    "Chugoku": "🏯",
    "Tohoku": "🌿",
}


def show_regional_statistics() -> None:
    """Display regional statistics using pandas calculations."""
    stats = get_regional_statistics()
    
    clear_screen()
    
    # Build the display
    regions_display = []
    for region in sorted(stats.keys()):
        emoji = REGION_EMOJIS.get(region, "📍")
        region_stats = stats[region]
        
        regions_display.append(
            f"{emoji} {region}\n"
            f"\n"
            f"Cities: {region_stats['cities']}\n"
            f"\n"
            f"Population: {region_stats['population']}"
        )
    
    separator = "\n" + "─" * 30 + "\n"
    full_display = separator.join(regions_display)
    
    print_line(
        f"""
═══════════════════════════════════════
       🌎 REGIONAL STATISTICS
═══════════════════════════════════════

{full_display}

═══════════════════════════════"""
    )
    
    pause("\nPress ENTER to return to the menu...")
