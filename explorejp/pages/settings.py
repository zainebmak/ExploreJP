"""Settings page for ExploreJP."""

import streamlit as st
from explorejp.database import (
    update_user_settings,
    get_user_by_id,
    delete_user,
    get_user_favorites,
    get_recently_viewed,
    get_bucket_list,
)


def show():
    """Display the settings page."""

    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("🏠 Back to Home", key="back_home_settings", use_container_width=True):
            st.session_state.page = "🏠 Home"
            st.rerun()

    user = st.session_state.get("user")
    if not user:
        st.warning("Please log in to access settings.")
        return

    st.markdown("## ⚙️ Account Settings")
    st.markdown(f"Managing settings for **{user['username']}**")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["👤 Profile", "🔒 Security", "🗑️ Danger Zone"])

    with tab1:
        _show_profile_settings(user)

    with tab2:
        _show_security_settings(user)

    with tab3:
        _show_danger_zone(user)


def _show_profile_settings(user: dict):
    st.markdown("### Change Username")
    with st.form("change_username_form"):
        new_username = st.text_input("New Username", value=user["username"])
        new_email = st.text_input("New Email", value=user["email"])
        submitted = st.form_submit_button("Save Changes", use_container_width=True)

    if submitted:
        if not new_username or not new_email:
            st.error("Username and email cannot be empty.")
            return
        if "@" not in new_email:
            st.error("Please enter a valid email address.")
            return
        ok = update_user_settings(user["id"], username=new_username, email=new_email)
        if ok:
            st.session_state.user["username"] = new_username
            st.session_state.user["email"] = new_email
            st.success("Profile updated successfully.")
            st.rerun()
        else:
            st.error("That username or email is already taken.")

    st.markdown("---")
    st.markdown("### Preferences")
    with st.form("preferences_form"):
        season = st.selectbox(
            "Favorite Season",
            ["", "Spring", "Summer", "Autumn", "Winter"],
            index=["", "Spring", "Summer", "Autumn", "Winter"].index(
                user.get("favorite_season") or ""
            ),
        )
        budget = st.selectbox(
            "Preferred Budget",
            ["", "Budget", "Mid-range", "Luxury"],
            index=["", "Budget", "Mid-range", "Luxury"].index(
                user.get("preferred_budget") or ""
            ),
        )
        save_prefs = st.form_submit_button("Save Preferences", use_container_width=True)

    if save_prefs:
        update_user_settings(user["id"], favorite_season=season, preferred_budget=budget)
        st.session_state.user["favorite_season"] = season
        st.session_state.user["preferred_budget"] = budget
        st.success("Preferences saved.")


def _show_security_settings(user: dict):
    st.markdown("### Change Password")
    with st.form("change_password_form"):
        current_pw = st.text_input("Current Password", type="password")
        new_pw = st.text_input("New Password", type="password",
                               help="At least 6 characters")
        confirm_pw = st.text_input("Confirm New Password", type="password")
        submitted = st.form_submit_button("Update Password", use_container_width=True)

    if submitted:
        from explorejp.database import verify_password
        if not verify_password(user["username"], current_pw):
            st.error("Current password is incorrect.")
            return
        if len(new_pw) < 6:
            st.error("New password must be at least 6 characters.")
            return
        if new_pw != confirm_pw:
            st.error("Passwords do not match.")
            return
        update_user_settings(user["id"], password=new_pw)
        st.success("Password changed successfully.")


def _show_danger_zone(user: dict):
    st.markdown("### Delete Account")
    st.warning(
        "Deleting your account is **permanent**. All your favorites, trips, "
        "bucket list, and recently viewed history will be lost."
    )

    with st.form("delete_account_form"):
        confirm_text = st.text_input(
            f'Type **{user["username"]}** to confirm deletion',
            placeholder=user["username"],
        )
        password_confirm = st.text_input("Enter your password to confirm", type="password")
        submitted = st.form_submit_button("🗑️ Delete My Account", use_container_width=True)

    if submitted:
        from explorejp.database import verify_password
        if confirm_text != user["username"]:
            st.error("Username confirmation does not match.")
            return
        if not verify_password(user["username"], password_confirm):
            st.error("Incorrect password.")
            return
        delete_user(user["id"])
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("Your account has been deleted. Goodbye! 👋")
        st.rerun()
