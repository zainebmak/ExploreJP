"""
engine.py
Sakura AI engine.

Phase 2: Pure database-driven responses (always available, no API key needed).
Phase 3: LLM-powered conversational responses grounded in DB context (requires GROQ_API_KEY).
         Uses Groq — free tier, no credit card, ultra-fast inference.
         Get a free key at: https://console.groq.com
"""
from __future__ import annotations

import os

# Ensure .env is loaded whenever this module is first imported
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass

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
- To navigate to a page: [ACTION:NAVIGATE:PageName]

--- GROUNDING CONTEXT ---
{context}
--- END CONTEXT ---
"""

# ── Fallback DB-only responses (Phase 2) ─────────────────────────────────────

def _db_response(message: str, user_id: int | None) -> str:
    """Rule-based responses using only the database. No API key needed."""
    msg = message.lower().strip()

    city_mentions = [name for name in
                     ["tokyo", "kyoto", "osaka", "hiroshima", "sapporo",
                      "fukuoka", "nara", "sendai"]
                     if name in msg]

    # Food
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
        if any(w in msg for w in ["low", "cheap", "backpack"]):
            budget_level = "Budget"
        elif any(w in msg for w in ["luxury", "high-end", "splurge"]):
            budget_level = "Luxury"
        elif any(w in msg for w in ["mid", "moderate"]):
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
        lines = ["💰 **Japan Budget Overview**\n"]
        for level, info in BUDGET_GUIDE.items():
            lines.append(f"**{level}:** {info['daily_range']}")
        lines.append("\nTell me your budget style (Budget / Mid-range / Luxury) for detailed advice!")
        return "\n".join(lines)

    # Culture
    if any(w in msg for w in ["culture", "etiquette", "custom", "rude", "polite", "onsen", "shoes", "bow", "tipping"]):
        topic_map = {
            "shoes": "shoes", "onsen": "onsen", "eat": "eating", "food": "eating",
            "tip": "eating", "train": "trains", "cash": "cash", "language": "language",
            "bow": "greetings", "hello": "greetings", "temple": "temple_etiquette",
        }
        for word, topic in topic_map.items():
            if word in msg and topic in CULTURE_GUIDE:
                return f"🙏 **{topic.replace('_', ' ').title()}**\n\n{CULTURE_GUIDE[topic]}"
        lines = ["🙏 **Japanese Etiquette Quick Guide**\n"]
        for topic, advice in list(CULTURE_GUIDE.items())[:5]:
            lines.append(f"**{topic.replace('_', ' ').title()}:** {advice[:100]}...")
        lines.append("\nAsk about a specific topic for more detail!")
        return "\n".join(lines)

    # City info
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

    # Recommendations
    if any(w in msg for w in ["recommend", "suggest", "where", "visit", "best city", "which city"]):
        from explorejp.database import get_all_cities
        lines = ["🗾 **Japan Cities at a Glance**\n"]
        for c in get_all_cities()[:6]:
            lines.append(
                f"**{c['name']}** ({c['region']}) — {c['best_season'].split()[0]} | "
                f"Cost: {c['cost_of_living']} | "
                f"{c['known_for'].replace('|', ', ')[:60]}..."
            )
        lines.append("\nTell me your interests, season, and budget for a personalised recommendation!")
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

    return (
        "I specialise in Japan travel! Try asking:\n\n"
        "• *What should I eat in Osaka?*\n"
        "• *Best cities for cherry blossoms?*\n"
        "• *Mid-range budget tips for Japan?*\n"
        "• *Tell me about Japanese etiquette*\n"
        "• *Recommend a city for a first-time visitor*"
    )


# ── LLM engine (Phase 3) — Groq (free, no credit card) ───────────────────────

def _get_groq_key() -> str:
    """Return the Groq key, reloading .env each time to defeat Streamlit's module cache."""
    try:
        from dotenv import load_dotenv
        load_dotenv(override=True)
    except ImportError:
        pass
    return os.environ.get("GROQ_API_KEY", "").strip()


def is_llm_available() -> bool:
    """True when a valid-looking GROQ_API_KEY is set and groq package is installed."""
    key = _get_groq_key()
    # Groq keys start with gsk_ — reject anything that looks like an OpenAI key or placeholder
    if not key or not key.startswith("gsk_") or len(key) < 20:
        return False
    try:
        import groq  # noqa: F401
        return True
    except ImportError:
        return False


def llm_unavailable_reason() -> str:
    key = _get_groq_key()
    if not key or not key.startswith("gsk_") or len(key) < 20:
        return "no_key"
    try:
        import groq  # noqa: F401
        return ""
    except ImportError:
        return "not_installed"


def llm_response(
    messages: list[dict],
    user_id: int | None = None,
    model: str = "llama-3.3-70b-versatile",
) -> str:
    """
    Generate a response using Groq (free tier).
    Falls back to rule-based DB responses when no key is configured.
    """
    user_message = messages[-1]["content"] if messages else ""

    if not is_llm_available():
        return _db_response(user_message, user_id)

    try:
        from groq import Groq

        api_key = _get_groq_key()
        client = Groq(api_key=api_key)
        context = build_full_context(user_id)
        system_content = SYSTEM_PROMPT_TEMPLATE.format(context=context)

        history = messages[-10:] if len(messages) > 10 else messages
        api_messages = [{"role": "system", "content": system_content}] + [
            {"role": m["role"], "content": m["content"]} for m in history
        ]

        response = client.chat.completions.create(
            model=model,
            messages=api_messages,
            temperature=0.7,
            max_tokens=800,
        )
        return response.choices[0].message.content or ""

    except Exception as e:
        key_hint = api_key[:10] + "..." if api_key else "EMPTY"
        raw_env_key = os.environ.get("GROQ_API_KEY", "NO_KEY_IN_ENV")
        return (
            f"⚠️ **Debug info:**\n"
            f"- Error: `{type(e).__name__}: {str(e)[:120]}`\n"
            f"- Key passed to Groq: `{key_hint}` (len={len(api_key)})\n"
            f"- Raw env key: `{raw_env_key[:15]}...` (len={len(raw_env_key)})\n\n"
            f"{_db_response(user_message, user_id)}"
        )
