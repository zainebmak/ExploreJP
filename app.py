"""Streamlit app for ExploreJP - Discover Japan."""

import streamlit as st
from explorejp.config import PAGE_CONFIG, CUSTOM_CSS
from explorejp.pages import home, explore_cities

# Page configuration
st.set_page_config(**PAGE_CONFIG)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize database
from explorejp.database import init_database, import_csv_to_db

@st.cache_resource
def initialize_database():
    """Initialize the database (cached to run only once)."""
    init_database()
    import_csv_to_db()

initialize_database()

# Navigation
def main():
    """Main application with navigation."""

    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "🏠 Home"

    # Handle query parameters for navigation
    query_params = st.query_params
    requested_page = query_params.get("page")
    if requested_page == "explore":
        st.session_state.page = "🗺️ Explore Cities"
        # Clear query params to prevent repeated navigation
        st.query_params.clear()

    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🌸 ExploreJP")
        st.markdown("---")
        
        # Calculate current index based on session state
        current_index = 0 if st.session_state.page == "🏠 Home" else 1
        
        # Use a unique key that won't conflict with other navigation
        page = st.radio(
            "Navigate",
            ["🏠 Home", "🗺️ Explore Cities"],
            label_visibility="collapsed",
            index=current_index,
            key="sidebar_nav_radio"
        )
        
        # Only update if there's an actual change and it's from user interaction
        if page != st.session_state.page:
            st.session_state.page = page
            # Clear any action state when switching pages
            if "explore_cities_action" in st.session_state:
                st.session_state.explore_cities_action = "Browse All Cities"
            if "selected_city_id" in st.session_state:
                del st.session_state.selected_city_id
            st.rerun()
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        Discover the beauty of Japan through our curated city guide.
        
        - Explore popular destinations
        - Compare cities
        - View interactive statistics
        """)
    
    # Page routing - use session state directly to avoid conflicts
    current_page = st.session_state.page
    if current_page == "🏠 Home":
        home.show()
    elif current_page == "🗺️ Explore Cities":
        explore_cities.show()

if __name__ == "__main__":
    main()
