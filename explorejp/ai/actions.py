"""
actions.py
Phase 4 — Sakura AI can perform actions inside ExploreJP.

The engine embeds structured action tags in its text responses:
    [ACTION:ADD_FAVORITE:Tokyo]
    [ACTION:ADD_BUCKET:Kyoto]
    [ACTION:CREATE_TRIP:name=Spring Tour|start=2025-03-28|end=2025-04-05|season=Spring|interests=Culture,Food|budget=2000]
    [ACTION:NAVIGATE:Explore Cities]

This module parses those tags, executes them against the DB, and returns
a human-readable confirmation message.
"""
from __future__ import annotations

import re
import streamlit as st

from explorejp.database import (
    add_user_favorite,
    add_to_bucket_list,
    create_user_itinerary,
    get_all_cities,
)


# ── Action parsing ────────────────────────────────────────────────────────────

ACTION_PATTERN = re.compile(r"\[ACTION:([A-Z_]+):([^\]]*)\]")

# Page name → session state page key used by app.py router
PAGE_MAP = {
    "explore cities":         "🗺️ Explore Cities",
    "cherry blossom guide":   "🌸 Cherry Blossom Guide",
    "cherry blossom":         "🌸 Cherry Blossom Guide",
    "plan your trip":         "🧳 Plan Your Trip",
    "plan trip":              "🧳 Plan Your Trip",
    "dashboard":              "📊 Dashboard",
}


def _find_city_id(city_name: str) -> int | None:
    """Case-insensitive city name → id lookup."""
    cities = get_all_cities()
    name_lower = city_name.strip().lower()
    for c in cities:
        if c["name"].lower() == name_lower or name_lower in c["name"].lower():
            return c["id"]
    return None


def parse_and_execute(response_text: str, user_id: int | None) -> tuple[str, list[str]]:
    """
    Find all ACTION tags in *response_text*, execute them, strip the tags from
    the text, and return (clean_text, list_of_confirmation_messages).
    """
    confirmations: list[str] = []
    clean_text = response_text

    for match in ACTION_PATTERN.finditer(response_text):
        action_type = match.group(1)
        payload = match.group(2)
        tag = match.group(0)  # full [ACTION:...] string to strip

        msg = _execute_action(action_type, payload, user_id)
        if msg:
            confirmations.append(msg)

        # Remove tag from response text
        clean_text = clean_text.replace(tag, "").strip()

    return clean_text, confirmations


def _execute_action(action_type: str, payload: str, user_id: int | None) -> str | None:
    """Execute a single action. Returns a confirmation string or None."""

    # ── ADD_FAVORITE ──────────────────────────────────────────────────────────
    if action_type == "ADD_FAVORITE":
        if not user_id:
            return "ℹ️ Log in to save favourites."
        city_id = _find_city_id(payload)
        if city_id is None:
            return f"⚠️ City '{payload}' not found in database."
        ok = add_user_favorite(user_id, city_id)
        if ok:
            # Update session state immediately
            return f"❤️ **{payload}** added to your favourites!"
        return f"ℹ️ **{payload}** is already in your favourites."

    # ── ADD_BUCKET ────────────────────────────────────────────────────────────
    if action_type == "ADD_BUCKET":
        if not user_id:
            return "ℹ️ Log in to use the bucket list."
        city_id = _find_city_id(payload)
        if city_id is None:
            return f"⚠️ City '{payload}' not found in database."
        ok = add_to_bucket_list(user_id, city_id)
        if ok:
            return f"🌸 **{payload}** added to your bucket list!"
        return f"ℹ️ **{payload}** is already in your bucket list."

    # ── CREATE_TRIP ───────────────────────────────────────────────────────────
    if action_type == "CREATE_TRIP":
        if not user_id:
            return "ℹ️ Log in to save trips."
        params: dict[str, str] = {}
        for part in payload.split("|"):
            if "=" in part:
                k, v = part.split("=", 1)
                params[k.strip()] = v.strip()

        name      = params.get("name", "AI Suggested Trip")
        start     = params.get("start", "2025-04-01")
        end       = params.get("end", "2025-04-10")
        season    = params.get("season", "Spring")
        interests = params.get("interests", "Culture, Sightseeing")
        budget_s  = params.get("budget", "")
        budget    = float(budget_s) if budget_s and budget_s.replace(".", "").isdigit() else None

        trip_id = create_user_itinerary(
            user_id=user_id,
            name=name,
            start_date=start,
            end_date=end,
            season=season,
            interests=interests,
            budget=budget,
        )
        # Store in session so Plan Your Trip page can open it
        st.session_state.current_itinerary_id = trip_id
        return (
            f"🧳 Trip **'{name}'** created! "
            f"({start} → {end}, {season}) — "
            f"Go to **Plan Your Trip** to add cities."
        )

    # ── NAVIGATE ──────────────────────────────────────────────────────────────
    if action_type == "NAVIGATE":
        page = PAGE_MAP.get(payload.strip().lower())
        if page:
            st.session_state.page = page
            st.rerun()
        return None

    return None
