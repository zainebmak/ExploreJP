"""Streamlit app for ExploreJP - Discover Japan."""

# Load .env FIRST — before any other imports so GROQ_API_KEY is in os.environ
# when the AI engine module is imported.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import os
import streamlit as st
from explorejp.config import PAGE_CONFIG, CUSTOM_CSS
from explorejp.pages import home, explore_cities, plan_trip, cherry_blossom, auth, dashboard, settings, sakura_ai

# Page configuration
st.set_page_config(**PAGE_CONFIG)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize database
from explorejp.database import init_database, import_csv_to_db

@st.cache_resource
def initialize_database():
    """Initialize the database (cached to run once)."""
    init_database()
    import_csv_to_db()

initialize_database()

def main():
    """Main application with navigation."""
    
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "🏠 Home"
    
    user = st.session_state.get("user")

    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🌸 ExploreJP")
        st.markdown("---")
        
        # Core navigation
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            st.session_state.page = "🏠 Home"
            if "explore_cities_action" in st.session_state:
                del st.session_state.explore_cities_action
            if "selected_city_id" in st.session_state:
                del st.session_state.selected_city_id
            st.rerun()
        
        if st.button("🗺️ Explore Cities", key="nav_explore", use_container_width=True):
            st.session_state.page = "🗺️ Explore Cities"
            st.session_state.explore_cities_action = "Browse All Cities"
            st.rerun()

        if st.button("🧳 Plan Your Trip", key="nav_plan", use_container_width=True):
            st.session_state.page = "🧳 Plan Your Trip"
            st.rerun()

        if st.button("🌸 Cherry Blossom Guide", key="nav_sakura", use_container_width=True):
            st.session_state.page = "🌸 Cherry Blossom Guide"
            st.session_state.sakura_section = "home"
            st.rerun()

        if st.button("🤖 Sakura AI", key="nav_sakura_ai", use_container_width=True):
            st.session_state.page = "🤖 Sakura AI"
            st.rerun()
        
        st.markdown("---")

        # Auth section
        if user:
            st.markdown(f"👤 **{user['username']}**")
            if st.button("📊 My Dashboard", key="nav_dashboard", use_container_width=True):
                st.session_state.page = "📊 Dashboard"
                st.rerun()
            if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
                st.session_state.page = "⚙️ Settings"
                st.rerun()
            if st.button("🚪 Log Out", key="nav_logout", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        else:
            if st.button("🔑 Log In / Register", key="nav_login", use_container_width=True):
                st.session_state.page = "🔑 Login"
                st.rerun()

        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        Discover the beauty of Japan through our curated city guide.
        
        - Explore popular destinations
        - Compare cities
        - View interactive statistics
        - Plan your perfect trip
        """)

        # Sakura AI — API key widget (only shown on AI page or when key not set)
        if st.session_state.get("page") == "🤖 Sakura AI":
            sakura_ai.render_api_key_sidebar()
    
    # Page routing
    if st.session_state.page == "🏠 Home":
        home.show()
    elif st.session_state.page == "🗺️ Explore Cities":
        explore_cities.show()
    elif st.session_state.page == "🧳 Plan Your Trip":
        plan_trip.show()
    elif st.session_state.page == "🌸 Cherry Blossom Guide":
        cherry_blossom.show()
    elif st.session_state.page == "🔑 Login":
        auth.show()
    elif st.session_state.page == "📊 Dashboard":
        dashboard.show()
    elif st.session_state.page == "⚙️ Settings":
        settings.show()
    elif st.session_state.page == "🤖 Sakura AI":
        sakura_ai.show()

if __name__ == "__main__":
    main()
