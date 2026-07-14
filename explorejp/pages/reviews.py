"""Community reviews and ratings page for ExploreJP Streamlit app."""

import streamlit as st
from explorejp.config import COLORS
from explorejp.database import (
    get_all_cities,
    get_city_by_id,
    get_reviews_by_city,
    get_reviews_by_user,
    get_user_review_for_city,
    add_review,
    update_review,
    delete_review,
    get_city_average_rating,
    get_city_rating_count,
    get_all_reviews,
)


def _current_user_id() -> int | None:
    """Return logged-in user's id, or None if guest."""
    user = st.session_state.get("user")
    return user["id"] if user else None


def _render_page_header() -> None:
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("🏠 Back to Home", key="back_home_reviews", use_container_width=True):
            st.session_state.page = "🏠 Home"
            st.rerun()
    st.markdown('<div class="explore-page-header"><h1 class="explore-title">⭐ Community Reviews & Ratings</h1><p class="explore-subtitle">Share your experiences and discover what others think about Japanese cities</p></div>', unsafe_allow_html=True)


def _render_rating_stars(rating: float) -> str:
    """Render star rating display."""
    full_stars = int(rating)
    has_half = rating - full_stars >= 0.5
    
    stars = "⭐" * full_stars
    if has_half:
        stars += "✨"
    
    return stars


def _render_review_form(city_id: int, existing_review: dict | None = None) -> None:
    """Render review submission/edit form."""
    city = get_city_by_id(city_id)
    if not city:
        return
    
    uid = _current_user_id()
    if not uid:
        st.warning("🔐 Please log in to write a review.")
        return
    
    st.markdown(f'<div class="review-form-container"><h3>📝 {"Edit Your Review" if existing_review else "Write a Review"} for {city["name"]}</h3></div>', unsafe_allow_html=True)
    
    with st.form(key=f"review_form_{city_id}"):
        rating = st.slider(
            "⭐ Rating",
            min_value=1,
            max_value=5,
            value=existing_review["rating"] if existing_review else 5,
            step=1,
            help="Rate your experience from 1 to 5 stars"
        )
        
        review_text = st.text_area(
            "💬 Your Review",
            value=existing_review["review_text"] if existing_review else "",
            placeholder="Share your experience visiting this city...",
            height=150,
            help="Tell others about your experience, tips, or recommendations"
        )
        
        col_submit, col_cancel = st.columns([1, 1])
        with col_submit:
            submit_button = st.form_submit_button(
                "✅ Submit Review",
                use_container_width=True,
                type="primary"
            )
        with col_cancel:
            cancel_button = st.form_submit_button(
                "✕ Cancel",
                use_container_width=True
            )
        
        if submit_button:
            if existing_review:
                success = update_review(uid, city_id, rating, review_text)
                if success:
                    st.success("✅ Review updated successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to update review.")
            else:
                review_id = add_review(uid, city_id, rating, review_text)
                if review_id:
                    st.success("✅ Review submitted successfully!")
                    st.rerun()
                else:
                    st.error("❌ You have already reviewed this city.")
        
        if cancel_button:
            st.rerun()


def _render_city_reviews(city_id: int) -> None:
    """Render reviews for a specific city."""
    city = get_city_by_id(city_id)
    if not city:
        return
    
    uid = _current_user_id()
    reviews = get_reviews_by_city(city_id)
    avg_rating = get_city_average_rating(city_id)
    rating_count = get_city_rating_count(city_id)
    
    st.markdown(f'<div class="city-reviews-header"><h2>📍 Reviews for {city["name"]}</h2></div>', unsafe_allow_html=True)
    
    # Rating summary
    st.markdown('<div class="rating-summary">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="rating-card"><div class="rating-number">{avg_rating}</div><div class="rating-label">Average Rating</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="rating-card"><div class="rating-number">{rating_count}</div><div class="rating-label">Total Reviews</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="rating-card"><div class="rating-stars">{_render_rating_stars(avg_rating)}</div><div class="rating-label">Star Rating</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # User's existing review (if any)
    if uid:
        existing_review = get_user_review_for_city(uid, city_id)
        if existing_review:
            st.markdown("---")
            with st.expander(f"✏️ Your Review ({_render_rating_stars(existing_review['rating'])})", expanded=False):
                st.markdown(f'<div class="user-review-text">{existing_review["review_text"] or "No text provided"}</div>', unsafe_allow_html=True)
                st.markdown(f'<small class="review-date">Reviewed on {existing_review["created_at"][:10]}</small>', unsafe_allow_html=True)
                
                col_edit, col_delete = st.columns([1, 1])
                with col_edit:
                    if st.button("✏️ Edit Review", key=f"edit_review_{city_id}", use_container_width=True):
                        st.session_state[f"editing_review_{city_id}"] = True
                        st.rerun()
                with col_delete:
                    if st.button("🗑️ Delete Review", key=f"delete_review_{city_id}", use_container_width=True):
                        if delete_review(uid, city_id):
                            st.success("✅ Review deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete review.")
    
    # Review form
    if uid:
        if not get_user_review_for_city(uid, city_id):
            st.markdown("---")
            _render_review_form(city_id)
        elif st.session_state.get(f"editing_review_{city_id}"):
            st.markdown("---")
            _render_review_form(city_id, get_user_review_for_city(uid, city_id))
    else:
        st.info("🔐 Log in to write a review for this city.")
    
    # All reviews
    st.markdown("---")
    st.markdown(f'<div class="all-reviews-header"><h3>💬 All Reviews ({len(reviews)})</h3></div>', unsafe_allow_html=True)
    
    if not reviews:
        st.markdown('<div class="empty-reviews"><div class="empty-icon">💬</div><h3>No reviews yet</h3><p>Be the first to review {city["name"]}!</p></div>', unsafe_allow_html=True)
    else:
        for review in reviews:
            st.markdown(f'<div class="review-card"><div class="review-header"><div class="review-author">👤 {review["username"]}</div><div class="review-rating">{_render_rating_stars(review["rating"])}</div></div><div class="review-content">{review["review_text"] or "No text provided"}</div><div class="review-footer"><small class="review-date">📅 {review["created_at"][:10]}</small></div></div>', unsafe_allow_html=True)


def _render_my_reviews() -> None:
    """Render reviews written by the current user."""
    uid = _current_user_id()
    if not uid:
        st.warning("🔐 Please log in to view your reviews.")
        return
    
    reviews = get_reviews_by_user(uid)
    
    st.markdown('<div class="my-reviews-header"><h2>📝 My Reviews</h2></div>', unsafe_allow_html=True)
    
    if not reviews:
        st.markdown('<div class="empty-reviews"><div class="empty-icon">📝</div><h3>You haven\'t written any reviews yet</h3><p>Start exploring cities and share your experiences!</p></div>', unsafe_allow_html=True)
        return
    
    for review in reviews:
        st.markdown(f'<div class="review-card"><div class="review-header"><div class="review-city">📍 {review["city_name"]}</div><div class="review-rating">{_render_rating_stars(review["rating"])}</div></div><div class="review-content">{review["review_text"] or "No text provided"}</div><div class="review-footer"><small class="review-date">📅 Reviewed on {review["created_at"][:10]}</small></div></div>', unsafe_allow_html=True)
        
        col_edit, col_delete = st.columns([1, 1])
        with col_edit:
            if st.button("✏️ Edit", key=f"my_review_edit_{review['id']}", use_container_width=True):
                st.session_state[f"editing_review_{review['city_id']}"] = True
                st.session_state.selected_city_for_review = review["city_id"]
                st.rerun()
        with col_delete:
            if st.button("🗑️ Delete", key=f"my_review_delete_{review['id']}", use_container_width=True):
                if delete_review(uid, review["city_id"]):
                    st.success("✅ Review deleted successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to delete review.")


def _render_all_reviews() -> None:
    """Render all reviews across all cities."""
    reviews = get_all_reviews()
    
    st.markdown('<div class="all-reviews-header"><h2>💬 All Community Reviews</h2></div>', unsafe_allow_html=True)
    
    if not reviews:
        st.markdown('<div class="empty-reviews"><div class="empty-icon">💬</div><h3>No reviews yet</h3><p>Be the first to share your experience!</p></div>', unsafe_allow_html=True)
        return
    
    st.markdown(f'<div class="results-count">Showing <strong>{len(reviews)}</strong> reviews</div>', unsafe_allow_html=True)
    
    for review in reviews:
        st.markdown(f'<div class="review-card"><div class="review-header"><div class="review-author">👤 {review["username"]}</div><div class="review-city">📍 {review["city_name"]}</div><div class="review-rating">{_render_rating_stars(review["rating"])}</div></div><div class="review-content">{review["review_text"] or "No text provided"}</div><div class="review-footer"><small class="review-date">📅 {review["created_at"][:10]}</small></div></div>', unsafe_allow_html=True)


def show() -> None:
    """Main reviews page."""
    _render_page_header()
    
    # Check if a specific city was selected from city details
    if "reviews_city_id" in st.session_state:
        city_id = st.session_state.reviews_city_id
        city = get_city_by_id(city_id)
        if city:
            _render_city_reviews(city_id)
            # Clear the selection after rendering
            if "reviews_city_id" in st.session_state:
                del st.session_state.reviews_city_id
            return
    
    # Initialize session state
    if "reviews_view" not in st.session_state:
        st.session_state.reviews_view = "All Reviews"
    
    uid = _current_user_id()
    
    # View selector
    st.markdown('<div class="view-selector">', unsafe_allow_html=True)
    view_options = ["All Reviews"]
    if uid:
        view_options.insert(0, "My Reviews")
    
    selected_view = st.selectbox(
        "📋 Select View",
        view_options,
        index=0,
        key="reviews_view_selector",
        label_visibility="collapsed"
    )
    st.session_state.reviews_view = selected_view
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # City selector for city-specific reviews
    if selected_view == "All Reviews":
        all_cities = get_all_cities()
        city_names = sorted([city["name"] for city in all_cities])
        
        st.markdown('<div class="city-selector">', unsafe_allow_html=True)
        selected_city_name = st.selectbox(
            "🏙️ Select a city to view reviews",
            ["All Cities"] + city_names,
            key="reviews_city_selector"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        if selected_city_name == "All Cities":
            _render_all_reviews()
        else:
            city = next((c for c in all_cities if c["name"] == selected_city_name), None)
            if city:
                _render_city_reviews(city["id"])
            else:
                st.error("City not found.")
    elif selected_view == "My Reviews":
        _render_my_reviews()
