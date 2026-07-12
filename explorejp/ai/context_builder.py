"""
context_builder.py
Reads ExploreJP's SQLite database and builds structured plain-text context
blocks that are injected into every LLM prompt.  No hallucination — the AI
only knows what we explicitly tell it from our own data.
"""
from __future__ import annotations

from explorejp.database import (
    get_all_cities,
    get_cherry_blossom_cities,
    get_sakura_spots,
    get_user_favorites,
    get_user_itineraries,
    get_bucket_list,
    get_recently_viewed,
)


# ── Static knowledge blocks ───────────────────────────────────────────────────

FOOD_GUIDE: dict[str, dict] = {
    "Tokyo": {
        "must_try": ["Sushi (Tsukiji outer market)", "Ramen (Fuunji or Ichiran)", "Tempura", "Monjayaki"],
        "areas": ["Shibuya food halls", "Asakusa street food", "Shinjuku izakayas"],
        "budget_tip": "Convenience stores (7-Eleven, Lawson) have excellent onigiri and bento from ¥200.",
    },
    "Kyoto": {
        "must_try": ["Kaiseki (multi-course)", "Tofu cuisine (yudofu)", "Matcha sweets", "Obanzai (Kyoto home cooking)"],
        "areas": ["Nishiki Market", "Gion izakayas", "Pontocho alley"],
        "budget_tip": "Nishiki Market lets you graze on small bites — ideal for a cheap lunch.",
    },
    "Osaka": {
        "must_try": ["Takoyaki", "Okonomiyaki", "Kushikatsu", "Negiyaki"],
        "areas": ["Dotonbori", "Shinsekai", "Kuromon Ichiba Market"],
        "budget_tip": "Osaka is Japan's food capital — eat big at lunch when set meals are cheapest.",
    },
    "Hiroshima": {
        "must_try": ["Hiroshima-style okonomiyaki (layered, not mixed)", "Oysters", "Anago rice"],
        "areas": ["Okonomimura building (7 floors of okonomiyaki)"],
        "budget_tip": "Okonomiyaki at ¥900–¥1,200 is a filling, cheap meal.",
    },
    "Sapporo": {
        "must_try": ["Sapporo miso ramen", "Genghis Khan (lamb BBQ)", "Seafood donburi", "Jingisukan"],
        "areas": ["Susukino food district", "Nijo Market"],
        "budget_tip": "Ramen here is a cultural institution — budget ¥800–¥1,200 per bowl.",
    },
    "Fukuoka": {
        "must_try": ["Hakata tonkotsu ramen", "Mentaiko (spicy cod roe)", "Yatai stall food", "Mizutaki"],
        "areas": ["Nakasu yatai stalls (open-air food stalls along the river)", "Tenjin"],
        "budget_tip": "Yatai stalls are atmospheric and cheap — a bowl of ramen + beer is around ¥1,500.",
    },
    "Nara": {
        "must_try": ["Kakinoha-zushi (persimmon leaf sushi)", "Miwa somen noodles", "Kaki (persimmon) sweets"],
        "areas": ["Naramachi old town restaurants"],
        "budget_tip": "Nara is compact — lunch near the deer park is touristy but convenient.",
    },
    "Sendai": {
        "must_try": ["Gyutan (grilled beef tongue)", "Zunda mochi (edamame sweet)", "Sasakamaboko (fish cake)"],
        "areas": ["Kokubuncho entertainment district"],
        "budget_tip": "Gyutan lunch sets run ¥1,500–¥2,000 — cheaper than dinner at the same restaurants.",
    },
}

CULTURE_GUIDE: dict[str, str] = {
    "greetings": "Bow instead of handshaking. A slight bow (15°) is fine for tourists. Say 'arigatou gozaimasu' to thank people.",
    "shoes": "Remove shoes before entering homes, many ryokan, and some traditional restaurants. Look for a step up (genkan) as the cue.",
    "onsen": "Tattoos are often prohibited in public onsen. Wash thoroughly before entering the communal bath. Towels stay outside the water.",
    "temple_etiquette": "Purify hands at the temizuya (water basin) before entering shrines. Don't point at people or objects in shrines.",
    "eating": "It's fine to slurp noodles — it shows enjoyment. Don't tip; it can be considered rude. Pay at the register, not at the table in many places.",
    "trains": "Queue behind the yellow lines. No phone calls in quiet carriages. Give up priority seats. Eating on local trains is frowned upon.",
    "cash": "Japan is still largely cash-based. Always carry yen. ATMs at 7-Eleven and Japan Post accept foreign cards.",
    "trash": "There are almost no public rubbish bins. Carry a small bag for your waste — convenience stores are the best place to dispose of it.",
    "language": "Learning 'sumimasen' (excuse me/sorry) and 'eigo ga hanasemasu ka?' (do you speak English?) goes a long way.",
}

BUDGET_GUIDE: dict[str, dict] = {
    "Budget": {
        "daily_range": "¥5,000–¥8,000 / day (≈ $33–$53)",
        "accommodation": "Hostels (¥2,500–¥4,000/night), capsule hotels (¥3,000–¥5,000/night)",
        "food": "Convenience stores, ramen shops, gyudon chains (Yoshinoya, Sukiya)",
        "transport": "IC card (Suica/Pasmo) for local travel, overnight buses instead of bullet trains",
        "tips": ["Buy a 7-day JR Pass only if you're taking 3+ bullet train journeys",
                 "Free attractions: Shinjuku Gyoen (¥500), Ueno Park (free), Arashiyama (free)",
                 "Lunch sets at restaurants are 30–40% cheaper than dinner menus"],
    },
    "Mid-range": {
        "daily_range": "¥12,000–¥25,000 / day (≈ $80–$165)",
        "accommodation": "Business hotels (¥7,000–¥12,000/night), ryokan (¥15,000+ with meals)",
        "food": "Sit-down restaurants, sushi conveyor belts, izakayas",
        "transport": "Mix of JR Pass and local transit; occasional taxi",
        "tips": ["Book ryokan at least 2 months ahead for sakura / autumn seasons",
                 "Combo tickets for attractions save 20–30%",
                 "IC cards work on most buses, metros, and even some taxis"],
    },
    "Luxury": {
        "daily_range": "¥40,000+ / day (≈ $270+)",
        "accommodation": "Ryokan with kaiseki dinners (¥30,000–¥80,000/night), 5-star hotels",
        "food": "Kaiseki restaurants, Michelin-starred sushi counters, private dining",
        "transport": "Shinkansen, private car hire, chartered experiences",
        "tips": ["Reserve Michelin restaurants 1–3 months ahead via Tableall or Omakase.com",
                 "Hire a private guide for cultural immersion",
                 "Consider a Ryokan-only trip through the Japan alps (Hakone, Kinosaki)"],
    },
}

SAKURA_TIPS = {
    "Tokyo":     "Go to Shinjuku Gyoen at dawn — it opens at 9 AM so arrive right at opening to beat crowds. Chidorigafuchi is magical for rowing boats under the blossoms.",
    "Kyoto":     "Philosopher's Path at 7 AM before the tour groups arrive. Maruyama Park has the famous weeping cherry — illuminated at night during peak.",
    "Osaka":     "Osaka Castle Park is huge and less hectic than Kyoto. Great for a relaxed hanami picnic. Also check Kema Sakuranomiya Park along the river.",
    "Hiroshima": "Sakura at the Peace Memorial Park creates a uniquely moving atmosphere — blossoms frame the A-Bomb Dome. Less crowded than Osaka or Kyoto.",
    "Sapporo":   "Blooms late (late April–early May) — perfect if you've missed the southern season. Maruyama Park is the main spot. Hokkaido University campus is stunning.",
    "Fukuoka":   "Maizuru Park inside Fukuoka Castle ruins is the best spot. Also Nishi Park has panoramic views over the city through the blossoms.",
    "Nara":      "Nara Park with free-roaming deer under blossoms is a uniquely magical scene. Yoshino Mountain (day trip) has one of Japan's most famous sakura displays.",
    "Sendai":    "Tsutsujigaoka Park has 1,200 trees. Less crowded than central Japan — great if you want a genuine local hanami experience.",
}


# ── Dynamic context from DB ───────────────────────────────────────────────────

def build_cities_context() -> str:
    """Return a concise text block of all cities from the DB."""
    cities = get_all_cities()
    lines = ["=== CITIES IN EXPLOREJP DATABASE ==="]
    for c in cities:
        lines.append(
            f"• {c['name']} | Region: {c['region']} | Best season: {c['best_season']} "
            f"| Cost: {c['cost_of_living']} | Pop: {c['population']} "
            f"| Known for: {c['known_for'].replace('|', ', ')}"
        )
    return "\n".join(lines)


def build_sakura_context() -> str:
    """Return cherry blossom data from the DB."""
    cities = get_cherry_blossom_cities()
    lines = ["=== CHERRY BLOSSOM DATA ==="]
    for c in cities:
        spots = get_sakura_spots(c["city_id"])
        spot_names = ", ".join(s["name"] for s in spots) if spots else "N/A"
        lines.append(
            f"• {c['name']} | Peak: {c['peak_bloom_start']} → {c['peak_bloom_end']} "
            f"| Crowd: {c['crowd_level']} | Spots: {spot_names} "
            f"| Tip: {c['travel_tips']}"
        )
        if c.get("nearby_attractions"):
            lines.append(f"  Attractions: {c['nearby_attractions']}")
    return "\n".join(lines)


def build_food_context() -> str:
    lines = ["=== FOOD GUIDE ==="]
    for city, info in FOOD_GUIDE.items():
        lines.append(f"• {city}: Must-try — {', '.join(info['must_try'])}. "
                     f"Best areas: {', '.join(info['areas'])}. "
                     f"Budget tip: {info['budget_tip']}")
    return "\n".join(lines)


def build_culture_context() -> str:
    lines = ["=== JAPANESE CULTURE & ETIQUETTE ==="]
    for topic, advice in CULTURE_GUIDE.items():
        lines.append(f"• {topic.replace('_', ' ').title()}: {advice}")
    return "\n".join(lines)


def build_budget_context() -> str:
    lines = ["=== BUDGET PLANNING GUIDE ==="]
    for level, info in BUDGET_GUIDE.items():
        lines.append(
            f"• {level} ({info['daily_range']}): "
            f"Stay — {info['accommodation']}. "
            f"Food — {info['food']}. "
            f"Tips: {' | '.join(info['tips'])}"
        )
    return "\n".join(lines)


def build_user_context(user_id: int) -> str:
    """Return a personalised context block for the logged-in user."""
    lines = ["=== USER PROFILE ==="]
    favs = get_user_favorites(user_id)
    if favs:
        lines.append(f"Favourite cities: {', '.join(c['name'] for c in favs)}")
    bucket = get_bucket_list(user_id)
    if bucket:
        lines.append(f"Bucket list: {', '.join(c['name'] for c in bucket)}")
    recent = get_recently_viewed(user_id, limit=5)
    if recent:
        lines.append(f"Recently viewed: {', '.join(c['name'] for c in recent)}")
    trips = get_user_itineraries(user_id)
    if trips:
        for t in trips[:3]:
            lines.append(
                f"Saved trip '{t['name']}': {t['start_date']}→{t['end_date']}, "
                f"season={t['season']}, budget=${t['budget'] or 'N/A'}, "
                f"interests={t['interests']}"
            )
    return "\n".join(lines)


def build_full_context(user_id: int | None = None) -> str:
    """
    Assemble the complete grounding context that goes into the system prompt.
    Keeps it under ~2 000 tokens to leave room for conversation history.
    """
    blocks = [
        build_cities_context(),
        build_sakura_context(),
        build_food_context(),
        build_culture_context(),
        build_budget_context(),
    ]
    if user_id:
        blocks.append(build_user_context(user_id))
    return "\n\n".join(blocks)


def get_city_info(city_name: str) -> dict | None:
    """Quick lookup — returns the first matching city dict."""
    cities = get_all_cities()
    name_lower = city_name.lower()
    for c in cities:
        if c["name"].lower() == name_lower or name_lower in c["name"].lower():
            return c
    return None


def get_food_info(city_name: str) -> dict | None:
    for key in FOOD_GUIDE:
        if key.lower() == city_name.lower():
            return FOOD_GUIDE[key]
    return None


def get_budget_info(level: str) -> dict | None:
    for key in BUDGET_GUIDE:
        if key.lower() == level.lower():
            return BUDGET_GUIDE[key]
    return None


def get_sakura_tip(city_name: str) -> str | None:
    for key, tip in SAKURA_TIPS.items():
        if key.lower() == city_name.lower():
            return tip
    return None
