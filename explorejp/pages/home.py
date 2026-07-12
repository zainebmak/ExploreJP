"""Home page for ExploreJP Streamlit app."""

from pathlib import Path

import streamlit as st
from explorejp.database import get_total_cities, get_all_regions, get_all_seasons


def show():
    """Display the home page."""

    total_cities  = get_total_cities()
    total_regions = len(get_all_regions())
    total_seasons = len(get_all_seasons())

    logo_path = Path(__file__).resolve().parents[2] / "data" / "logo.png"

    # ── Navbar row ────────────────────────────────────────────────────────────
    user = st.session_state.get("user")

    if user:
        col_brand, col_spacer, col_ai, col_sakura, col_plan, col_dash, col_logout = st.columns([3, 1, 2, 2, 2, 2, 2])
    else:
        col_brand, col_spacer, col_ai, col_sakura, col_plan, col_login = st.columns([3, 2, 2, 2, 2, 2])

    with col_brand:
        if logo_path.exists():
            st.image(str(logo_path), width=44)
        st.markdown("### ExploreJP")

    with col_ai:
        st.write("")
        if st.button("🤖 Chat with Sakura", key="nav_sakura_ai_home", use_container_width=True):
            st.session_state.page = "🤖 Sakura AI"
            st.rerun()

    with col_sakura:
        st.write("")
        if st.button("🌸 Cherry Blossom", key="nav_cherry_blossom", use_container_width=True):
            st.session_state.page = "🌸 Cherry Blossom Guide"
            st.session_state.sakura_section = "home"
            st.rerun()

    with col_plan:
        st.write("")
        if st.button("🧳 Plan Trip", key="nav_plan_trip", use_container_width=True):
            st.session_state.page = "🧳 Plan Your Trip"
            st.rerun()

    if user:
        with col_dash:
            st.write("")
            if st.button("📊 Dashboard", key="nav_home_dashboard", use_container_width=True):
                st.session_state.page = "📊 Dashboard"
                st.rerun()
        with col_logout:
            st.write("")
            if st.button("🚪 Log Out", key="nav_home_logout", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
    else:
        with col_login:
            st.write("")
            if st.button("🔑 Log In", key="nav_home_login", use_container_width=True):
                st.session_state.page = "🔑 Login"
                st.rerun()

    st.divider()

    # ── Welcome banner for logged-in users ───────────────────────────────────
    if user:
        badges = []
        if user.get("favorite_season"):
            badges.append(f"🌸 **{user['favorite_season']}** season")
        if user.get("preferred_budget"):
            badges.append(f"💰 **{user['preferred_budget']}** budget")
        badge_str = "  •  ".join(badges) if badges else "Set your preferences in Settings ⚙️"

        with st.container(border=True):
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"### 👋 Welcome back, {user['username']}!")
                st.caption(badge_str)
            with c2:
                st.write("")
                if st.button("📊 My Dashboard", key="home_dash_banner", use_container_width=True):
                    st.session_state.page = "📊 Dashboard"
                    st.rerun()
        st.divider()

    # ── Hero row ──────────────────────────────────────────────────────────────
    col_text, col_image = st.columns([1, 1], gap="large")

    with col_text:
        st.caption("WELCOME TO")
        st.title("Discover Japan")
        st.write(
            "Explore beautiful destinations, rich culture, "
            "and unforgettable experiences. Your journey begins here."
        )
        st.write("")
        if st.button("Explore Now →", key="btn_explore_now"):
            st.session_state.page = "🗺️ Explore Cities"
            st.session_state.explore_cities_action = "Browse All Cities"
            st.rerun()

    with col_image:
        st.image(
            "https://images.unsplash.com/photo-1528164344705-47542687000d"
            "?auto=format&fit=crop&w=900&q=80",
            caption="Mount Fuji & Chureito Pagoda",
            use_container_width=True,
        )

    st.divider()

    # ── Stats row ─────────────────────────────────────────────────────────────
    s1, s2, s3 = st.columns(3)
    s1.metric("🏙️ Cities",   total_cities)
    s2.metric("🗾 Regions",  total_regions)
    s3.metric("🌸 Seasons",  total_seasons)

    st.divider()

    # ── Popular Destinations ──────────────────────────────────────────────────
    dest_header, dest_btn = st.columns([4, 1])
    with dest_header:
        st.subheader("Popular Destinations")
    with dest_btn:
        st.write("")
        if st.button("View All →", key="view_all_destinations", use_container_width=True):
            st.session_state.page = "🗺️ Explore Cities"
            st.session_state.explore_cities_action = "Browse All Cities"
            st.rerun()

    destinations = [
        ("Tokyo",  "Modern meets tradition",
         "https://i.pinimg.com/1200x/9b/15/5b/9b155ba076855fb968ab6b457be10816.jpg"),
        ("Kyoto",  "Timeless beauty",
         "https://i.pinimg.com/1200x/29/d5/c2/29d5c2a255007594642cba1ecec88656.jpg"),
        ("Osaka",  "Vibrant and energetic",
         "https://i.pinimg.com/1200x/2d/d5/ac/2dd5ac8bec1ea2744fb66f4956d95b0a.jpg"),
    ]

    d1, d2, d3 = st.columns(3, gap="medium")
    for col, (city, desc, img) in zip([d1, d2, d3], destinations):
        with col:
            st.image(img, use_container_width=True)
            st.markdown(f"**{city}**")
            st.caption(desc)

    st.divider()

    # ── Travel Guide ──────────────────────────────────────────────────────────
    st.subheader("Travel Guide")

    guides = [
        ("📍", "Where to Go",        "Top destinations in Japan"),
        ("🌸", "Things to Do",       "Unique experiences awaiting you"),
        ("🧳", "Plan Your Trip",     "Tips, tools and itineraries"),
        ("ℹ️",  "Travel Essentials",  "Everything you need before you go"),
    ]

    g1, g2 = st.columns(2, gap="medium")
    for i, (icon, title, desc) in enumerate(guides):
        col = g1 if i % 2 == 0 else g2
        with col:
            with st.container(border=True):
                st.markdown(f"#### {icon} {title}")
                st.caption(desc)