"""Cherry Blossom Guide page for ExploreJP Streamlit app."""

import streamlit as st
import sys
import datetime

try:
    import folium
    from streamlit_folium import folium_static
    _map_available = True
except ImportError:
    _map_available = False

try:
    from explorejp.database import (
        get_cherry_blossom_cities,
        get_cities_by_bloom_month,
        get_cherry_blossom_city_by_id,
        get_sakura_spots,
        get_sakura_forecast,
    )
except ImportError as e:
    st.error(f"Import error: {e}\n\nPython: {sys.executable}\n\nPath: {sys.path}")
    st.stop()


def show():
    """Display the cherry blossom guide page."""

    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("🏠 Back to Home", key="back_home_cherry", use_container_width=True):
            st.session_state.page = "🏠 Home"
            st.rerun()

    if "sakura_section" not in st.session_state:
        st.session_state.sakura_section = "home"

    section = st.session_state.sakura_section

    if section == "home":
        _show_home()
    elif section == "calendar":
        _show_bloom_calendar()
    elif section == "spots":
        _show_viewing_spots()
    elif section == "map":
        _show_sakura_map()
    elif section == "forecast":
        _show_bloom_forecast()
    elif section == "photography":
        _show_photography_guide()
    elif section == "etiquette":
        _show_sakura_etiquette()


# ── Shared helpers ────────────────────────────────────────────────────────────

def _back_button(key: str):
    if st.button("← Back to Home", key=key):
        st.session_state.sakura_section = "home"
        st.rerun()


def _nav_to(section: str):
    st.session_state.sakura_section = section
    st.rerun()


# ── Home ──────────────────────────────────────────────────────────────────────

def _show_home():
    st.markdown("""
    <style>
    .sakura-home {
        background: linear-gradient(135deg, #FFB7C5 0%, #FFD1DC 50%, #FFE4E1 100%);
        padding: 60px 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
    }
    .sakura-title  { font-size: 48px; color: #6C0820; font-weight: bold; margin-bottom: 10px; }
    .sakura-subtitle { font-size: 24px; color: #8B4513; margin-bottom: 30px; }
    </style>
    <div class="sakura-home">
        <div class="sakura-title">🌸 Cherry Blossom Guide</div>
        <div class="sakura-subtitle">Discover Japan's Sakura Season</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🌸 Explore Japan's Cherry Blossom Season")
    st.markdown("Click any section below to explore.")
    st.markdown("<br>", unsafe_allow_html=True)

    # Row 1
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📅  Bloom Calendar", key="home_calendar", use_container_width=True):
            _nav_to("calendar")
        st.caption("Interactive timeline of peak bloom dates across Japan")

    with c2:
        if st.button("📍  Best Viewing Spots", key="home_spots", use_container_width=True):
            _nav_to("spots")
        st.caption("Top locations with photos, tips, and nearby attractions")

    with c3:
        if st.button("🗺️  Sakura Map", key="home_map", use_container_width=True):
            _nav_to("map")
        st.caption("Interactive map — click a marker to see city details")

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2
    c4, c5, c6 = st.columns(3)
    with c4:
        if st.button("🔮  Bloom Forecast", key="home_forecast", use_container_width=True):
            _nav_to("forecast")
        st.caption("Pick a date and see predicted bloom % per city")

    with c5:
        if st.button("📷  Photography Guide", key="home_photo", use_container_width=True):
            _nav_to("photography")
        st.caption("Golden hour, camera settings, and drone rules")

    with c6:
        if st.button("🙏  Sakura Etiquette", key="home_etiquette", use_container_width=True):
            _nav_to("etiquette")
        st.caption("Cultural dos and don'ts for respectful hanami")


# ── Bloom Calendar ────────────────────────────────────────────────────────────

def _show_bloom_calendar():
    st.markdown("### 📅 Bloom Calendar")
    st.markdown("Select a month to see which cities are at peak bloom.")
    _back_button("calendar_back")
    st.markdown("---")

    months = ["January", "February", "March", "April", "May"]
    selected_month = st.selectbox("Select Month", months, index=3)  # default April

    month_map = {"January": "01", "February": "02", "March": "03",
                 "April": "04", "May": "05"}

    cities = get_cities_by_bloom_month(month_map[selected_month])

    if cities:
        st.markdown(f"#### 🌸 Cities with Peak Bloom in {selected_month}")
        for city in cities:
            with st.expander(f"🏙️ {city['name']} — {city['region']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Peak Bloom:** {city['peak_bloom_start']} → {city['peak_bloom_end']}")
                    st.markdown(f"**Crowd Level:** {city['crowd_level']}")
                with col2:
                    st.markdown(f"**Travel Tips:** {city['travel_tips']}")
                if city.get('nearby_attractions'):
                    st.markdown(f"**Nearby Attractions:** {city['nearby_attractions']}")
    else:
        st.info(f"No cities with peak bloom data for {selected_month}.")


# ── Best Viewing Spots ────────────────────────────────────────────────────────

def _show_viewing_spots():
    st.markdown("### 📍 Best Viewing Spots")
    _back_button("spots_back")
    st.markdown("---")

    cities = get_cherry_blossom_cities()

    if not cities:
        st.info("No cherry blossom data available yet.")
        return

    for city in cities:
        st.markdown(f"## 🏙️ {city['name']}")

        # City overview
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**🌸 Peak Bloom**")
            st.markdown(f"{city['peak_bloom_start']} → {city['peak_bloom_end']}")
        with col2:
            st.markdown("**👥 Crowd Level**")
            crowd = city['crowd_level']
            crowd_color = {"Very High": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(crowd, "⚪")
            st.markdown(f"{crowd_color} {crowd}")
        with col3:
            st.markdown("**✈️ Travel Tips**")
            st.markdown(city['travel_tips'])

        # Nearby attractions
        if city.get('nearby_attractions'):
            st.markdown("**🗺️ Nearby Attractions**")
            attractions = [a.strip() for a in city['nearby_attractions'].split(',')]
            cols = st.columns(min(len(attractions), 4))
            for i, attraction in enumerate(attractions):
                cols[i % 4].markdown(f"📌 {attraction}")

        # Best spots
        spots = get_sakura_spots(city['city_id'])
        if spots:
            st.markdown("**🌸 Best Sakura Spots**")
            spot_cols = st.columns(min(len(spots), 3))
            for i, spot in enumerate(spots):
                with spot_cols[i % 3]:
                    with st.container(border=True):
                        st.markdown(f"✓ **{spot['name']}**")
                        if spot['description']:
                            st.caption(spot['description'])
                        if spot['image_url']:
                            st.image(spot['image_url'], use_container_width=True)

        st.markdown("---")


# ── Sakura Map ────────────────────────────────────────────────────────────────

def _show_sakura_map():
    st.markdown("### 🗺️ Sakura Map")
    st.markdown("Click a marker to see city details.")
    _back_button("map_back")
    st.markdown("---")

    cities = get_cherry_blossom_cities()

    if not cities:
        st.info("No cherry blossom data available yet.")
        return

    if not _map_available:
        st.warning("Map library not installed. Run: `.venv\\Scripts\\pip install folium streamlit-folium`")
        for city in cities:
            st.markdown(f"- **{city['name']}** ({city['region']}) — {city['peak_bloom_start']} → {city['peak_bloom_end']}")
        return

    m = folium.Map(location=[36.2048, 138.2529], zoom_start=5, tiles="OpenStreetMap")

    crowd_colors = {"Very High": "red", "High": "orange", "Medium": "blue", "Low": "green"}

    for city in cities:
        if city['latitude'] and city['longitude']:
            attractions_html = ""
            if city.get('nearby_attractions'):
                items = [a.strip() for a in city['nearby_attractions'].split(',')]
                attractions_html = "<br>".join(f"📌 {a}" for a in items)
                attractions_html = f"<p style='margin:5px 0;'><strong>Nearby:</strong><br>{attractions_html}</p>"

            popup_html = f"""
            <div style="font-family: Arial, sans-serif; min-width: 220px;">
                <h4 style="margin:0 0 6px; color:#6C0820;">🌸 {city['name']}</h4>
                <p style="margin:4px 0;"><strong>Region:</strong> {city['region']}</p>
                <p style="margin:4px 0;"><strong>Peak Bloom:</strong> {city['peak_bloom_start']} – {city['peak_bloom_end']}</p>
                <p style="margin:4px 0;"><strong>Crowd:</strong> {city['crowd_level']}</p>
                <p style="margin:4px 0; color:#555;">{city['travel_tips']}</p>
                {attractions_html}
            </div>
            """

            color = crowd_colors.get(city['crowd_level'], "blue")
            folium.Marker(
                location=[city['latitude'], city['longitude']],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"🌸 {city['name']} — click for details",
                icon=folium.Icon(color=color, icon="leaf", prefix="fa"),
            ).add_to(m)

    # Legend
    st.markdown("**Map legend — crowd level:** 🔴 Very High &nbsp; 🟠 High &nbsp; 🔵 Medium &nbsp; 🟢 Low")
    folium_static(m, width=700, height=520)


# ── Bloom Forecast ────────────────────────────────────────────────────────────

def _show_bloom_forecast():
    st.markdown("### 🔮 Bloom Forecast")
    st.markdown("Pick a date to see predicted bloom percentage for each city.")
    _back_button("forecast_back")
    st.markdown("---")

    # Default to April 5 — peak season
    default_date = datetime.date(2024, 4, 5)
    forecast_date = st.date_input("Select a date", value=default_date,
                                  min_value=datetime.date(2024, 1, 1),
                                  max_value=datetime.date(2024, 12, 31))

    cities = get_cherry_blossom_cities()

    if not cities:
        st.info("No cherry blossom data available yet.")
        return

    st.markdown(f"#### 🌸 Bloom predictions for {forecast_date.strftime('%B %d, %Y')}")

    results = []
    for city in cities:
        forecast = get_sakura_forecast(city['city_id'], forecast_date.strftime("%Y-%m-%d"))
        bloom_pct = forecast['bloom_percentage'] if forecast else 0
        results.append((city['name'], bloom_pct))

    # Sort by bloom % descending
    results.sort(key=lambda x: x[1], reverse=True)

    for city_name, bloom_pct in results:
        if bloom_pct >= 90:
            status, bar_color = "🌸🌸🌸 Excellent", "#4CAF50"
        elif bloom_pct >= 70:
            status, bar_color = "🌸🌸 Good", "#8BC34A"
        elif bloom_pct >= 50:
            status, bar_color = "🌸 Fair", "#FFC107"
        elif bloom_pct >= 20:
            status, bar_color = "🌱 Early / Fading", "#FF9800"
        else:
            status, bar_color = "❄️ Not in Season", "#9E9E9E"

        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.markdown(f"**{city_name}**")
        with col2:
            st.markdown(
                f"<div style='background:{bar_color};border-radius:8px;padding:4px 10px;"
                f"color:white;font-weight:bold;display:inline-block'>{status}</div>",
                unsafe_allow_html=True,
            )
        with col3:
            st.metric("", f"{bloom_pct}%")
        st.progress(bloom_pct / 100)


# ── Photography Guide ─────────────────────────────────────────────────────────

def _show_photography_guide():
    st.markdown("### 📷 Photography Guide")
    _back_button("photo_back")
    st.markdown("---")

    with st.expander("🌅 Golden Hour", expanded=True):
        st.markdown("""
**Best Times for Sakura Photography:**
- **Early Morning (6:00–8:00 AM):** Soft golden light with far fewer crowds
- **Late Afternoon (4:00–6:00 PM):** Warm backlighting through petals
- **Blue Hour (30 min after sunset):** Magical blue-pink sky contrast

**Tips:**
- Arrive early to claim the best angles before crowds arrive
- Use a tripod for long exposures in low light
- Shoot during golden hour for warm, dreamy tones
        """)

    with st.expander("📍 Best Photography Locations"):
        st.markdown("""
**Composition Ideas:**
- **Framing:** Use torii gates or temple structures as natural frames
- **Reflections:** Capture sakura in ponds and rivers
- **Tunnel Effect:** Shoot through blossom tunnels for depth
- **Silhouettes:** Backlight subjects against bright blooms
- **Detail Shots:** Focus on individual petals or falling blossoms

**Popular Photo Spots:**
- Philosopher's Path, Kyoto
- Chidorigafuchi Canal, Tokyo
- Hirosaki Castle, Aomori
- Meguro River, Tokyo
        """)

    with st.expander("🎥 Camera Settings"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
**Recommended Settings:**
- **Aperture:** f/2.8–f/4 for soft bokeh background
- **ISO:** 100–400 for clean images
- **Shutter Speed:** 1/250s+ handheld; slower on tripod
- **White Balance:** Auto or Daylight
            """)
        with col2:
            st.markdown("""
**Recommended Equipment:**
- 50mm or 85mm prime lens for portraits
- 24–70mm zoom for versatility
- Sturdy tripod
- Circular polarising filter to cut glare
            """)

    with st.expander("🚁 Drone Photography Rules"):
        st.markdown("""
**Important Regulations in Japan:**
- **Registration Required** — all drones must be registered with the MLIT
- **No-Fly Zones** — strictly prohibited near airports, government buildings, and populated areas
- **Altitude Limit** — maximum 150 m above ground level
- **Visual Line of Sight** — must maintain direct visual contact with your drone at all times
- **Privacy** — cannot photograph identifiable individuals without consent

**Best Drone-Friendly Locations:**
- Mount Yoshino (with advance permit)
- Rural mountain areas with low population density
- Coastal cherry blossom areas away from urban centres
- Always check current prefectural regulations before flying
        """)


# ── Sakura Etiquette ──────────────────────────────────────────────────────────

def _show_sakura_etiquette():
    st.markdown("### 🙏 Sakura Etiquette")
    st.markdown("Things every visitor should know before attending hanami.")
    _back_button("etiquette_back")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ✅ Do")
        dos = [
            ("🧘", "Enjoy the moment", "Take time to appreciate the beauty — put the phone down occasionally"),
            ("📸", "Take photos respectfully", "Be mindful of other visitors in your shots"),
            ("🗑️", "Clean your picnic area", "Japan has a strong leave-no-trace culture"),
            ("📋", "Follow local rules", "Each park may have specific guidelines — read signage"),
            ("⏳", "Be patient", "Popular spots get crowded; go with the flow"),
            ("🛤️", "Use designated areas", "Stay on paths and in permitted picnic zones"),
        ]
        for icon, title, desc in dos:
            st.markdown(f"**{icon} {title}**")
            st.caption(desc)

    with col2:
        st.markdown("#### ❌ Don't")
        donts = [
            ("🌿", "Shake branches", "This damages and knocks off blossoms prematurely"),
            ("🌸", "Pick flowers", "Leave them for everyone to enjoy"),
            ("🌳", "Climb trees", "Disrespectful and dangerous"),
            ("🗑️", "Leave trash", "Pack out everything you bring in"),
            ("🚧", "Block paths", "Keep walkways clear for other visitors"),
            ("📢", "Be excessively loud", "Maintain a peaceful atmosphere for everyone"),
        ]
        for icon, title, desc in donts:
            st.markdown(f"**{icon} Don't {title.lower()}**")
            st.caption(desc)

    st.markdown("---")

    with st.expander("📜 Cultural Significance of Hanami (花見)"):
        st.markdown("""
Hanami — literally "flower viewing" — is a centuries-old Japanese tradition dating back to the Nara period (710–794 AD), 
originally practiced by the imperial court. It spread to the samurai class during the Heian period and eventually became 
a nationwide celebration.

**What cherry blossoms symbolise:**
- The fleeting, transient nature of life (*mono no aware* — 物の哀れ)
- Renewal and the arrival of spring
- The beauty found in impermanence

**Modern hanami:**
- Friends and families spread tarps under cherry trees
- Share food, drinks, and conversation
- Often includes hanami bento (special picnic boxes from convenience stores)
- A time for reflection, gratitude, and celebration of nature's cycle
        """)

    with st.expander("🍱 Hanami Picnic Tips"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
**Planning:**
- Arrive early at popular spots — people claim space from dawn
- Bring a waterproof tarp or picnic mat
- Many convenience stores (7-Eleven, Lawson, FamilyMart) sell hanami sets
- Dress in warm layers — spring evenings are cold
            """)
        with col2:
            st.markdown("""
**Checklist:**
- ✅ Picnic mat or tarp
- ✅ Food and drinks
- ✅ Warm jacket
- ✅ Camera
- ✅ Trash bags (essential — many parks have no bins)
- ✅ Wet wipes
- ✅ Cash (many vendors are cash-only)
            """)
