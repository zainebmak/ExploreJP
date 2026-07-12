"""
engine.py
Sakura AI engine.

Phase 2: Pure database-driven responses (always available, no API key needed).
Phase 3: LLM-powered conversational responses grounded in DB context (requires OPENAI_API_KEY).

The engine auto-detects which mode to use based on whether an API key is configured.
"""
from __future__ import annotations

import os
import re
from explorejp.ai.context_builder import (
    build_full_context,
    get_city_info,
    get_food_info,
    get_budget_info,
    get_sakura_tip,
    CULTURE_GUIDE,
    BUDGET_GUIDE,
    FOOD_GUIDE,
    SAKURA_TIPS,
)

# ── System prompt ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT_TEMPLATE = """You are Sakura AI, an expert Japan travel consultant for ExploreJP.
Your personality is warm, knowledgeable, and enthusiastic about Japan.
You speak like a friend who has lived in Japan and loves sharing insider knowledge.

Your expertise covers:
- City recommendations tailored to travellers' interests, budget, and season
- Food guides: local specialties, best areas, budget tips
- Cherry blossom (sakura) season: timing, best spots, crowd levels, photography
- Budget planning: accommodation, transport, daily cost estimates
- Japanese culture and etiquette
- Trip improvement: reviewing itineraries and suggesting enhancements
- Actions: you can save favourites, add to bucket list, and create trip plans for the user

IMPORTANT RULES:
1. ONLY use information from the database context provided below. Do not invent cities, places, or facts not in the context.
2. When recommending cities, always explain WHY based on the user's stated preferences.
3. When the user asks you to DO something (save a city, create a trip), respond with an action tag.
4. Be conversational and warm — not robotic. Use emojis sparingly but naturally (🌸, 🍜, 🗾).
5. Format responses clearly: use bullet points for lists, bold for key terms.
6. If you don't have specific data for something, say so honestly rather than guessing.
7. Always mention practical tips — opening times, crowd tips, budget estimates.

ACTION TAGS (use these exactly when performing actions):
- To save a city as favourite: [ACTION:ADD_FAVORITE:CityName]
- To add to bucket list: [ACTION:ADD_BUCKET:CityName]
- To create a trip: [ACTION:CREATE_TRIP:name=X|start=YYYY-MM-DD|end=YYYY-MM-DD|season=X|interests=X|budget=X]
- To navigate to a page: [ACTION:NAVIGATE:PageName]  (valid pages: Explore Cities, Cherry Blossom Guide, Plan Your Trip, Dashboard)

--- GROUNDING CONTEXT ---
{context}
--- END CONTEXT ---
"""

# ── Fallback DB-only responses (Phase 2) ─────────────────────────────────────

def _db_response(message: str, user_id: int | None) -> str:
    """
    Rule-based responses using only the database.
    Used when no API key is configured or as a fallback.
    """
    msg = message.lower().strip()

    # City recommendation
    city_mentions = [name for name in
                     ["tokyo", "kyoto", "osaka", "hiroshima", "sapporo",
                      "fukuoka", "nara", "sendai"]
                     if name in msg]

    # Food questions
    if any(w in msg for w in ["food", "eat", "restaurant", "cuisine", "dish", "ramen", "sushi", "okonomiyaki"]):
        if city_mentions:
            city = city_mentions[0].title()
            info = get_food_info(city)
            if info:
                return (
                    f"🍜 **{city} Food Guide**\n\n"
                    f"**Must-try dishes:** {', '.join(info['must_try'])}\n\n"
                    f"**Best food areas:** {', '.join(info['areas'])}\n\n"
                    f"**💡 Budget tip:** {info['budget_tip']}"
                )
        # General food overview
        lines = ["🍜 **Japan Food Highlights by City**\n"]
        for city, info in list(FOOD_GUIDE.items())[:4]:
            lines.append(f"**{city}:** {info['must_try'][0]}, {info['must_try'][1]}")
        lines.append("\nAsk me about a specific city for a detailed food guide!")
        return "\n".join(lines)

    # Cherry blossom
    if any(w in msg for w in ["cherry", "sakura", "blossom", "hanami", "bloom"]):
        if city_mentions:
            city = city_mentions[0].title()
            tip = get_sakura_tip(city)
            if tip:
                return f"🌸 **Sakura tips for {city}**\n\n{tip}"
        lines = ["🌸 **Cherry Blossom Season Overview**\n"]
        for city, tip in SAKURA_TIPS.items():
            lines.append(f"**{city}:** {tip[:120]}...")
        lines.append("\nAsk me about a specific city for detailed sakura advice!")
        return "\n".join(lines)

    # Budget
    if any(w in msg for w in ["budget", "cost", "money", "cheap", "expensive", "afford", "price"]):
        budget_level = None
        if "budget" in msg and ("low" in msg or "cheap" in msg or "backpack" in msg):
            budget_level = "Budget"
        elif "luxury" in msg or "high-end" in msg or "splurge" in msg:
            budget_level = "Luxury"
        elif "mid" in msg or "moderate" in msg:
            budget_level = "Mid-range"

        if budget_level:
            info = get_budget_info(budget_level)
            if info:
                return (
                    f"💰 **{budget_level} Travel in Japan**\n\n"
                    f"**Daily budget:** {info['daily_range']}\n\n"
                    f"**Accommodation:** {info['accommodation']}\n\n"
                    f"**Food:** {info['food']}\n\n"
                    f"**Tips:**\n" + "\n".join(f"• {t}" for t in info["tips"])
                )
        # Overview
        lines = ["💰 **Japan Budget Overview**\n"]
        for level, info in BUDGET_GUIDE.items():
            lines.append(f"**{level}:** {info['daily_range']}")
        lines.append("\nTell me your budget style (Budget / Mid-range / Luxury) for detailed advice!")
        return "\n".join(lines)

    # Culture / etiquette
    if any(w in msg for w in ["culture", "etiquette", "custom", "rude", "polite", "onsen", "shoes", "bow", "tip", "tipping"]):
        topic_map = {
            "shoes": "shoes", "onsen": "onsen", "eat": "eating", "food": "eating",
            "tip": "eating", "train": "trains", "cash": "cash", "language": "language",
            "bow": "greetings", "hello": "greetings", "temple": "temple_etiquette",
        }
        found_topic = None
        for word, topic in topic_map.items():
            if word in msg:
                found_topic = topic
                break
        if found_topic and found_topic in CULTURE_GUIDE:
            title = found_topic.replace("_", " ").title()
            return f"🙏 **{title}**\n\n{CULTURE_GUIDE[found_topic]}"

        lines = ["🙏 **Japanese Etiquette Quick Guide**\n"]
        for topic, advice in list(CULTURE_GUIDE.items())[:5]:
            lines.append(f"**{topic.replace('_', ' ').title()}:** {advice[:100]}...")
        lines.append("\nAsk about a specific topic for more detail!")
        return "\n".join(lines)

    # City info / recommendation
    if city_mentions:
        city = city_mentions[0].title()
        info = get_city_info(city)
        if info:
            food = get_food_info(city)
            sakura = get_sakura_tip(city)
            result = (
                f"🗾 **{info['name']}** — {info['region']} Region\n\n"
                f"**Best season:** {info['best_season']}\n"
                f"**Cost of living:** {info['cost_of_living']}\n"
                f"**Population:** {info['population']}\n"
                f"**Known for:** {info['known_for'].replace('|', ', ')}\n"
            )
            if food:
                result += f"\n🍜 **Must eat:** {', '.join(food['must_try'][:3])}\n"
            if sakura:
                result += f"\n🌸 **Sakura tip:** {sakura[:200]}\n"
            return result

    # General recommendation intent
    if any(w in msg for w in ["recommend", "suggest", "where", "visit", "go", "best city", "which city"]):
        cities = get_city_info("") or {}
        from explorejp.database import get_all_cities
        all_cities = get_all_cities()
        lines = ["🗾 **Japan Cities at a Glance**\n"]
        for c in all_cities[:6]:
            lines.append(
                f"**{c['name']}** ({c['region']}) — {c['best_season'].split()[0]} | "
                f"Cost: {c['cost_of_living']} | "
                f"{c['known_for'].replace('|', ', ')[:60]}..."
            )
        lines.append("\nTell me your interests, season, and budget and I'll give you a personalised recommendation!")
        return "\n".join(lines)

    # Greeting
    if any(w in msg for w in ["hello", "hi", "hey", "konnichiwa", "start", "help"]):
        return (
            "🌸 **Konnichiwa! I'm Sakura AI, your personal Japan travel consultant.**\n\n"
            "I can help you with:\n"
            "• 🗾 **City recommendations** — tell me your interests, season & budget\n"
            "• 🍜 **Food guides** — local specialties and best restaurants per city\n"
            "• 🌸 **Cherry blossom advice** — timing, best spots, crowd tips\n"
            "• 💰 **Budget planning** — daily costs for Budget / Mid-range / Luxury travel\n"
            "• 🙏 **Japanese culture** — etiquette, customs, and insider tips\n"
            "• 🧳 **Trip planning** — I can save cities and create itineraries for you\n\n"
            "What would you like to explore? 🗾"
        )

    # Default
    return (
        "I'm not sure I understood that — I specialise in Japan travel! Try asking me:\n\n"
        "• *What should I eat in Osaka?*\n"
        "• *When is the best time to see cherry blossoms in Kyoto?*\n"
        "• *I have a mid-range budget — what's Japan like for cost?*\n"
        "• *Tell me about Japanese etiquette*\n"
        "• *Recommend a city for a first-time visitor*"
    )


# ── LLM engine (Phase 3) ──────────────────────────────────────────────────────

def _get_openai_client():
    """Return an OpenAI client if a key is configured, else None."""
    try:
        from openai import OpenAI
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key or api_key.startswith("sk-your"):
            return None
        return OpenAI(api_key=api_key)
    except ImportError:
        return None


def llm_response(
    messages: list[dict],
    user_id: int | None = None,
    model: str = "gpt-4o-mini",
) -> str:
    """
    Generate a response.
    - With API key → GPT call with full DB context injected as system message.
    - Without API key → fall back to rule-based DB responses.
    """
    client = _get_openai_client()
    user_message = messages[-1]["content"] if messages else ""

    if client is None:
        # Phase 2 fallback
        return _db_response(user_message, user_id)

    # Phase 3: Build context and call the LLM
    context = build_full_context(user_id)
    system_content = SYSTEM_PROMPT_TEMPLATE.format(context=context)

    # Build the messages list for the API call
    # Keep at most last 10 turns to avoid token overflow
    history = messages[-10:] if len(messages) > 10 else messages
    api_messages = [{"role": "system", "content": system_content}] + history

    try:
        response = client.chat.completions.create(
            model=model,
            messages=api_messages,
            temperature=0.7,
            max_tokens=800,
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        # Graceful fallback on any API error
        return (
            f"⚠️ AI service temporarily unavailable ({type(e).__name__}). "
            f"Falling back to database mode:\n\n{_db_response(user_message, user_id)}"
        )


def is_llm_available() -> bool:
    """True if OpenAI key is configured and openai package is installed."""
    return _get_openai_client() is not None
