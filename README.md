# ExploreJP 🗾

A beautiful, data-driven platform for discovering Japanese cities and planning your perfect trip.

## ✨ Features

- **👤 User Accounts** - Register, login, and manage your profile with secure authentication
- **🏙️ City Discovery** - Browse Japanese cities with images, stats, and detailed information
- **🔍 Smart Search** - Find cities by name, region, or best season to visit
- **❤️ Favorites & Bucket List** - Save cities to your personal collection and dream destinations
- **⚖️ City Comparison** - Compare cities side-by-side with visual charts
- **🧳 Trip Planning** - Build custom itineraries with maps, route optimization, and PDF export
- **🌸 Cherry Blossom Guide** - Peak bloom calendars, viewing spots, and travel tips
- **🤖 Sakura AI** - AI-powered travel consultant (Groq API or database fallback)
- **🌤️ Weather Analysis** - Climate data, temperature patterns, and best months to visit
- **⭐ Reviews & Ratings** - Share experiences and see community ratings for cities
- **📊 Data Visualizations** - Interactive charts for population, cost of living, and regional stats

## 🚀 Quick Start

```bash
# Clone and install
git clone https://github.com/zainebmak/ExploreJP.git
cd ExploreJP
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run the app
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite
- **Auth**: bcrypt
- **Visualization**: Plotly, Folium
- **AI**: Groq API

## 📁 Project Structure

```
ExploreJP/
├── app.py                    # Main Streamlit app
├── init_db.py                # Database initialization
├── explorejp/
│   ├── database.py           # Database operations
│   ├── config.py             # App configuration
│   └── pages/                # All page modules
└── data/
    └── cities.csv            # City data source
```

## � License

MIT License - see LICENSE file for details.

## � Author

**Zaineb Makhlouf** — [zainebmak](https://github.com/zainebmak)
