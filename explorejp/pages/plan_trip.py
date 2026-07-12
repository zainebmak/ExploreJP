"""Trip planning page for ExploreJP Streamlit app."""

import streamlit as st
import folium
from streamlit_folium import folium_static
from fpdf import FPDF
import pandas as pd
from explorejp.database import (
    create_itinerary,
    get_all_itineraries,
    get_itinerary_by_id,
    delete_itinerary,
    add_city_to_itinerary,
    get_itinerary_cities,
    remove_city_from_itinerary,
    clear_itinerary_cities,
    get_all_cities,
    get_cities_by_season,
    create_user_itinerary,
    get_user_itineraries,
)

# City coordinates for map visualization
CITY_COORDINATES = {
    "Tokyo": (35.6762, 139.6503),
    "Kyoto": (35.0116, 135.7681),
    "Osaka": (34.6937, 135.5023),
    "Sapporo": (43.0642, 141.3469),
    "Nara": (34.6851, 135.8048),
    "Fukuoka": (33.5904, 130.4017),
    "Hiroshima": (34.3853, 132.4553),
    "Kobe": (34.6901, 135.1956),
    "Yokohama": (35.4437, 139.6380),
    "Nagoya": (35.1815, 136.9066),
}


def _calculate_travel_distance(city1: str, city2: str) -> float:
    """Calculate approximate travel distance between two cities in km."""
    if city1 not in CITY_COORDINATES or city2 not in CITY_COORDINATES:
        return 0.0
    
    lat1, lon1 = CITY_COORDINATES[city1]
    lat2, lon2 = CITY_COORDINATES[city2]
    
    # Haversine formula
    from math import radians, cos, sin, sqrt, atan2
    
    R = 6371  # Earth's radius in km
    
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c


def _optimize_route(cities: list[str]) -> list[str]:
    """Optimize route to minimize total travel distance using nearest neighbor algorithm."""
    if not cities:
        return []
    if len(cities) == 1:
        return cities
    
    # Start with first city
    optimized = [cities[0]]
    remaining = cities[1:]
    
    while remaining:
        last_city = optimized[-1]
        # Find nearest city
        nearest_idx = 0
        nearest_dist = float('inf')
        
        for idx, city in enumerate(remaining):
            dist = _calculate_travel_distance(last_city, city)
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_idx = idx
        
        optimized.append(remaining.pop(nearest_idx))
    
    return optimized


def _create_itinerary_map(cities: list[dict]) -> folium.Map:
    """Create an interactive map with the itinerary route."""
    if not cities:
        return None
    
    # Create map centered on Japan
    m = folium.Map(location=[36.2048, 138.2529], zoom_start=5, tiles="OpenStreetMap")
    
    # Add markers for each city
    for idx, city in enumerate(cities):
        city_name = city['name']
        if city_name in CITY_COORDINATES:
            lat, lon = CITY_COORDINATES[city_name]
            
            # Create popup with city info
            popup_html = f"""
            <div style="font-family: Arial, sans-serif;">
                <h4 style="margin: 0; color: #6C0820;">{city_name}</h4>
                <p style="margin: 5px 0;"><strong>Day {idx + 1}</strong></p>
                <p style="margin: 5px 0;">{city['known_for']}</p>
                <p style="margin: 5px 0; color: #666;">{city['region']}</p>
            </div>
            """
            
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"Day {idx + 1}: {city_name}",
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(m)
    
    # Draw route lines
    if len(cities) > 1:
        coordinates = []
        for city in cities:
            city_name = city['name']
            if city_name in CITY_COORDINATES:
                coordinates.append(CITY_COORDINATES[city_name])
        
        if len(coordinates) > 1:
            folium.PolyLine(
                locations=coordinates,
                color="#6C0820",
                weight=3,
                opacity=0.8,
                dash_array='5, 5'
            ).add_to(m)
    
    return m


def _remove_emojis(text: str) -> str:
    """Remove emojis from text to make it PDF-compatible."""
    import re
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

def _export_itinerary_to_pdf(itinerary: dict, cities: list[dict]) -> bytes:
    """Export itinerary to PDF."""
    pdf = FPDF()
    pdf.add_page()
    
    # Set font (using built-in fonts)
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 15, f"Japan Trip: {_remove_emojis(itinerary['name'])}", ln=True, align="C")
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"{itinerary['start_date']} to {itinerary['end_date']}", ln=True, align="C")
    pdf.cell(0, 10, f"Season: {_remove_emojis(itinerary['season'])}", ln=True, align="C")
    pdf.cell(0, 10, f"Budget: ${itinerary['budget']:,.2f}" if itinerary['budget'] else "Budget: Not set", ln=True, align="C")
    
    pdf.ln(15)
    
    # Add itinerary details
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Itinerary", ln=True)
    
    pdf.set_font("Arial", "", 11)
    for idx, city in enumerate(cities, 1):
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, f"Day {idx}: {_remove_emojis(city['name'])}", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 6, f"Region: {_remove_emojis(city['region'])}", ln=True)
        pdf.cell(0, 6, f"Best Season: {_remove_emojis(city['best_season'])}", ln=True)
        pdf.cell(0, 6, f"Cost of Living: {_remove_emojis(city['cost_of_living'])}", ln=True)
        pdf.multi_cell(0, 6, f"Known For: {_remove_emojis(city['known_for'])}")
        pdf.ln(5)
    
    # Add packing list
    pdf.ln(10)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Packing List", ln=True)
    
    pdf.set_font("Arial", "", 10)
    packing_items = _get_packing_list(itinerary['season'], itinerary['interests'])
    for item in packing_items:
        pdf.cell(0, 6, f"[ ] {_remove_emojis(item)}", ln=True)
    
    # Generate PDF as bytes
    pdf_bytes = pdf.output(dest='S')
    if isinstance(pdf_bytes, str):
        return pdf_bytes.encode('latin-1')
    elif isinstance(pdf_bytes, bytearray):
        return bytes(pdf_bytes)
    return pdf_bytes


def show():
    """Display the trip planning page."""
    
    st.markdown("## 🧳 Plan Your Trip")
    st.markdown("Create your perfect Japan itinerary with smart recommendations")
    
    # Initialize session state
    if "current_itinerary_id" not in st.session_state:
        st.session_state.current_itinerary_id = None
    
    # Tab navigation
    tab1, tab2, tab3 = st.tabs(["Create Trip", "My Trips", "Trip Builder"])
    
    with tab1:
        _show_create_trip()
    
    with tab2:
        _show_my_trips()
    
    with tab3:
        if st.session_state.current_itinerary_id:
            _show_trip_builder()
        else:
            st.info("Select or create a trip from the 'My Trips' tab to start building your itinerary.")


def _show_create_trip():
    """Show the create trip form."""
    
    st.markdown("### 📝 Create New Trip")
    
    with st.form("create_trip_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            trip_name = st.text_input("Trip Name*", placeholder="e.g., Spring Cherry Blossom Tour")
            start_date = st.date_input("Start Date*")
        
        with col2:
            season = st.selectbox("Season*", ["Spring", "Summer", "Autumn", "Winter"])
            end_date = st.date_input("End Date*")
        
        interests = st.multiselect(
            "Interests*",
            ["Culture & History", "Nature & Scenery", "Food & Dining", "Shopping", "Nightlife", "Temples & Shrines", "Modern Cities", "Traditional Arts", "Beaches", "Mountains"],
            help="Select your travel interests to get personalized recommendations"
        )
        
        budget = st.number_input("Budget (USD)", min_value=0, value=2000, step=100)
        
        submitted = st.form_submit_button("Create Trip", use_container_width=True)
        
        if submitted:
            if not trip_name or not interests:
                st.error("Please fill in all required fields.")
            else:
                interests_str = ", ".join(interests)
                uid = st.session_state.get("user", {}).get("id")
                if uid:
                    itinerary_id = create_user_itinerary(
                        user_id=uid,
                        name=trip_name,
                        start_date=start_date.strftime("%Y-%m-%d"),
                        end_date=end_date.strftime("%Y-%m-%d"),
                        season=season,
                        interests=interests_str,
                        budget=budget,
                    )
                else:
                    itinerary_id = create_itinerary(
                        name=trip_name,
                        start_date=start_date.strftime("%Y-%m-%d"),
                        end_date=end_date.strftime("%Y-%m-%d"),
                        season=season,
                        interests=interests_str,
                        budget=budget,
                    )
                st.session_state.current_itinerary_id = itinerary_id
                st.success(f"Trip '{trip_name}' created successfully!")
                st.rerun()


def _show_my_trips():
    """Show saved trips."""
    
    st.markdown("### 📂 My Saved Trips")

    uid = st.session_state.get("user", {}).get("id") if st.session_state.get("user") else None
    if uid:
        itineraries = get_user_itineraries(uid)
    else:
        itineraries = get_all_itineraries()
    
    if not itineraries:
        st.info("No trips saved yet. Create your first trip in the 'Create Trip' tab.")
        return
    
    for itinerary in itineraries:
        with st.expander(f"🗓️ {itinerary['name']} ({itinerary['start_date']} to {itinerary['end_date']})"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Season:** {itinerary['season']}")
                st.markdown(f"**Budget:** ${itinerary['budget']:,.2f}" if itinerary['budget'] else "**Budget:** Not set")
            
            with col2:
                st.markdown(f"**Interests:** {itinerary['interests']}")
                cities_count = len(get_itinerary_cities(itinerary['id']))
                st.markdown(f"**Cities:** {cities_count}")
            
            with col3:
                if st.button("Edit Trip", key=f"edit_{itinerary['id']}", use_container_width=True):
                    st.session_state.current_itinerary_id = itinerary['id']
                    st.rerun()
                
                if st.button("Delete Trip", key=f"delete_{itinerary['id']}", use_container_width=True):
                    delete_itinerary(itinerary['id'])
                    if st.session_state.current_itinerary_id == itinerary['id']:
                        st.session_state.current_itinerary_id = None
                    st.success("Trip deleted successfully!")
                    st.rerun()


def _show_trip_builder():
    """Show the trip builder interface."""
    
    itinerary = get_itinerary_by_id(st.session_state.current_itinerary_id)
    if not itinerary:
        st.error("Trip not found.")
        return
    
    st.markdown(f"### 🏗️ Building: {itinerary['name']}")
    
    # Tab navigation for trip builder
    builder_tab1, builder_tab2, builder_tab3 = st.tabs(["Add Cities", "Map & Route", "Export"])
    
    with builder_tab1:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### 🎯 Recommended Cities")
            
            # Get cities based on season
            season_cities = get_cities_by_season(itinerary['season'])
            
            # Filter by interests (simple keyword matching)
            interests = itinerary['interests'].lower().split(', ')
            recommended_cities = []
            
            for city in season_cities:
                city_known_for = city['known_for'].lower()
                if any(interest in city_known_for for interest in interests):
                    recommended_cities.append(city)
            
            # If no matches, show all season cities
            if not recommended_cities:
                recommended_cities = season_cities
            
            for city in recommended_cities[:10]:  # Show top 10
                with st.expander(f"🏙️ {city['name']}"):
                    st.markdown(f"**Region:** {city['region']}")
                    st.markdown(f"**Known For:** {city['known_for']}")
                    st.markdown(f"**Cost:** {city['cost_of_living']}")
                    
                    # Add to itinerary
                    current_cities = get_itinerary_cities(itinerary['id'])
                    next_day = len(current_cities) + 1
                    
                    if st.button(f"Add to Day {next_day}", key=f"add_{city['id']}", use_container_width=True):
                        add_city_to_itinerary(itinerary['id'], city['id'], next_day)
                        st.success(f"Added {city['name']} to your trip!")
                        st.rerun()
        
        with col2:
            st.markdown("#### 📋 Your Itinerary")
            
            itinerary_cities = get_itinerary_cities(itinerary['id'])
            
            if not itinerary_cities:
                st.info("No cities added yet. Select cities from the recommendations on the left.")
            else:
                for idx, city in enumerate(itinerary_cities, 1):
                    st.markdown(f"""
                    <div style="padding: 16px; border: 1px solid #e0e0e0; border-radius: 8px; margin-bottom: 12px; background: white;">
                        <h4 style="margin: 0 0 8px 0; color: #6C0820;">Day {idx}: {city['name']}</h4>
                        <p style="margin: 4px 0; color: #666;">📍 {city['region']} | 💰 {city['cost_of_living']}</p>
                        <p style="margin: 4px 0; color: #666;">🎯 {city['known_for']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button("Remove", key=f"remove_{idx}_{city['id']}", use_container_width=True):
                            remove_city_from_itinerary(itinerary['id'], city['id'])
                            st.success(f"Removed {city['name']} from your trip.")
                            st.rerun()
                    with col_btn2:
                        if st.button("Add Notes", key=f"notes_{idx}_{city['id']}", use_container_width=True):
                            st.session_state[f"notes_{idx}_{city['id']}"] = True
            
            # Trip summary
            st.markdown("---")
            st.markdown("#### 💰 Trip Summary")
            
            total_days = len(itinerary_cities)
            daily_budget = itinerary['budget'] / total_days if itinerary['budget'] and total_days > 0 else 0
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Days", total_days)
                st.metric("Daily Budget", f"${daily_budget:,.2f}" if daily_budget else "N/A")
            with col2:
                st.metric("Total Budget", f"${itinerary['budget']:,.2f}" if itinerary['budget'] else "Not set")
            
            # Packing list suggestion
            st.markdown("---")
            st.markdown("#### 🎒 Packing List Suggestions")
            
            packing_items = _get_packing_list(itinerary['season'], itinerary['interests'])
            for item in packing_items:
                st.checkbox(item, key=f"pack_{item}")
            
            st.markdown("---")
            if st.button("Clear All Cities", use_container_width=True):
                clear_itinerary_cities(itinerary['id'])
                st.success("All cities removed from itinerary.")
                st.rerun()
    
    with builder_tab2:
        st.markdown("#### 🗺️ Interactive Map & Route Optimization")
        
        itinerary_cities = get_itinerary_cities(itinerary['id'])
        
        if not itinerary_cities:
            st.info("Add cities to your itinerary to see the map and route.")
        else:
            # Route optimization button
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Optimize Route", use_container_width=True):
                    city_names = [city['name'] for city in itinerary_cities]
                    optimized_names = _optimize_route(city_names)
                    
                    # Clear and re-add cities in optimized order
                    clear_itinerary_cities(itinerary['id'])
                    for idx, city_name in enumerate(optimized_names, 1):
                        # Find city ID
                        for city in itinerary_cities:
                            if city['name'] == city_name:
                                add_city_to_itinerary(itinerary['id'], city['id'], idx)
                                break
                    
                    st.success("Route optimized for minimal travel distance!")
                    st.rerun()
            
            with col2:
                # Calculate total distance
                total_distance = 0
                city_names = [city['name'] for city in itinerary_cities]
                for i in range(len(city_names) - 1):
                    total_distance += _calculate_travel_distance(city_names[i], city_names[i + 1])
                
                st.metric("Total Travel Distance", f"{total_distance:.0f} km")
            
            st.markdown("---")
            
            # Create and display map
            itinerary_map = _create_itinerary_map(itinerary_cities)
            if itinerary_map:
                folium_static(itinerary_map, width=700, height=500)
            else:
                st.warning("Unable to create map. Some cities may not have coordinates.")
    
    with builder_tab3:
        st.markdown("#### 📄 Export Your Itinerary")
        
        itinerary_cities = get_itinerary_cities(itinerary['id'])
        
        if not itinerary_cities:
            st.info("Add cities to your itinerary before exporting.")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📥 Download PDF", use_container_width=True):
                    try:
                        pdf_bytes = _export_itinerary_to_pdf(itinerary, itinerary_cities)
                        st.download_button(
                            label="Save PDF",
                            data=pdf_bytes,
                            file_name=f"{itinerary['name']}_itinerary.pdf",
                            mime="application/pdf"
                        )
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")
            
            with col2:
                st.markdown("#### Export Options")
                st.markdown("- **PDF**: Complete itinerary with packing list")
                st.markdown("- **Map**: Interactive route visualization")
                st.markdown("- **Route**: Optimized travel path")


def _get_packing_list(season: str, interests: str) -> list[str]:
    """Generate packing list based on season and interests."""
    
    base_items = [
        "Passport & Travel Documents",
        "Phone charger & power bank",
        "Comfortable walking shoes",
        "Toiletries",
        "Medications",
    ]
    
    season_items = {
        "Spring": ["Light jacket", "Umbrella", "Layers"],
        "Summer": ["Sunscreen", "Hat", "Light clothing", "Insect repellent"],
        "Autumn": ["Warm layers", "Comfortable shoes for walking", "Light jacket"],
        "Winter": ["Warm coat", "Scarf & gloves", "Thermal underwear", "Waterproof boots"],
    }
    
    interest_items = []
    interests_lower = interests.lower()
    
    if "nature" in interests_lower or "mountains" in interests_lower:
        interest_items.extend(["Hiking boots", "Backpack", "Water bottle"])
    if "beaches" in interests_lower:
        interest_items.extend(["Swimwear", "Beach towel", "Sandals"])
    if "temples" in interests_lower or "culture" in interests_lower:
        interest_items.extend(["Modest clothing for temples", "Comfortable shoes"])
    
    return base_items + season_items.get(season, []) + interest_items
