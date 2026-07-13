# ExploreJP 🗾

**ExploreJP** is a beautiful, data-driven web platform that helps people discover Japanese cities and make informed decisions about where to visit, explore, or plan a trip.

## ✨ Features

### 👤 User Accounts
Full authentication system with per-user data:
- Register and log in with username, email, and password (bcrypt-hashed)
- Persistent session with account state across all pages
- Login / Register page with tabbed interface

### 📊 Personal Dashboard
A dedicated dashboard for logged-in users showing:
- Stats overview: favorites, saved trips, bucket list, recently viewed counts
- Favorite cities with quick-remove actions
- Recently viewed cities (auto-tracked when browsing)
- Saved trips with direct navigation to the trip builder
- Bucket list cities with remove actions

### ⚙️ Account Settings
Full account management in one place:
- Change username and email
- Set travel preferences (favorite season, preferred budget)
- Change password with current-password verification
- Delete account with username + password confirmation (cascades all user data)

### 🏙️ City Discovery
Browse and explore cities across Japan with rich, visual profiles:
- City images and detailed information
- Regional and seasonal categorization
- Population statistics and cost of living data
- Interactive filtering and search

### 🔍 Smart Search
- Discover cities by name with instant results
- Filter by region (Kanto, Kansai, Hokkaido, etc.)
- Browse by best season to visit (Spring, Summer, Fall, Winter)
- Save favorite cities (per-user when logged in, anonymous otherwise)

### ❤️ Favorites, Bucket List & History
- Save favorite cities to "My Japan" collection (synced to your account)
- Add cities to a personal bucket list
- Recently viewed history — automatically recorded per user, capped at 20

### ⚖️ City Comparison
Compare cities side-by-side:
- Population and demographic data
- Regional characteristics and best seasons
- Cost of living metrics
- Visual comparison charts

### 📊 Data Analytics
Interactive visualizations:
- Population distribution across cities
- Cost of living analysis
- Regional statistics
- Seasonal preferences

### 🧳 Trip Planning
Plan your perfect Japan trip:
- Create custom itineraries (dates, season, budget, interests)
- Trips are saved to your account when logged in
- City recommendations based on season and interests
- Interactive map with route visualization
- Route optimization using nearest neighbor algorithm
- PDF export with full itinerary and packing list
- Smart packing suggestions based on season and interests
- Daily budget breakdown

### � Cherry Blossom Guide
- Peak bloom calendar per city
- Best viewing spots with photos
- Crowd level indicators and travel tips
- Nearby attractions for each sakura destination

### 🤖 Sakura AI — Japan Travel Consultant
An AI-powered chat assistant built into the app:
- Conversational travel advice powered by Groq (LLM mode)
- Falls back to ExploreJP's own database when no API key is set
- Quick-action suggestion chips for common travel questions
- Personalized responses for logged-in users
- Set your Groq API key in `.env` to enable full AI mode (free at [console.groq.com](https://console.groq.com))

### 🌤️ Weather Analysis & Climate Data
- Comprehensive climate data for Japanese cities
- Monthly temperature patterns and visualizations
- Climate type classification and comparison
- Best months to visit recommendations
- Annual precipitation and humidity analysis
- Interactive Plotly charts and heatmaps

## 🎨 Design

- Cherry blossom-inspired color palette
- Responsive card-based layouts
- Smooth animations and transitions
- Playfair Display and Montserrat fonts
- Auth-aware navbar on every page
- "Back to Home" button on every feature page for easy navigation

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip package manager

### Installation

1. Clone the repository
```bash
git clone https://github.com/zainebmak/ExploreJP.git
cd ExploreJP
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Initialize the database
```bash
python init_db.py
```

4. Run the web application
```bash
streamlit run app.py
```

5. Open your browser at `http://localhost:8501`

### Console Application (Legacy)

The original console interface is still available:
```bash
python main.py
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite (via `explorejp.db`)
- **Auth**: bcrypt password hashing
- **Data Visualization**: Plotly
- **Maps**: Folium + streamlit-folium
- **PDF Export**: fpdf2
- **AI**: Groq API (LLM mode) / ExploreJP database (fallback mode)

## 📁 Project Structure

```
ExploreJP/
├── app.py                    # Main Streamlit app + routing
├── main.py                   # Console application (legacy)
├── init_db.py                # Database initialization script
├── init_sakura_data.py       # Cherry blossom data seeding
├── explorejp/
│   ├── config.py             # App config and global CSS
│   ├── database.py           # All database operations
│   ├── pages/
│   │   ├── auth.py           # Login & registration page
│   │   ├── dashboard.py      # Personal user dashboard
│   │   ├── settings.py       # Account settings page
│   │   ├── home.py           # Home / landing page
│   │   ├── explore_cities.py # City browsing & search
│   │   ├── plan_trip.py      # Trip planning & itinerary builder
│   │   ├── cherry_blossom.py # Sakura guide
│   │   ├── sakura_ai.py      # AI travel consultant (Groq)
│   │   ├── weather.py        # Weather analysis & climate data
│   │   └── data_visualizations.py
│   ├── screens/              # Console application screens
│   └── data/                 # Data helpers
├── database/
│   └── explorejp.db          # SQLite database
├── data/
│   ├── cities.csv            # City source data
│   ├── favorites.json        # Anonymous favorites (legacy)
│   └── logo.png
└── tests/
```

## 🗄️ Database Schema (User Tables)

| Table | Purpose |
|---|---|
| `users` | Accounts: username, email, bcrypt hash, preferences |
| `user_favorites` | Per-user saved cities |
| `recently_viewed` | Auto-tracked city views per user (max 20) |
| `bucket_list` | Dream destinations per user |
| `itineraries` | Trip plans linked to a user |

## 🎯 Roadmap

### Implemented ✅
- Full user authentication (register, login, logout)
- Personal dashboard with favorites, trips, bucket list, history
- Account settings: profile, preferences, password, delete account
- Per-user favorites, bucket list, recently viewed tracking
- City browsing, search, filtering, comparison
- Data visualizations
- Trip planning with itinerary builder, map, route optimization, PDF export
- Cherry Blossom Guide with bloom calendar and viewing spots
- Weather Analysis and Climate Data with monthly patterns and recommendations
- Sakura AI chat assistant powered by Groq (with database fallback mode)
- "Back to Home" navigation button on every feature page

### Upcoming 🔜
- Community reviews and ratings

## 🤝 Contributing

Contributions are welcome! Feel free to report bugs, suggest features, or submit pull requests.

## 📝 License

This project is open source and available under the MIT License.

## Author

**Zaineb Makhlouf** — [zainebmak](https://github.com/zainebmak)
