# ExploreJP 🗾

**ExploreJP** is a beautiful, data-driven web platform that helps people discover Japanese cities and make informed decisions about where to live, visit, or relocate.



## ✨ Features

### 🏙️ City Discovery
Browse and explore cities across Japan with rich, visual profiles featuring:
- City images and detailed information
- Regional and seasonal categorization
- Population statistics and cost of living data
- Interactive filtering and search capabilities

### 🔍 Smart Search
- Discover cities by name with instant results
- Filter by region (Kanto, Kansai, Hokkaido, etc.)
- Browse by best season to visit (Spring, Summer, Fall, Winter)
- Save your favorite cities to "My Japan" collection

### ⚖️ City Comparison
Compare cities side-by-side with:
- Population and demographic data
- Regional characteristics
- Best seasons to visit
- Cost of living metrics
- Visual comparison charts

### 📊 Data Analytics
Explore insights and trends with interactive visualizations:
- Population distribution across cities
- Cost of living analysis
- Regional statistics
- Seasonal preferences

### ❤️ Personal Collection
Build your dream Japan itinerary:
- Save favorite cities
- Create personalized travel plans
- Quick access to saved destinations
- Beautiful card-based layout

## 🎨 Design

ExploreJP features a modern, elegant design with:
- Cherry blossom-inspired color palette
- Responsive card-based layouts
- Smooth animations and transitions
- Beautiful typography with Playfair Display and Montserrat fonts
- Intuitive navigation and user experience

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
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

5. Open your browser and navigate to `http://localhost:8501`

### Console Application (Legacy)

The original console interface is still available:
```bash
python main.py
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite
- **Data Visualization**: Plotly
- **Styling**: Custom CSS with responsive design

## 📁 Project Structure

```
ExploreJP/
├── app.py                 # Streamlit web application
├── main.py               # Console application
├── init_db.py            # Database initialization
├── explorejp/
│   ├── config.py         # App configuration and styling
│   ├── database.py       # Database operations
│   ├── pages/           # Web application pages
│   │   ├── home.py
│   │   ├── explore_cities.py
│   │   └── data_visualizations.py
│   ├── screens/         # Console application screens
│   └── data/            # Data management
├── database/
│   └── explorejp.db     # SQLite database
├── data/
│   ├── cities.csv       # City data
│   ├── favorites.json   # User favorites
│   └── logo.png         # Application logo
└── tests/               # Test suite
```

## 🎯 Roadmap

### Current Features ✅
- Beautiful web interface with modern design
- City browsing and filtering
- Search functionality
- Regional and seasonal exploration
- City comparison tool
- Data visualizations
- Favorites management

### Upcoming Features 🔜
- Weather analysis and climate data
- Transportation network explorer
- Detailed cost of living breakdown
- User accounts and profiles
- AI-powered city recommendations
- Travel itinerary planner
- Community reviews and ratings

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 License

This project is open source and available under the MIT License.

## Author

**Zaineb Makhlouf** — [zainebmak](https://github.com/zainebmak)
