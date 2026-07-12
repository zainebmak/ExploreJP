"""Login and Register page for ExploreJP."""

import streamlit as st
from explorejp.database import create_user, verify_password


def show():
    """Show login or register form based on tab selection."""

    st.markdown("""
    <style>
    .auth-container {
        max-width: 480px;
        margin: 40px auto;
        padding: 40px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 4px 24px rgba(108,8,32,0.08);
    }
    .auth-title {
        font-size: 32px;
        font-weight: bold;
        color: #6C0820;
        text-align: center;
        margin-bottom: 6px;
    }
    .auth-subtitle {
        text-align: center;
        color: #888;
        margin-bottom: 28px;
        font-size: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="auth-title">🌸 ExploreJP</div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-subtitle">Your personal Japan travel guide</div>',
                    unsafe_allow_html=True)

        tab_login, tab_register = st.tabs(["🔑 Log In", "✨ Create Account"])

        with tab_login:
            _show_login()

        with tab_register:
            _show_register()


def _show_login():
    with st.form("login_form"):
        st.markdown("#### Welcome back")
        username = st.text_input("Username", placeholder="your username")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        submitted = st.form_submit_button("Log In", use_container_width=True)

    if submitted:
        if not username or not password:
            st.error("Please enter your username and password.")
            return
        user = verify_password(username, password)
        if user:
            st.session_state.user = {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "preferred_theme": user.get("preferred_theme", "light"),
                "favorite_season": user.get("favorite_season", ""),
                "preferred_budget": user.get("preferred_budget", ""),
            }
            st.session_state.page = "🏠 Home"
            st.success(f"Welcome back, {user['username']}! 🌸")
            st.rerun()
        else:
            st.error("Incorrect username or password.")


def _show_register():
    with st.form("register_form"):
        st.markdown("#### Create your ExploreJP Account")
        username = st.text_input("Username", placeholder="choose a username", key="reg_username")
        email = st.text_input("Email", placeholder="you@example.com", key="reg_email")
        password = st.text_input("Password", type="password",
                                 placeholder="at least 6 characters", key="reg_password")
        confirm = st.text_input("Confirm Password", type="password",
                                placeholder="repeat your password", key="reg_confirm")
        submitted = st.form_submit_button("Create Account", use_container_width=True)

    if submitted:
        if not all([username, email, password, confirm]):
            st.error("Please fill in all fields.")
            return
        if len(password) < 6:
            st.error("Password must be at least 6 characters.")
            return
        if password != confirm:
            st.error("Passwords do not match.")
            return
        if "@" not in email:
            st.error("Please enter a valid email address.")
            return

        user_id = create_user(username, email, password)
        if user_id is None:
            st.error("That username or email is already taken. Please choose another.")
            return

        st.session_state.user = {
            "id": user_id,
            "username": username,
            "email": email,
            "preferred_theme": "light",
            "favorite_season": "",
            "preferred_budget": "",
        }
        st.session_state.page = "🏠 Home"
        st.success(f"Account created! Welcome to ExploreJP, {username}! 🌸")
        st.rerun()
