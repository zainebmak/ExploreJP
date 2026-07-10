"""Home page for ExploreJP Streamlit app."""

import base64
from pathlib import Path

import streamlit as st
from explorejp.config import COLORS
from explorejp.database import get_total_cities, get_all_regions, get_all_seasons


def get_logo_html() -> str:
    logo_path = Path(__file__).resolve().parents[2] / "data" / "logo.png"
    if logo_path.exists():
        encoded = base64.b64encode(logo_path.read_bytes()).decode("utf-8")
        return f'<img class="brand-logo" src="data:image/png;base64,{encoded}" alt="ExploreJP logo">'

    return '<div class="brand-logo-badge" aria-label="ExploreJP logo"><svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><rect x="8" y="8" width="48" height="48" rx="16" fill="#6C0820" /><path d="M24 20c0-5 4-9 9-9s9 4 9 9c0 3-2 5-4 7l-3 2-3-2c-2-2-4-4-4-7Z" fill="#FFF3F6" /><path d="M20 40c4 3 8 4 12 4s8-1 12-4v6H20v-6Z" fill="#F2AEBC" /></svg></div>'


def show():
    """Display the home page."""

    total_cities = get_total_cities()
    total_regions = len(get_all_regions())
    total_seasons = len(get_all_seasons())
    brand_logo_html = get_logo_html()

    # Top Navigation Bar
    st.markdown(f'<div class="top-nav-bar"><div class="nav-brand-main">{brand_logo_html}<span class="brand-name-text">ExploreJP</span></div><div class="nav-menu-main"><a href="#" class="nav-item-main active">HOME •</a><a href="#" class="nav-item-main">DESTINATIONS</a><a href="#" class="nav-item-main">EXPERIENCES</a><a href="#" class="nav-item-main">GUIDES</a><a href="#" class="nav-item-main">ABOUT</a></div><button class="nav-cta-main">PLAN YOUR TRIP</button></div>', unsafe_allow_html=True)
    
    # Hero Section with side-by-side layout
    st.markdown('<div class="hero-container-main">', unsafe_allow_html=True)
    
    col_hero_left, col_hero_right = st.columns([1, 1.3], gap="large")
    
    with col_hero_left:
        st.markdown('<div class="hero-left-content"><p class="hero-eyebrow-text">WELCOME TO</p><h1 class="hero-title-main">Discover<br/>Japan</h1><p class="hero-desc-text">Explore beautiful destinations, rich culture,<br/>and unforgettable experiences.<br/>Your journey begins here.</p></div>', unsafe_allow_html=True)
        
        # Explore Now button that navigates to explore cities
        if st.button("EXPLORE NOW →", use_container_width=False, key="explore_now_btn"):
            st.session_state.page = "🗺️ Explore Cities"
            # Reset explore cities action to browse all cities
            st.session_state.explore_cities_action = "Browse All Cities"
            # Force a rerun to navigate
            st.rerun()
    
    with col_hero_right:
        st.markdown('<div class="hero-right-visual"><img src="https://images.unsplash.com/photo-1528164344705-47542687000d?auto=format&fit=crop&w=1400&q=80" alt="Mount Fuji with Torii gate and cherry blossoms" class="hero-image-main"></div>', unsafe_allow_html=True)
    
    st.markdown('</div><br/><br/>', unsafe_allow_html=True)
    
    # Popular Destinations and Travel Guide side by side
    col_destinations, col_guide = st.columns([1.8, 1], gap="large")
    
    with col_destinations:
        # Section header with clickable VIEW ALL button
        dest_col1, dest_col2 = st.columns([3, 1])
        with dest_col1:
            st.markdown('<h2 class="section-title-main">Popular Destinations</h2>', unsafe_allow_html=True)
        with dest_col2:
            if st.button("VIEW ALL", key="view_all_destinations"):
                st.session_state.page = "🗺️ Explore Cities"
                # Reset explore cities action to browse all cities
                st.session_state.explore_cities_action = "Browse All Cities"
                # Force a rerun to navigate
                st.rerun()
        
        # Destinations in horizontal layout
        dest_cols = st.columns(3, gap="medium")
        
        destinations = [
            ('Tokyo', 'Modern meets tradition', 'https://i.pinimg.com/1200x/9b/15/5b/9b155ba076855fb968ab6b457be10816.jpg'),
            ('Kyoto', 'Timeless beauty', 'https://i.pinimg.com/1200x/29/d5/c2/29d5c2a255007594642cba1ecec88656.jpg'),
            ('Osaka', 'Vibrant and energetic', 'https://i.pinimg.com/1200x/2d/d5/ac/2dd5ac8bec1ea2744fb66f4956d95b0a.jpg')
        ]
        
        for idx, (city, desc, img) in enumerate(destinations):
            with dest_cols[idx]:
                st.markdown(f'<div class="dest-card-main"><img src="{img}" alt="{city}" class="dest-image-main"><div class="dest-info-main"><h3 class="dest-name-main">{city}</h3><p class="dest-desc-main">{desc}</p></div></div>', unsafe_allow_html=True)
    
    with col_guide:
        st.markdown('<h2 class="section-title-main" style="margin-bottom: 24px;">Travel Guide</h2>', unsafe_allow_html=True)
        
        guides = [
            ('📍', 'Where to Go', 'Top destinations in Japan'),
            ('🌸', 'Things to Do', 'Unique experiences'),
            ('🧳', 'Plan Your Trip', 'Tips and itineraries'),
            ('ℹ️', 'Travel Essentials', 'Everything you need to know')
        ]
        
        for icon, title, desc in guides:
            st.markdown(f'<div class="guide-item-main"><span class="guide-icon-main">{icon}</span><div class="guide-content-main"><h4 class="guide-title-main">{title}</h4><p class="guide-desc-main">{desc}</p></div><span class="guide-arrow-main">›</span></div>', unsafe_allow_html=True)


