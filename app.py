"""Streamlit app for ExploreJP - Discover Japan."""

import streamlit as st
from explorejp.config import PAGE_CONFIG, CUSTOM_CSS
from explorejp.pages import home, explore_cities, plan_trip

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
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🌸 ExploreJP")
        st.markdown("---")
        
        # Simple navigation without conflicts
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            st.session_state.page = "🏠 Home"
            if "explore_cities_action" in st.session_state:
                del st.session_state.explore_cities_action
            if "selected_city_id" in st.session_state:
                del st.session_state.selected_city_id
        
        if st.button("🗺️ Explore Cities", key="nav_explore", use_container_width=True):
            st.session_state.page = "🗺️ Explore Cities"
            st.session_state.explore_cities_action = "Browse All Cities"
        
        st.markdown("---")
        st.markdown(f"**Current Page:** {st.session_state.page}")
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        Discover the beauty of Japan through our curated city guide.
        
        - Explore popular destinations
        - Compare cities
        - View interactive statistics
        - Plan your perfect trip
        """)
    
    # Page routing
    if st.session_state.page == "🏠 Home":
        home.show()
    elif st.session_state.page == "🗺️ Explore Cities":
        explore_cities.show()
    elif st.session_state.page == "🧳 Plan Your Trip":
        plan_trip.show()

if __name__ == "__main__":
    main()
