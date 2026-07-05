"""City data for ExploreJP."""

from dataclasses import dataclass


@dataclass(frozen=True)
class City:
    name: str
    population: str
    region: str
    best_season: str
    known_for: list[str]


CITIES: dict[str, City] = {
    "1": City(
        name="Tokyo",
        population="13.9 Million",
        region="Kanto",
        best_season="Spring 🌸",
        known_for=["Anime", "Technology", "Nightlife", "Food"],
    ),
    "2": City(
        name="Kyoto",
        population="1.4 Million",
        region="Kansai",
        best_season="Autumn 🍁",
        known_for=["Temples", "Geisha Districts", "Traditional Culture", "Cherry Blossoms"],
    ),
    "3": City(
        name="Osaka",
        population="2.7 Million",
        region="Kansai",
        best_season="Spring 🌸",
        known_for=["Street Food", "Comedy", "Castle", "Nightlife"],
    ),
    "4": City(
        name="Hiroshima",
        population="1.2 Million",
        region="Chugoku",
        best_season="Spring 🌸",
        known_for=["Peace Memorial", "Miyajima", "Okonomiyaki", "History"],
    ),
    "5": City(
        name="Sapporo",
        population="1.9 Million",
        region="Hokkaido",
        best_season="Winter ❄️",
        known_for=["Snow Festival", "Beer", "Ramen", "Nature"],
    ),
    "6": City(
        name="Fukuoka",
        population="1.6 Million",
        region="Kyushu",
        best_season="Spring 🌸",
        known_for=["Ramen", "Yatai Stalls", "Beaches", "Gateway to Asia"],
    ),
}
