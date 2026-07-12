"""
Sakura AI — Japan Travel Consultant
Beautiful chat interface for ExploreJP.
"""
from __future__ import annotations

import os
import streamlit as st

from explorejp.ai.engine import llm_response, is_llm_available, llm_unavailable_reason
from explorejp.ai.actions import parse_and_execute


# ── Quick-action suggestion chips ────────────────────────────────────────────

SUGGESTION_CHIPS = [
    ("🗾", "Recommend a city for me"),
    ("🌸", "Best cities for cherry blossoms"),
    ("🍜", "What should I eat in Tokyo?"),
    ("💰", "Budget travel tips for Japan"),
    ("🙏", "Japanese etiquette guide"),
    ("🧳", "Help me plan a 10-day trip"),
    ("📷", "Photography tips for sakura"),
    ("❄️", "Best city to visit in winter"),
]


# ── Session state helpers ─────────────────────────────────────────────────────

def _init_chat():
    if "sakura_ai_messages" not in st.session_state:
        st.session_state.sakura_ai_messages = []
    if "sakura_ai_initialized" not in st.session_state:
        st.session_state.sakura_ai_initialized = False


def _add_message(role: str, content: str):
    st.session_state.sakura_ai_messages.append({"role": role, "content": content})


def _get_messages() -> list[dict]:
    return st.session_state.sakura_ai_messages


# ── Page ──────────────────────────────────────────────────────────────────────

def show():
    _init_chat()
    user = st.session_state.get("user")
    user_id = user["id"] if user else None

    _render_header(user)
    _render_mode_badge()

    # Auto-greet on first visit
    if not st.session_state.sakura_ai_initialized:
        greeting = llm_response(
            [{"role": "user", "content": "hello"}],
            user_id=user_id,
        )
        _add_message("assistant", greeting)
        st.session_state.sakura_ai_initialized = True

    # Suggestion chips — only when chat is empty (after greeting)
    if len(_get_messages()) <= 1:
        _render_chips(user_id)

    # Chat history
    _render_chat_history()

    # Input box at the bottom
    _render_input(user_id)


# ── Sub-components ────────────────────────────────────────────────────────────

def _render_header(user):
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #6C0820 0%, #305D91 100%);
                border-radius: 20px;
                padding: 28px 32px;
                margin-bottom: 8px;
            ">
                <h1 style="color:white;margin:0;font-size:2rem;">🌸 Sakura AI</h1>
                <p style="color:rgba(255,255,255,0.85);margin:6px 0 0;font-size:1.05rem;">
                    Your personal Japan travel consultant — powered by ExploreJP's own database
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.write("")
        st.write("")
        if st.button("🗑️ Clear", key="sakura_clear_chat", help="Clear conversation"):
            st.session_state.sakura_ai_messages = []
            st.session_state.sakura_ai_initialized = False
            st.rerun()


def _render_mode_badge():
    reason = llm_unavailable_reason()
    if not reason:
        st.success("🤖 AI mode active — conversational responses powered by Groq", icon="✅")
    elif reason == "no_key":
        st.info(
            "📚 Database mode — answering from ExploreJP's own data. "
            "Add your `GROQ_API_KEY` to `.env` to enable full AI conversations.",
            icon="ℹ️",
        )
    else:
        st.warning(f"⚠️ AI unavailable: {reason}. Running in database mode.", icon="⚠️")


def _render_chips(user_id: int | None):
    st.markdown("**Try asking:**")
    cols = st.columns(4)
    for i, (icon, label) in enumerate(SUGGESTION_CHIPS):
        with cols[i % 4]:
            if st.button(f"{icon} {label}", key=f"chip_{i}", use_container_width=True):
                _add_message("user", label)
                _generate_and_store(label, user_id)
                st.rerun()
    st.markdown("---")


def _render_chat_history():
    messages = _get_messages()
    for msg in messages:
        role = msg["role"]
        content = msg["content"]

        if role == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(content)
        else:
            with st.chat_message("assistant", avatar="🌸"):
                st.markdown(content)
                # Show action confirmations stored alongside message
                for conf in msg.get("confirmations", []):
                    st.success(conf)


def _render_input(user_id: int | None):
    if prompt := st.chat_input("Ask Sakura AI anything about Japan travel..."):
        _add_message("user", prompt)
        _generate_and_store(prompt, user_id)
        st.rerun()


def _generate_and_store(user_message: str, user_id: int | None):
    """Call the AI engine, parse actions, and store the assistant message."""
    messages = _get_messages()
    # Build the messages list for the LLM (only role/content pairs)
    api_messages = [{"role": m["role"], "content": m["content"]} for m in messages]

    with st.spinner("Sakura AI is thinking... 🌸"):
        raw_response = llm_response(api_messages, user_id=user_id)

    # Parse and execute any embedded action tags
    clean_response, confirmations = parse_and_execute(raw_response, user_id)

    # Store with confirmations attached so they render next to the message
    st.session_state.sakura_ai_messages.append({
        "role": "assistant",
        "content": clean_response,
        "confirmations": confirmations,
    })


# ── Settings helper (shown in sidebar by app.py) ─────────────────────────────

def render_api_key_sidebar():
    """
    Small sidebar widget to set GROQ_API_KEY at runtime without restarting.
    """
    reason = llm_unavailable_reason()

    if not reason:
        return  # AI is working fine, nothing to show

    with st.sidebar.expander("🔑 Enable AI mode", expanded=False):
        st.caption("Enter your Groq API key. Free at console.groq.com — no credit card needed.")
        key = st.text_input("Groq API Key", type="password",
                            placeholder="gsk_...", key="sidebar_groq_key")
        if st.button("Activate", key="activate_groq", use_container_width=True):
            if key and key.startswith("gsk_"):
                os.environ["GROQ_API_KEY"] = key
                st.success("AI mode activated!")
                st.rerun()
            else:
                st.error("Invalid key — Groq keys start with gsk_")
