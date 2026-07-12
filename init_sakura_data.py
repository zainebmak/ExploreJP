"""Initialize cherry blossom data in the database."""

from explorejp.database import (
    add_cherry_blossom_city,
    add_sakura_spot,
    add_sakura_forecast,
    get_all_cities,
)


def init_sakura_data():
    """Populate the database with cherry blossom data."""
    
    # Get all cities to find IDs
    cities = get_all_cities()
    city_map = {city['name']: city['id'] for city in cities}
    
    # Cherry blossom data for major cities
    sakura_cities = [
        {
            'name': 'Tokyo',
            'peak_bloom_start': '2024-03-27',
            'peak_bloom_end': '2024-04-05',
            'latitude': 35.6762,
            'longitude': 139.6503,
            'crowd_level': 'Very High',
            'travel_tips': 'Visit early morning (6-8 AM) to avoid crowds. Meguro River and Shinjuku Gyoen are popular spots.'
        },
        {
            'name': 'Kyoto',
            'peak_bloom_start': '2024-03-30',
            'peak_bloom_end': '2024-04-08',
            'latitude': 35.0116,
            'longitude': 135.7681,
            'crowd_level': 'Very High',
            'travel_tips': 'Philosopher\'s Path and Maruyama Park are must-visit. Consider visiting lesser-known temples for fewer crowds.'
        },
        {
            'name': 'Osaka',
            'peak_bloom_start': '2024-03-28',
            'peak_bloom_end': '2024-04-06',
            'latitude': 34.6937,
            'longitude': 135.5023,
            'crowd_level': 'High',
            'travel_tips': 'Osaka Castle grounds offer beautiful views. Kema Sakuranomiya Park along the river is excellent for hanami.'
        },
        {
            'name': 'Nara',
            'peak_bloom_start': '2024-03-29',
            'peak_bloom_end': '2024-04-07',
            'latitude': 34.6851,
            'longitude': 135.8048,
            'crowd_level': 'Medium',
            'travel_tips': 'Nara Park with deer and cherry blossoms is magical. Isuien Garden offers a peaceful viewing experience.'
        },
        {
            'name': 'Hirosaki',
            'peak_bloom_start': '2024-04-20',
            'peak_bloom_end': '2024-05-05',
            'latitude': 40.8225,
            'longitude': 140.4550,
            'crowd_level': 'Medium',
            'travel_tips': 'Famous for late-blooming varieties. Hirosaki Castle is one of Japan\'s top sakura destinations.'
        },
    ]
    
    # Add cherry blossom city data
    for city_data in sakura_cities:
        city_name = city_data['name']
        if city_name in city_map:
            city_id = city_map[city_name]
            add_cherry_blossom_city(
                city_id=city_id,
                peak_bloom_start=city_data['peak_bloom_start'],
                peak_bloom_end=city_data['peak_bloom_end'],
                latitude=city_data['latitude'],
                longitude=city_data['longitude'],
                crowd_level=city_data['crowd_level'],
                travel_tips=city_data['travel_tips']
            )
            print(f"Added cherry blossom data for {city_name}")
    
    # Sakura viewing spots
    sakura_spots = [
        # Tokyo spots
        {
            'city': 'Tokyo',
            'name': 'Shinjuku Gyoen',
            'description': 'One of Tokyo\'s largest parks with over 1,000 cherry trees. Perfect for picnics.',
            'image_url': 'https://i.pinimg.com/1200x/7b/0a/3b/7b0a3bdce4604379fa847476756b2050.jpg'
        },
        {
            'city': 'Tokyo',
            'name': 'Meguro River',
            'description': 'Famous for its 4km cherry tree-lined river. Beautiful at night with illuminations.',
            'image_url': 'https://i.pinimg.com/1200x/c6/70/d9/c670d985b022020c837b5186259f3aa7.jpg'
        },
        {
            'city': 'Tokyo',
            'name': 'Ueno Park',
            'description': 'Historic park with over 1,000 cherry trees. Popular for hanami parties.',
            'image_url': 'https://i.pinimg.com/736x/02/f6/24/02f6246888da9cfda7024d52b62f7463.jpg'
        },
        # Kyoto spots
        {
            'city': 'Kyoto',
            'name': 'Philosopher\'s Path',
            'description': 'Scenic canal path lined with hundreds of cherry trees. Perfect for peaceful walks.',
            'image_url': 'https://i.pinimg.com/1200x/3d/c5/e9/3dc5e90782bcb686b53b20290b9258f9.jpg'
        },
        {
            'city': 'Kyoto',
            'name': 'Maruyama Park',
            'description': 'Famous for its huge weeping cherry tree. Great for evening hanami.',
            'image_url': 'https://i.pinimg.com/1200x/e9/d6/38/e9d6381765807102cb75b3a52a15d9fe.jpg'
        },
        {
            'city': 'Kyoto',
            'name': 'Arashiyama',
            'description': 'Bamboo grove meets cherry blossoms. Stunning combination of nature.',
            'image_url': 'https://i.pinimg.com/1200x/6b/35/f7/6b35f7ad90a61fa78141dbfef75d03ea.jpg'
        },
        # Osaka spots
        {
            'city': 'Osaka',
            'name': 'Osaka Castle',
            'description': 'Historic castle surrounded by 3,000 cherry trees. Iconic view.',
            'image_url': 'https://i.pinimg.com/1200x/c4/d3/4e/c4d34e7da3d9d560186ce665a15e3de4.jpg'
        },
        {
            'city': 'Osaka',
            'name': 'Kema Sakuranomiya Park',
            'description': '4.2km riverside park with 4,800 cherry trees. Great for cycling.',
            'image_url': 'https://i.pinimg.com/1200x/ab/63/76/ab6376e22553ef8d84cda90fd56eea0b.jpg'
        },
        # Nara spots
        {
            'city': 'Nara',
            'name': 'Nara Park',
            'description': 'Famous deer park with cherry blossoms. Unique wildlife viewing experience.',
            'image_url': 'https://i.pinimg.com/736x/e2/9e/2d/e29e2dfc8e4151fe394d1ba75b1816bf.jpg'
        },
        {
            'city': 'Nara',
            'name': 'Isuien Garden',
            'description': 'Traditional Japanese garden with carefully curated cherry trees.',
            'image_url': 'https://i.pinimg.com/1200x/c8/49/f1/c849f1a39c73a15a906107bd0c67b28c.jpg'
        },
        # Hirosaki spots
        {
            'city': 'Hirosaki',
            'name': 'Hirosaki Castle',
            'description': 'One of Japan\'s best cherry blossom spots with 2,600 trees. Famous for petal moats.',
            'image_url': 'https://i.pinimg.com/1200x/93/70/4c/93704c6171b38186e5466718f64d3c2d.jpg'
        },
    ]
    
    # Add sakura spots
    for spot_data in sakura_spots:
        city_name = spot_data['city']
        if city_name in city_map:
            city_id = city_map[city_name]
            add_sakura_spot(
                city_id=city_id,
                name=spot_data['name'],
                description=spot_data['description'],
                image_url=spot_data['image_url']
            )
            print(f"Added sakura spot: {spot_data['name']} in {city_name}")
    
    # Sample bloom forecasts for April 2024
    forecasts = [
        ('Tokyo', '2024-04-01', 95),
        ('Tokyo', '2024-04-05', 85),
        ('Tokyo', '2024-04-10', 60),
        ('Kyoto', '2024-04-02', 95),
        ('Kyoto', '2024-04-05', 90),
        ('Kyoto', '2024-04-10', 70),
        ('Osaka', '2024-04-01', 90),
        ('Osaka', '2024-04-05', 85),
        ('Osaka', '2024-04-10', 65),
        ('Nara', '2024-04-02', 92),
        ('Nara', '2024-04-05', 88),
        ('Nara', '2024-04-10', 68),
        ('Hirosaki', '2024-04-01', 10),
        ('Hirosaki', '2024-04-10', 30),
        ('Hirosaki', '2024-04-25', 95),
    ]
    
    # Add forecasts
    for city_name, date, percentage in forecasts:
        if city_name in city_map:
            city_id = city_map[city_name]
            add_sakura_forecast(
                city_id=city_id,
                forecast_date=date,
                bloom_percentage=percentage
            )
            print(f"Added forecast for {city_name} on {date}: {percentage}%")


if __name__ == "__main__":
    print("Initializing cherry blossom data...")
    init_sakura_data()
    print("Cherry blossom data initialization complete!")
