"""Home page for ExploreJP Streamlit app."""

import base64
from pathlib import Path

import streamlit as st
from explorejp.database import get_total_cities, get_all_regions, get_all_seasons


def get_logo_base64() -> str:
    logo_path = Path(__file__).resolve().parents[2] / "data" / "logo.png"
    if logo_path.exists():
        encoded = base64.b64encode(logo_path.read_bytes()).decode("utf-8")
        return (
            f'<img src="data:image/png;base64,{encoded}" alt="ExploreJP" '
            f'style="width:42px;height:42px;object-fit:contain;border-radius:12px;flex-shrink:0;">'
        )
    return (
        '<div style="width:42px;height:42px;border-radius:12px;flex-shrink:0;'
        'background:linear-gradient(135deg,#6C0820,#F2AEBC);'
        'display:flex;align-items:center;justify-content:center;">'
        '<svg viewBox="0 0 64 64" width="26" height="26" xmlns="http://www.w3.org/2000/svg">'
        '<path d="M24 20c0-5 4-9 9-9s9 4 9 9c0 3-2 5-4 7l-3 2-3-2c-2-2-4-4-4-7Z" fill="#FFF3F6"/>'
        '<path d="M20 40c4 3 8 4 12 4s8-1 12-4v6H20v-6Z" fill="#F2AEBC"/>'
        '</svg></div>'
    )


def show():
    """Display the home page."""

    get_total_cities()
    get_all_regions()
    get_all_seasons()
    logo_html = get_logo_base64()

    # ── Styles ────────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@400;500;600;700&display=swap');

    .stMainBlockContainer { padding-top: 1.2rem !important; }

    /* ── shell ── */
    .hm-shell {
        font-family: 'Montserrat', sans-serif;
        background: #fff8fb;
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 8px 40px rgba(108,8,32,0.08);
        margin-bottom: 0;
    }

    /* ── navbar ── */
    .hm-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 16px 40px;
        background: #fff;
        border-bottom: 1px solid rgba(242,174,188,0.3);
    }
    .hm-nav-brand {
        display: flex;
        align-items: center;
        gap: 11px;
        text-decoration: none;
    }
    .hm-nav-brand-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #6C0820;
        letter-spacing: 0.02em;
    }
    .hm-nav-links {
        display: flex;
        align-items: center;
        gap: 32px;
    }
    .hm-nav-links a {
        font-size: 0.76rem;
        letter-spacing: 0.12em;
        color: #305D91;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.2s;
    }
    .hm-nav-links a.active {
        color: #6C0820;
        border-bottom: 2px solid #F2AEBC;
        padding-bottom: 2px;
    }
    .hm-nav-links a:hover { color: #6C0820; }

    /* ── hero ── */
    .hm-hero {
        display: grid;
        grid-template-columns: 1fr 1.35fr;
        min-height: 500px;
    }
    .hm-hero-left {
        padding: 60px 44px 60px 48px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        background: #fff8fb;
    }
    .hm-eyebrow {
        font-size: 0.7rem;
        letter-spacing: 0.26em;
        color: #6C0820;
        font-weight: 700;
        text-transform: uppercase;
        margin: 0 0 14px 0;
    }
    .hm-title {
        font-family: 'Playfair Display', serif;
        font-size: 4.6rem;
        line-height: 0.93;
        color: #6C0820;
        margin: 0 0 22px 0;
        letter-spacing: -0.02em;
    }
    .hm-desc {
        font-size: 0.97rem;
        line-height: 1.85;
        color: #666;
        margin: 0 0 0 0;
        max-width: 380px;
    }
    .hm-hero-right {
        overflow: hidden;
        position: relative;
    }
    .hm-hero-right img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
        min-height: 500px;
        transition: transform 0.6s ease;
    }
    .hm-hero-right:hover img { transform: scale(1.03); }

    /* ── PLAN YOUR TRIP button (outlined pill, inside navbar) ── */
    button[key="btn_plan_trip"] {
        background: white !important;
        color: #6C0820 !important;
        border: 2px solid #6C0820 !important;
        border-radius: 32px !important;
        padding: 9px 22px !important;
        font-size: 0.74rem !important;
        letter-spacing: 0.11em !important;
        font-weight: 700 !important;
        box-shadow: none !important;
        transition: all 0.25s !important;
    }

    /* Target by key — Streamlit renders key as the element id on the button wrapper */
    div[data-testid="stButton"]:has(> button[key="btn_plan_trip"]) button,
    div[data-testid="stButton"]:has(> button[key="btn_plan_trip"]) button:focus {
        background: white !important;
        color: #6C0820 !important;
        border: 2px solid #6C0820 !important;
        border-radius: 32px !important;
        font-size: 0.74rem !important;
        letter-spacing: 0.11em !important;
        font-weight: 700 !important;
        box-shadow: none !important;
        padding: 9px 22px !important;
        min-height: unset !important;
        height: auto !important;
        line-height: 1.4 !important;
    }
    div[data-testid="stButton"]:has(> button[key="btn_plan_trip"]) button:hover {
        background: #6C0820 !important;
        color: white !important;
    }

    /* ── EXPLORE NOW button (gradient pill, inside hero left) ── */
    div[data-testid="stButton"]:has(> button[key="btn_explore_now"]) button,
    div[data-testid="stButton"]:has(> button[key="btn_explore_now"]) button:focus {
        background: linear-gradient(135deg, #6C0820 0%, #305D91 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 32px !important;
        padding: 14px 34px !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.13em !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 24px rgba(108,8,32,0.22) !important;
        min-height: unset !important;
        height: auto !important;
        line-height: 1.4 !important;
        transition: transform 0.25s, box-shadow 0.25s !important;
    }
    div[data-testid="stButton"]:has(> button[key="btn_explore_now"]) button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 14px 36px rgba(108,8,32,0.32) !important;
    }

    /* ── Pull the nav button row up into the navbar ── */
    div[data-testid="stHorizontalBlock"]:has(button[key="btn_plan_trip"]) {
        margin-top: -56px !important;
        margin-bottom: 4px !important;
        position: relative;
        z-index: 100;
        padding-right: 40px !important;
    }
    /* make the two surrounding spacer columns disappear */
    div[data-testid="stHorizontalBlock"]:has(button[key="btn_plan_trip"])
        > div[data-testid="column"]:not(:last-child) {
        visibility: hidden !important;
    }

    /* ── Pull the explore button row up into the hero left ── */
    div[data-testid="stHorizontalBlock"]:has(button[key="btn_explore_now"]) {
        margin-top: -60px !important;
        margin-bottom: 0 !important;
        position: relative;
        z-index: 100;
        padding-left: 48px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(button[key="btn_explore_now"])
        > div[data-testid="column"]:not(:first-child) {
        visibility: hidden !important;
    }

    /* ── below-hero sections ── */
    .section-title-main {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        color: #6C0820;
        font-weight: 700;
        margin: 0 0 22px 0;
    }
    .dest-card-main {
        background: #fff;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 6px 28px rgba(108,8,32,0.09);
        transition: transform 0.3s, box-shadow 0.3s;
        cursor: pointer;
    }
    .dest-card-main:hover {
        transform: translateY(-10px);
        box-shadow: 0 18px 44px rgba(108,8,32,0.16);
    }
    .dest-image-main { width:100%; height:210px; object-fit:cover; display:block; }
    .dest-info-main { padding: 16px 18px 18px; }
    .dest-name-main {
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        font-weight: 700;
        color: #6C0820;
        margin: 0 0 5px 0;
    }
    .dest-desc-main { font-size: 0.85rem; color: #777; margin: 0; }
    .guide-item-main {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 16px 18px;
        background: #fff;
        border-radius: 14px;
        margin-bottom: 10px;
        box-shadow: 0 3px 16px rgba(108,8,32,0.07);
        transition: background 0.22s, transform 0.22s, box-shadow 0.22s;
        cursor: pointer;
    }
    .guide-item-main:hover {
        background: #F2DCDB;
        transform: translateX(7px);
        box-shadow: 0 7px 22px rgba(108,8,32,0.11);
    }
    .guide-icon-main { font-size: 1.5rem; flex-shrink: 0; }
    .guide-content-main { flex: 1; }
    .guide-title-main { font-size: 0.95rem; font-weight: 700; color: #6C0820; margin: 0 0 2px 0; }
    .guide-desc-main { font-size: 0.8rem; color: #777; margin: 0; line-height: 1.4; }
    .guide-arrow-main { font-size: 1.5rem; color: #F2AEBC; line-height: 1; }
    </style>
    """, unsafe_allow_html=True)

    # ── Navbar + Hero HTML (no buttons inside — they come as st.button below) ─
    st.markdown(f"""
    <div class="hm-shell">
      <div class="hm-nav">
        <a class="hm-nav-brand" href="#">
          {logo_html}
          <span class="hm-nav-brand-name">ExploreJP</span>
        </a>
        <nav class="hm-nav-links">
          <a href="#" class="active">HOME •</a>
          <a href="#">DESTINATIONS</a>
          <a href="#">EXPERIENCES</a>
          <a href="#">GUIDES</a>
          <a href="#">ABOUT</a>
        </nav>
        <!-- PLAN YOUR TRIP button is rendered by Streamlit below, overlaid here -->
      </div>
      <div class="hm-hero">
        <div class="hm-hero-left">
          <p class="hm-eyebrow">Welcome to</p>
          <h1 class="hm-title">Discover<br>Japan</h1>
          <p class="hm-desc">
            Explore beautiful destinations, rich culture,
            and unforgettable experiences across Japan.
            Your journey begins here.
          </p>
          <!-- EXPLORE NOW button is rendered by Streamlit below, overlaid here -->
        </div>
        <div class="hm-hero-right">
          <img
            src="https://images.unsplash.com/photo-1528164344705-47542687000d?auto=format&fit=crop&w=1400&q=80"
            alt="Mount Fuji with Torii gate and cherry blossoms">
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── PLAN YOUR TRIP — real st.button overlaid into navbar via CSS ──────────
    _s, _m, plan_col = st.columns([5, 3, 1])
    with plan_col:
        if st.button("PLAN YOUR TRIP", key="btn_plan_trip", use_container_width=True):
            st.session_state.page = "🧳 Plan Your Trip"
            st.rerun()

    # ── EXPLORE NOW — real st.button overlaid into hero-left via CSS ──────────
    explore_col, _r = st.columns([1, 2])
    with explore_col:
        if st.button("EXPLORE NOW →", key="btn_explore_now", use_container_width=False):
            st.session_state.page = "🗺️ Explore Cities"
            st.session_state.explore_cities_action = "Browse All Cities"
            st.rerun()

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    # ── Popular Destinations + Travel Guide ───────────────────────────────────
    col_dest, col_guide = st.columns([1.8, 1], gap="large")

    with col_dest:
        hdr_col, btn_col = st.columns([3, 1])
        with hdr_col:
            st.markdown('<h2 class="section-title-main">Popular Destinations</h2>', unsafe_allow_html=True)
        with btn_col:
            if st.button("VIEW ALL →", key="view_all_destinations"):
                st.session_state.page = "🗺️ Explore Cities"
                st.session_state.explore_cities_action = "Browse All Cities"
                st.rerun()

        dcols = st.columns(3, gap="medium")
        destinations = [
            ("Tokyo", "Modern meets tradition",
             "https://i.pinimg.com/1200x/9b/15/5b/9b155ba076855fb968ab6b457be10816.jpg"),
            ("Kyoto", "Timeless beauty",
             "https://i.pinimg.com/1200x/29/d5/c2/29d5c2a255007594642cba1ecec88656.jpg"),
            ("Osaka", "Vibrant and energetic",
             "https://i.pinimg.com/1200x/2d/d5/ac/2dd5ac8bec1ea2744fb66f4956d95b0a.jpg"),
        ]
        for i, (city, desc, img) in enumerate(destinations):
            with dcols[i]:
                st.markdown(
                    f'<div class="dest-card-main">'
                    f'<img src="{img}" alt="{city}" class="dest-image-main">'
                    f'<div class="dest-info-main">'
                    f'<h3 class="dest-name-main">{city}</h3>'
                    f'<p class="dest-desc-main">{desc}</p>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )

    with col_guide:
        st.markdown('<h2 class="section-title-main">Travel Guide</h2>', unsafe_allow_html=True)
        guides = [
            ("📍", "Where to Go",       "Top destinations in Japan"),
            ("🌸", "Things to Do",      "Unique experiences"),
            ("🧳", "Plan Your Trip",    "Tips and itineraries"),
            ("ℹ️",  "Travel Essentials", "Everything you need to know"),
        ]
        for icon, title, desc in guides:
            st.markdown(
                f'<div class="guide-item-main">'
                f'<span class="guide-icon-main">{icon}</span>'
                f'<div class="guide-content-main">'
                f'<h4 class="guide-title-main">{title}</h4>'
                f'<p class="guide-desc-main">{desc}</p>'
                f'</div>'
                f'<span class="guide-arrow-main">›</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
