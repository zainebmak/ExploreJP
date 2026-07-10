"""Explore cities page for ExploreJP Streamlit app."""

import streamlit as st
import pandas as pd
from explorejp.config import COLORS
from explorejp.data.favorites import (
    add_favorite,
    get_favorite_ids,
    get_favorites,
    remove_favorite,
)
from explorejp.database import (
    get_all_cities,
    search_cities,
    get_cities_by_region,
    get_cities_by_season,
    get_all_regions,
    get_all_seasons,
    get_city_by_id,
    get_cities_count_by_region,
    get_cities_count_by_season,
)
from explorejp.pages.data_visualizations import (
    get_cities_df,
    render_population_distribution,
    render_cost_of_living,
    render_regional_overview,
    render_seasonal_preferences,
    render_city_comparison_chart,
)

CITY_IMAGE_URLS = {
    "Tokyo": "https://i.pinimg.com/736x/76/45/d6/7645d66eecaa75d475a0a3878a0b6d4e.jpg",
    "Kyoto": "https://i.pinimg.com/1200x/5c/b8/2d/5cb82d83bc50e60e7bcd7d6fed32d2ca.jpg",
    "Osaka": "https://i.pinimg.com/1200x/0e/fd/0c/0efd0c03b5d991764de6e1f6062a9867.jpg",
    "Sapporo": "https://i.pinimg.com/1200x/4e/57/eb/4e57eba5f801825791e821fbacbc57db.jpg",
    "Nara": "https://i.pinimg.com/1200x/c3/22/4f/c3224f143c8f07d1077a12ed3de23c5d.jpg",
    "Fukuoka": "https://i.pinimg.com/1200x/ae/27/30/ae27305e760e790c49f0d4b83ba27abf.jpg",
    "Hiroshima": "https://i.pinimg.com/1200x/86/8d/21/868d2104a4cd9c10fc5a2f77e670d6a2.jpg",
}


def _get_city_image_url(city_name: str) -> str:
    return CITY_IMAGE_URLS.get(city_name, "https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=800&q=80")


def _favorite_button_label(city_id, favorite_ids) -> str:
    return "💖 Saved" if city_id in favorite_ids else "🤍 Save"


def _render_page_header() -> None:
    st.markdown('<div class="explore-page-header"><h1 class="explore-title">🗾 Explore Japan\'s Cities</h1><p class="explore-subtitle">Discover amazing destinations, compare cities, and build your perfect Japan travel itinerary</p></div>', unsafe_allow_html=True)


def _render_summary_stats(total_cities: int, regions: int, seasons: int, favorites_count: int) -> None:
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.markdown(f'<div class="stat-card"><div class="stat-icon">🏙️</div><div class="stat-number">{total_cities}</div><div class="stat-label">Cities</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><div class="stat-icon">🗺️</div><div class="stat-number">{regions}</div><div class="stat-label">Regions</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><div class="stat-icon">🌸</div><div class="stat-number">{seasons}</div><div class="stat-label">Seasons</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="stat-card stat-card-highlight"><div class="stat-icon">❤️</div><div class="stat-number">{favorites_count}</div><div class="stat-label">My Favorites</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def _render_action_menu(selected_action: str) -> None:
    sections = [
        ("📍", "Browse All Cities", "Browse the full city list with filters"),
        ("🔎", "Discover a City", "Search by name and explore details"),
        ("🌎", "Explore by Region", "Find cities by Japanese region"),
        ("🌸", "Explore by Season", "See cities by best season to visit"),
        ("❤️", "My Japan", "Review your saved favorites"),
        ("⚖️", "Compare Cities", "Compare stats between two cities"),
        ("📊", "City Analytics", "View data insights and trends"),
    ]

    # Create a responsive grid of action cards
    st.markdown('<div class="action-menu-container">', unsafe_allow_html=True)
    
    # First row - 4 cards
    cols1 = st.columns(4, gap="medium")
    for idx, (icon, action, description) in enumerate(sections[:4]):
        with cols1[idx]:
            button_label = f"{icon}\n\n{action}"
            button_key = f"menu_action_{idx}_{action.replace(' ', '_')}"
            if st.button(button_label, key=button_key, help=description, use_container_width=True):
                st.session_state.explore_cities_action = action
                # Clear any previous city selection when changing actions
                if "selected_city_id" in st.session_state:
                    del st.session_state.selected_city_id
    
    # Second row - 3 cards centered
    st.markdown('<br/>', unsafe_allow_html=True)
    col_spacer1, col_action5, col_action6, col_action7, col_spacer2 = st.columns([0.5, 1, 1, 1, 0.5], gap="medium")
    for idx, (col, (icon, action, description)) in enumerate(zip([col_action5, col_action6, col_action7], sections[4:]), start=4):
        with col:
            button_label = f"{icon}\n\n{action}"
            button_key = f"menu_action_{idx}_{action.replace(' ', '_')}"
            if st.button(button_label, key=button_key, help=description, use_container_width=True):
                st.session_state.explore_cities_action = action
                # Clear any previous city selection when changing actions
                if "selected_city_id" in st.session_state:
                    del st.session_state.selected_city_id
    
    st.markdown('</div>', unsafe_allow_html=True)


def show() -> None:
    # Initialize session state with more robust handling
    if "explore_cities_action" not in st.session_state:
        st.session_state.explore_cities_action = "Browse All Cities"

    _render_page_header()
    
    _render_summary_stats(
        total_cities=len(get_all_cities()),
        regions=len(get_all_regions()),
        seasons=len(get_all_seasons()),
        favorites_count=len(get_favorite_ids()),
    )

    st.markdown("<br/>", unsafe_allow_html=True)
    _render_action_menu(st.session_state.explore_cities_action)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    action = st.session_state.explore_cities_action
    st.markdown(f'<div class="current-view-header"><span class="view-label">Current View:</span> <span class="view-name">{action}</span></div>', unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)

    # Route to the appropriate function based on action
    action_routes = {
        "Browse All Cities": _show_browse_all_cities,
        "Discover a City": _show_discover_city,
        "Explore by Region": _show_explore_by_region,
        "Explore by Season": _show_explore_by_season,
        "My Japan": _show_my_japan,
        "Compare Cities": _show_compare_cities,
        "City Analytics": _show_city_analytics,
    }
    
    # Call the appropriate function
    if action in action_routes:
        action_routes[action]()
    else:
        # Fallback to browse all cities if unknown action
        st.session_state.explore_cities_action = "Browse All Cities"
        _show_browse_all_cities()


def _show_browse_all_cities() -> None:
    all_cities = get_all_cities()
    favorite_ids = set(get_favorite_ids())

    # Enhanced filter section
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        search_query = st.text_input("🔍 Search Cities", placeholder="Enter city name...", key="browse_search", label_visibility="collapsed")
    with col2:
        selected_region = st.selectbox("📍 Region", ["All Regions"] + get_all_regions(), key="browse_region")
    with col3:
        selected_season = st.selectbox("🌸 Season", ["All Seasons"] + get_all_seasons(), key="browse_season")
    st.markdown('</div>', unsafe_allow_html=True)

    # Apply filters
    filtered_cities = all_cities
    if search_query:
        filtered_cities = [dict(city) for city in search_cities(search_query)]
    if selected_region != "All Regions":
        region_cities = [dict(city) for city in get_cities_by_region(selected_region)]
        if search_query:
            filtered_ids = {city["id"] for city in filtered_cities}
            filtered_cities = [city for city in region_cities if city["id"] in filtered_ids]
        else:
            filtered_cities = region_cities
    if selected_season != "All Seasons":
        season_cities = [dict(city) for city in get_cities_by_season(selected_season)]
        filtered_ids = {city["id"] for city in filtered_cities}
        filtered_cities = [city for city in season_cities if city["id"] in filtered_ids]

    st.markdown(f'<div class="results-count">Found <strong>{len(filtered_cities)}</strong> cities</div>', unsafe_allow_html=True)
    
    if not filtered_cities:
        st.markdown('<div class="empty-favorites"><div class="empty-icon">🔍</div><h3>No cities found</h3><p>Try adjusting your filters to see more results</p></div>', unsafe_allow_html=True)
        return

    # Display cities in enhanced card layout
    st.markdown('<div class="cities-grid">', unsafe_allow_html=True)
    cols_per_row = 3
    for i in range(0, len(filtered_cities), cols_per_row):
        cols = st.columns(cols_per_row, gap="large")
        for idx, city in enumerate(filtered_cities[i:i + cols_per_row]):
            with cols[idx]:
                known_for_list = city["known_for"].split("|")
                known_for_display = ", ".join(known_for_list[:2])
                if len(known_for_list) > 2:
                    known_for_display += "..."

                is_favorite = city["id"] in favorite_ids
                fav_icon = "💖" if is_favorite else "🤍"
                
                st.markdown(f'<div class="enhanced-city-card"><img class="enhanced-city-image" src="{_get_city_image_url(city["name"])}" alt="{city["name"]}"><div class="enhanced-city-content"><h3 class="enhanced-city-name">{city["name"]}</h3><div class="enhanced-city-badges"><span class="enhanced-badge">{city["region"]}</span><span class="enhanced-badge">{city["best_season"]}</span></div><p class="enhanced-city-info"><strong>Cost:</strong> {city["cost_of_living"]} | <strong>Population:</strong> {city["population"]}</p><p class="enhanced-city-desc">{known_for_display}</p></div></div>', unsafe_allow_html=True)
                
                btn_col1, btn_col2 = st.columns([3, 1])
                with btn_col1:
                    if st.button("👁️ View Details", key=f"view_{city['id']}", use_container_width=True):
                        st.session_state.selected_city_id = city["id"]
                        st.rerun()
                with btn_col2:
                    if st.button(fav_icon, key=f"fav_{city['id']}", use_container_width=True):
                        if city["id"] in favorite_ids:
                            remove_favorite(city["id"])
                        else:
                            add_favorite(city["id"])
                        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    _show_city_details()


def _show_city_details() -> None:
    if "selected_city_id" not in st.session_state or not st.session_state.selected_city_id:
        return

    city = get_city_by_id(st.session_state.selected_city_id)
    if not city:
        return

    favorite_ids = set(get_favorite_ids())
    city = dict(city)
    known_for_list = city["known_for"].split("|")

    st.markdown("<br/><br/>", unsafe_allow_html=True)
    st.markdown(f'<div class="city-detail-modal"><div class="modal-header"><h2>📍 {city["name"]}</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f'<div class="detail-section"><img class="detail-image" src="{_get_city_image_url(city["name"])}" alt="{city["name"]}"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detail-section"><h3>About {city["name"]}</h3><p><strong>🌍 Region:</strong> {city["region"]}</p><p><strong>🌸 Best Season:</strong> {city["best_season"]}</p><p><strong>👥 Population:</strong> {city["population"]}</p><p><strong>💰 Cost of Living:</strong> {city["cost_of_living"]}</p></div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="detail-section"><h3>Known For</h3><ul class="known-for-list">', unsafe_allow_html=True)
        for item in known_for_list:
            st.markdown(f'<li>{item}</li>', unsafe_allow_html=True)
        st.markdown('</ul></div>', unsafe_allow_html=True)
        
        is_favorite = city["id"] in favorite_ids
        fav_label = "💖 Remove from Favorites" if is_favorite else "🤍 Add to Favorites"
        if st.button(fav_label, key=f"detail_fav_{city['id']}", use_container_width=True):
            if city["id"] in favorite_ids:
                remove_favorite(city["id"])
            else:
                add_favorite(city["id"])
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("✕ Close Details", key="close_details", use_container_width=False):
        del st.session_state.selected_city_id
        st.rerun()


def _show_discover_city() -> None:
    st.markdown('<div class="discover-section">', unsafe_allow_html=True)
    search_query = st.text_input("🔎 Search for a city", placeholder="Type city name (e.g., Tokyo, Kyoto, Osaka...)", key="discover_search")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not search_query:
        st.markdown('<div class="empty-favorites"><div class="empty-icon">�</div><h3>Discover Your Next Japanese Adventure</h3><p>Use the search box above to discover cities by name.<br/>Find hidden gems and popular destinations across Japan!</p></div>', unsafe_allow_html=True)
        return

    results = [dict(city) for city in search_cities(search_query)]
    if not results:
        st.markdown('<div class="empty-favorites"><div class="empty-icon">🔍</div><h3>No cities found</h3><p>Try a different name or check your spelling.<br/>We have cities from all regions of Japan!</p></div>', unsafe_allow_html=True)
        return

    favorite_ids = set(get_favorite_ids())
    
    st.markdown(f'<div class="results-count">Found <strong>{len(results)}</strong> matching {("city" if len(results) == 1 else "cities")}</div>', unsafe_allow_html=True)
    
    for city in results:
        known_for_formatted = city["known_for"].replace("|", " • ")
        st.markdown(f'<div class="search-result-card"><h3 class="result-city-name">🏙️ {city["name"]}</h3><p class="result-info"><strong>📍 Region:</strong> {city["region"]} | <strong>🌸 Best Season:</strong> {city["best_season"]} | <strong>💰 Cost:</strong> {city["cost_of_living"]} | <strong>👥 Population:</strong> {city["population"]}</p><p class="result-desc">{known_for_formatted}</p></div>', unsafe_allow_html=True)
        
        is_favorite = city["id"] in favorite_ids
        fav_label = "💖 Saved to My Japan" if is_favorite else "🤍 Save to My Japan"
        if st.button(fav_label, key=f"discover_fav_{city['id']}", use_container_width=True):
            if city["id"] in favorite_ids:
                remove_favorite(city["id"])
            else:
                add_favorite(city["id"])
            st.rerun()
        st.markdown("<br/>", unsafe_allow_html=True)


def _show_explore_by_region() -> None:
    cities_df = get_cities_df()
    region_counts = get_cities_count_by_region()

    st.markdown('<div class="region-section">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #6C0820; margin-bottom: 20px; font-size: 1.8rem;">🌎 Explore by Region</h3>', unsafe_allow_html=True)
    selected_region = st.selectbox("📍 Choose a region to explore", ["Select a region..."] + get_all_regions(), key="region_filter")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if selected_region == "Select a region...":
        st.markdown('<div class="empty-favorites"><div class="empty-icon">�️</div><h3>Discover Regions of Japan</h3><p>Select a region above to see cities and regional statistics.<br/>From snowy Hokkaido to tropical Okinawa!</p></div>', unsafe_allow_html=True)
    else:
        region_cities = [dict(city) for city in get_cities_by_region(selected_region)]
        st.markdown(f'<div class="region-header"><h3>📍 Cities in {selected_region} ({len(region_cities)} {("city" if len(region_cities) == 1 else "cities")})</h3></div>', unsafe_allow_html=True)
        
        cols = st.columns(3, gap="medium")
        for idx, city in enumerate(region_cities):
            with cols[idx % 3]:
                st.markdown(f'<div class="region-city-card"><h4>{city["name"]}</h4><p>🌸 {city["best_season"]} • 💰 {city["cost_of_living"]}</p></div>', unsafe_allow_html=True)

    st.markdown("<br/><br/>", unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">📊 Regional Overview</h3>', unsafe_allow_html=True)
    render_regional_overview(cities_df, region_counts)


def _show_explore_by_season() -> None:
    cities_df = get_cities_df()
    season_counts = get_cities_count_by_season()

    st.markdown('<div class="season-section">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #6C0820; margin-bottom: 20px; font-size: 1.8rem;">🌸 Explore by Season</h3>', unsafe_allow_html=True)
    selected_season = st.selectbox("� Choose a season to explore", ["Select a season..."] + get_all_seasons(), key="season_filter")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if selected_season == "Select a season...":
        st.markdown('<div class="empty-favorites"><div class="empty-icon">🌸</div><h3>Explore Japan by Season</h3><p>Select a season above to see the best cities to visit.<br/>Cherry blossoms in spring, festivals in summer, foliage in fall, snow in winter!</p></div>', unsafe_allow_html=True)
    else:
        season_cities = [dict(city) for city in get_cities_by_season(selected_season)]
        st.markdown(f'<div class="season-header"><h3>🌸 Best Cities for {selected_season} ({len(season_cities)} {("city" if len(season_cities) == 1 else "cities")})</h3></div>', unsafe_allow_html=True)
        
        cols = st.columns(3, gap="medium")
        for idx, city in enumerate(season_cities):
            with cols[idx % 3]:
                st.markdown(f'<div class="season-city-card"><h4>{city["name"]}</h4><p>📍 {city["region"]} • 💰 {city["cost_of_living"]}</p></div>', unsafe_allow_html=True)

    st.markdown("<br/><br/>", unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">📊 Seasonal Distribution</h3>', unsafe_allow_html=True)
    render_seasonal_preferences(cities_df, season_counts)


def _show_my_japan() -> None:
    favorites_list = get_favorites()
    
    if not favorites_list:
        st.markdown('<div class="empty-favorites"><div class="empty-icon">❤️</div><h3>Your My Japan list is empty</h3><p>Start adding cities to build your perfect Japan itinerary!<br/>Explore cities and click the 🤍 button to save your favorites.</p></div>', unsafe_allow_html=True)
        return

    st.markdown(f'<div class="favorites-header"><h3>❤️ My Japan Collection ({len(favorites_list)} {("city" if len(favorites_list) == 1 else "cities")})</h3></div>', unsafe_allow_html=True)

    cols_per_row = 2
    for i in range(0, len(favorites_list), cols_per_row):
        cols = st.columns(cols_per_row, gap="large")
        for idx, city in enumerate(favorites_list[i:i + cols_per_row]):
            with cols[idx]:
                known_for = city['known_for'].replace("|", " • ")
                st.markdown(f'<div class="favorite-city-card"><img class="favorite-city-image" src="{_get_city_image_url(city["name"])}" alt="{city["name"]}"><div class="favorite-city-content"><h3 class="favorite-city-name">{city["name"]}</h3><div class="favorite-city-badges"><span class="enhanced-badge">📍 {city["region"]}</span><span class="enhanced-badge">🌸 {city["best_season"]}</span><span class="enhanced-badge">💰 {city["cost_of_living"]}</span></div><p class="favorite-city-desc">{known_for}</p></div></div>', unsafe_allow_html=True)
                
                if st.button("💔 Remove from Favorites", key=f"myjapan_remove_{city['id']}", use_container_width=True):
                    remove_favorite(city['id'])
                    st.rerun()


def _show_compare_cities() -> None:
    cities_df = get_cities_df()
    city_names = sorted(cities_df["name"].tolist())

    st.markdown('<div class="compare-section">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #6C0820; margin-bottom: 24px; font-size: 1.8rem;">⚖️ Compare Two Cities</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        city1 = st.selectbox("🏙️ First City", city_names, key="compare_city1", index=0)
    with col2:
        city2 = st.selectbox("🏙️ Second City", city_names, key="compare_city2", index=min(1, len(city_names) - 1))
    st.markdown('</div>', unsafe_allow_html=True)

    if city1 == city2:
        st.markdown('<div class="empty-favorites"><div class="empty-icon">⚠️</div><h3>Please select different cities</h3><p>Choose two different cities to compare their features</p></div>', unsafe_allow_html=True)
        return

    city1_data = cities_df[cities_df["name"] == city1].iloc[0]
    city2_data = cities_df[cities_df["name"] == city2].iloc[0]

    # Enhanced comparison table
    st.markdown(f'<div class="comparison-header"><h3>📊 {city1} vs {city2}</h3></div>', unsafe_allow_html=True)
    
    comparison_df = pd.DataFrame({
        "Attribute": ["🏙️ City", "👥 Population", "📍 Region", "🌸 Best Season", "💰 Cost of Living"],
        city1: [city1, city1_data["population"], city1_data["region"], city1_data["best_season"], city1_data["cost_of_living"]],
        city2: [city2, city2_data["population"], city2_data["region"], city2_data["best_season"], city2_data["cost_of_living"]],
    })

    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">� Visual Comparison</h3>', unsafe_allow_html=True)
    render_city_comparison_chart(city1_data, city2_data, city1, city2)


def _show_city_analytics() -> None:
    st.markdown('<div class="analytics-header"><h3 style="text-align: center; color: #6C0820; font-size: 2rem; margin-bottom: 16px;">📊 City Analytics Dashboard</h3><p style="text-align: center; color: #666; margin-bottom: 0;">Explore data insights and trends across Japanese cities</p></div>', unsafe_allow_html=True)
    cities_df = get_cities_df()

    chart_choice = st.selectbox("📈 Select analytics view", ["Population Distribution", "Cost of Living Distribution"], key="city_analytics_choice")

    st.markdown("<br/>", unsafe_allow_html=True)
    if chart_choice == "Population Distribution":
        st.markdown('<h3 class="chart-title">👥 Population Distribution</h3>', unsafe_allow_html=True)
        render_population_distribution(cities_df)
    else:
        st.markdown('<h3 class="chart-title">💰 Cost of Living Distribution</h3>', unsafe_allow_html=True)
        render_cost_of_living(cities_df)
