"""Personal dashboard page for logged-in users."""

import streamlit as st
from explorejp.database import (
    get_user_favorites,
    get_recently_viewed,
    get_bucket_list,
    get_user_itineraries,
    remove_user_favorite,
    remove_from_bucket_list,
)

CITY_IMAGE_URLS = {
    "Tokyo":     "https://i.pinimg.com/736x/76/45/d6/7645d66eecaa75d475a0a3878a0b6d4e.jpg",
    "Kyoto":     "https://i.pinimg.com/1200x/5c/b8/2d/5cb82d83bc50e60e7bcd7d6fed32d2ca.jpg",
    "Osaka":     "https://i.pinimg.com/1200x/0e/fd/0c/0efd0c03b5d991764de6e1f6062a9867.jpg",
    "Sapporo":   "https://i.pinimg.com/1200x/4e/57/eb/4e57eba5f801825791e821fbacbc57db.jpg",
    "Nara":      "https://i.pinimg.com/1200x/c3/22/4f/c3224f143c8f07d1077a12ed3de23c5d.jpg",
    "Fukuoka":   "https://i.pinimg.com/1200x/ae/27/30/ae27305e760e790c49f0d4b83ba27abf.jpg",
    "Hiroshima": "https://i.pinimg.com/1200x/86/8d/21/868d2104a4cd9c10fc5a2f77e670d6a2.jpg",
    "Sendai":    "https://images.unsplash.com/photo-1524413840807-0c3cb6fa808d?auto=format&fit=crop&w=800&q=80",
}

def _city_img(name: str) -> str:
    return CITY_IMAGE_URLS.get(
        name,
        "https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=800&q=80",
    )


def show():
    """Display the personal dashboard."""

    user = st.session_state.get("user")
    if not user:
        st.warning("Please log in to view your dashboard.")
        return

    user_id = user["id"]

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(f"## 👋 Welcome back, {user['username']}!")

    # Show preferences badge if set
    badges = []
    if user.get("favorite_season"):
        badges.append(f"🌸 Favorite season: **{user['favorite_season']}**")
    if user.get("preferred_budget"):
        badges.append(f"💰 Budget: **{user['preferred_budget']}**")
    if badges:
        st.markdown("  •  ".join(badges))

    st.markdown("---")

    # ── Stats row ─────────────────────────────────────────────────────────────
    favorites   = get_user_favorites(user_id)
    bucket      = get_bucket_list(user_id)
    trips       = get_user_itineraries(user_id)
    recent      = get_recently_viewed(user_id)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("❤️ Favorites",      len(favorites))
    c2.metric("✈️ Saved Trips",    len(trips))
    c3.metric("🌸 Bucket List",    len(bucket))
    c4.metric("📍 Recently Viewed", len(recent))

    st.markdown("---")

    # ── Favorites ─────────────────────────────────────────────────────────────
    st.markdown("### ❤️ My Favorite Cities")
    if not favorites:
        st.info("You haven't saved any favorites yet. Explore cities and click 🤍 to save them.")
    else:
        cols = st.columns(min(len(favorites), 3))
        for i, city in enumerate(favorites[:6]):
            with cols[i % 3]:
                st.image(_city_img(city["name"]), use_container_width=True)
                st.markdown(f"**{city['name']}**")
                st.caption(f"📍 {city['region']}  •  🌸 {city['best_season']}")
                if st.button("💔 Remove", key=f"dash_fav_rm_{city['id']}", use_container_width=True):
                    remove_user_favorite(user_id, city["id"])
                    st.rerun()
        if len(favorites) > 6:
            st.caption(f"+ {len(favorites) - 6} more favorites")

    st.markdown("---")

    # ── Recently Viewed ───────────────────────────────────────────────────────
    st.markdown("### 📍 Recently Viewed")
    if not recent:
        st.info("Cities you view will appear here.")
    else:
        cols = st.columns(min(len(recent), 3))
        for i, city in enumerate(recent[:6]):
            with cols[i % 3]:
                st.image(_city_img(city["name"]), use_container_width=True)
                st.markdown(f"**{city['name']}**")
                st.caption(f"📍 {city['region']}")

    st.markdown("---")

    # ── Saved Trips ───────────────────────────────────────────────────────────
    st.markdown("### ✈️ My Saved Trips")
    if not trips:
        st.info("No trips yet. Head to Plan Your Trip to create one.")
    else:
        for trip in trips[:5]:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**🗓️ {trip['name']}**")
                    budget_str = f"${trip['budget']:,.0f}" if trip['budget'] else 'No budget set'
                    st.caption(
                        f"{trip['start_date']} → {trip['end_date']}  •  "
                        f"{trip['season']}  •  "
                        f"{budget_str}"
                    )
                with col2:
                    if st.button("Open", key=f"dash_trip_{trip['id']}", use_container_width=True):
                        st.session_state.current_itinerary_id = trip["id"]
                        st.session_state.page = "🧳 Plan Your Trip"
                        st.rerun()

    st.markdown("---")

    # ── Bucket List ───────────────────────────────────────────────────────────
    st.markdown("### 🌸 My Bucket List")
    if not bucket:
        st.info("No cities in your bucket list yet. Add cities you dream of visiting!")
    else:
        cols = st.columns(min(len(bucket), 3))
        for i, city in enumerate(bucket[:6]):
            with cols[i % 3]:
                st.image(_city_img(city["name"]), use_container_width=True)
                st.markdown(f"**{city['name']}**")
                st.caption(f"📍 {city['region']}  •  🌸 {city['best_season']}")
                if st.button("Remove", key=f"dash_bl_rm_{city['id']}", use_container_width=True):
                    remove_from_bucket_list(user_id, city["id"])
                    st.rerun()
        if len(bucket) > 6:
            st.caption(f"+ {len(bucket) - 6} more in bucket list")
