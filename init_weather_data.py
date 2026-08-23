"""Initialize weather data for Japanese cities."""

from explorejp.database import add_weather_data, get_all_cities


def seed_weather_data():
    """Seed weather data for Japanese cities."""
    
    # Get all cities from database
    cities = get_all_cities()
    
    # Weather data for each city (city_id matches the cities table)
    weather_data = [
        # Tokyo (id=1) - Humid subtropical climate
        {
            "city_id": 1,
            "january_avg_temp": 5.4,
            "february_avg_temp": 6.1,
            "march_avg_temp": 9.4,
            "april_avg_temp": 14.6,
            "may_avg_temp": 18.9,
            "june_avg_temp": 21.9,
            "july_avg_temp": 25.4,
            "august_avg_temp": 27.0,
            "september_avg_temp": 23.7,
            "october_avg_temp": 18.3,
            "november_avg_temp": 12.7,
            "december_avg_temp": 7.9,
            "annual_avg_temp": 15.9,
            "annual_precipitation": 1528,
            "humidity_avg": 60,
            "climate_type": "Humid Subtropical",
            "best_months": "March, April, May, October, November"
        },
        # Kyoto (id=2) - Humid subtropical climate
        {
            "city_id": 2,
            "january_avg_temp": 4.4,
            "february_avg_temp": 5.0,
            "march_avg_temp": 8.4,
            "april_avg_temp": 14.1,
            "may_avg_temp": 18.9,
            "june_avg_temp": 22.5,
            "july_avg_temp": 26.4,
            "august_avg_temp": 27.8,
            "september_avg_temp": 23.9,
            "october_avg_temp": 17.8,
            "november_avg_temp": 12.1,
            "december_avg_temp": 7.0,
            "annual_avg_temp": 15.4,
            "annual_precipitation": 1541,
            "humidity_avg": 65,
            "climate_type": "Humid Subtropical",
            "best_months": "March, April, May, October, November"
        },
        # Osaka (id=3) - Humid subtropical climate
        {
            "city_id": 3,
            "january_avg_temp": 5.6,
            "february_avg_temp": 6.2,
            "march_avg_temp": 9.6,
            "april_avg_temp": 15.0,
            "may_avg_temp": 19.6,
            "june_avg_temp": 23.3,
            "july_avg_temp": 27.4,
            "august_avg_temp": 28.9,
            "september_avg_temp": 25.0,
            "october_avg_temp": 19.1,
            "november_avg_temp": 13.4,
            "december_avg_temp": 8.2,
            "annual_avg_temp": 16.5,
            "annual_precipitation": 1278,
            "humidity_avg": 62,
            "climate_type": "Humid Subtropical",
            "best_months": "March, April, May, October, November"
        },
        # Hiroshima (id=4) - Humid subtropical climate
        {
            "city_id": 4,
            "january_avg_temp": 4.8,
            "february_avg_temp": 5.4,
            "march_avg_temp": 8.9,
            "april_avg_temp": 14.4,
            "may_avg_temp": 19.1,
            "june_avg_temp": 22.8,
            "july_avg_temp": 26.7,
            "august_avg_temp": 28.1,
            "september_avg_temp": 24.4,
            "october_avg_temp": 18.4,
            "november_avg_temp": 12.8,
            "december_avg_temp": 7.4,
            "annual_avg_temp": 15.9,
            "annual_precipitation": 1539,
            "humidity_avg": 68,
            "climate_type": "Humid Subtropical",
            "best_months": "April, May, October, November"
        },
        # Sapporo (id=5) - Humid continental climate
        {
            "city_id": 5,
            "january_avg_temp": -4.6,
            "february_avg_temp": -4.3,
            "march_avg_temp": 0.1,
            "april_avg_temp": 6.6,
            "may_avg_temp": 12.3,
            "june_avg_temp": 16.6,
            "july_avg_temp": 20.5,
            "august_avg_temp": 21.8,
            "september_avg_temp": 17.3,
            "october_avg_temp": 11.2,
            "november_avg_temp": 4.6,
            "december_avg_temp": -1.9,
            "annual_avg_temp": 8.5,
            "annual_precipitation": 1108,
            "humidity_avg": 72,
            "climate_type": "Humid Continental",
            "best_months": "July, August, September"
        },
        # Fukuoka (id=6) - Humid subtropical climate
        {
            "city_id": 6,
            "january_avg_temp": 6.5,
            "february_avg_temp": 7.2,
            "march_avg_temp": 10.4,
            "april_avg_temp": 15.4,
            "may_avg_temp": 19.7,
            "june_avg_temp": 23.3,
            "july_avg_temp": 27.2,
            "august_avg_temp": 28.0,
            "september_avg_temp": 24.7,
            "october_avg_temp": 19.3,
            "november_avg_temp": 13.9,
            "december_avg_temp": 9.0,
            "annual_avg_temp": 16.8,
            "annual_precipitation": 1684,
            "humidity_avg": 70,
            "climate_type": "Humid Subtropical",
            "best_months": "March, April, May, October, November"
        },
        # Nara (id=7) - Humid subtropical climate
        {
            "city_id": 7,
            "january_avg_temp": 3.9,
            "february_avg_temp": 4.5,
            "march_avg_temp": 8.0,
            "april_avg_temp": 13.7,
            "may_avg_temp": 18.5,
            "june_avg_temp": 22.2,
            "july_avg_temp": 26.1,
            "august_avg_temp": 27.5,
            "september_avg_temp": 23.6,
            "october_avg_temp": 17.5,
            "november_avg_temp": 11.7,
            "december_avg_temp": 6.5,
            "annual_avg_temp": 15.0,
            "annual_precipitation": 1386,
            "humidity_avg": 66,
            "climate_type": "Humid Subtropical",
            "best_months": "March, April, May, October, November"
        },
        # Sendai (id=8) - Humid subtropical climate
        {
            "city_id": 8,
            "january_avg_temp": 0.5,
            "february_avg_temp": 1.1,
            "march_avg_temp": 4.6,
            "april_avg_temp": 10.3,
            "may_avg_temp": 15.5,
            "june_avg_temp": 19.2,
            "july_avg_temp": 23.1,
            "august_avg_temp": 24.8,
            "september_avg_temp": 20.6,
            "october_avg_temp": 14.6,
            "november_avg_temp": 8.9,
            "december_avg_temp": 3.5,
            "annual_avg_temp": 12.1,
            "annual_precipitation": 1241,
            "humidity_avg": 68,
            "climate_type": "Humid Subtropical",
            "best_months": "April, May, October, November"
        },
    ]

    # Insert weather data
    for data in weather_data:
        city_id = data.pop("city_id")
        add_weather_data(city_id, **data)
        print(f"Added weather data for city ID {city_id}")

    print("\nWeather data seeding complete!")


if __name__ == "__main__":
    seed_weather_data()
