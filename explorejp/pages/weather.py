"""Weather analysis and climate data page for ExploreJP Streamlit app."""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sqlite3
from pathlib import Path

from explorejp.config import COLORS

# Direct database access
DB_PATH = Path(__file__).parent.parent.parent / "database" / "explorejp.db"


@st.cache_data(ttl=300)
def get_all_weather_data():
    """Get all cities with weather data."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT wd.*, c.name, c.region 
        FROM weather_data wd
        JOIN cities c ON wd.city_id = c.id
        ORDER BY c.name
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@st.cache_data(ttl=300)
def get_weather_data_by_city(city_id):
    """Get weather data for a specific city."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT wd.*, c.name, c.region 
        FROM weather_data wd
        JOIN cities c ON wd.city_id = c.id
        WHERE wd.city_id = ?
    """, (city_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


@st.cache_data(ttl=300)
def get_all_cities():
    """Get all cities from the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM cities ORDER BY name")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@st.cache_data(ttl=300)
def get_weather_data_by_climate_type(climate_type):
    """Get cities by climate type."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT wd.*, c.name, c.region 
        FROM weather_data wd
        JOIN cities c ON wd.city_id = c.id
        WHERE wd.climate_type LIKE ?
        ORDER BY c.name
    """, (f"%{climate_type}%",))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@st.cache_data(ttl=300)
def get_cities_by_best_month(month):
    """Get cities that have a specific month in their best months."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT wd.*, c.name, c.region 
        FROM weather_data wd
        JOIN cities c ON wd.city_id = c.id
        WHERE wd.best_months LIKE ?
        ORDER BY c.name
    """, (f"%{month}%",))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def show():
    """Main weather analysis page."""

    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("🏠 Back to Home", key="back_home_weather", use_container_width=True):
            st.session_state.page = "🏠 Home"
            st.rerun()

    st.title("🌤️ Weather Analysis & Climate Data")
    st.markdown("Explore climate patterns and weather data across Japanese cities.")

    # Initialize session state for weather section
    if "weather_section" not in st.session_state:
        st.session_state.weather_section = "overview"

    # Section selector
    section = st.selectbox(
        "Select Analysis",
        ["Overview", "City Climate Details", "Climate Types", "Best Months to Visit"],
        key="weather_section_select",
    )

    if section == "Overview":
        render_overview()
    elif section == "City Climate Details":
        render_city_details()
    elif section == "Climate Types":
        render_climate_types()
    elif section == "Best Months to Visit":
        render_best_months()


def render_overview():
    """Render overview of weather data."""
    st.subheader("📊 Climate Overview")

    weather_data = get_all_weather_data()
    
    if not weather_data:
        st.warning("No weather data available. Please run the weather data initialization script.")
        st.info("Run: `python init_weather_data.py` to populate climate data.")
        return

    weather_df = pd.DataFrame(weather_data)
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Cities with Data", len(weather_df))
    
    with col2:
        avg_temp = weather_df["annual_avg_temp"].mean()
        st.metric("Avg Annual Temp", f"{avg_temp:.1f}°C")
    
    with col3:
        avg_precip = weather_df["annual_precipitation"].mean()
        st.metric("Avg Annual Precipitation", f"{avg_precip:.0f}mm")
    
    with col4:
        avg_humidity = weather_df["humidity_avg"].mean()
        st.metric("Avg Humidity", f"{avg_humidity:.0f}%")

    st.markdown("---")

    # Temperature comparison chart
    st.subheader("🌡️ Monthly Temperature Comparison")
    
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    month_cols = [f"{m.lower()}_avg_temp" for m in months]
    
    # Prepare data for plotting
    temp_data = []
    for _, row in weather_df.iterrows():
        for month, col in zip(months, month_cols):
            temp_data.append({
                "City": row["name"],
                "Month": month,
                "Temperature": row[col]
            })
    
    temp_df = pd.DataFrame(temp_data)
    
    fig = px.line(
        temp_df,
        x="Month",
        y="Temperature",
        color="City",
        title="Monthly Average Temperatures by City",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Month",
        yaxis_title="Temperature (°C)"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Climate type distribution
    st.subheader("🌍 Climate Type Distribution")
    
    climate_counts = weather_df["climate_type"].value_counts()
    fig = px.pie(
        values=climate_counts.values,
        names=climate_counts.index,
        title="Distribution of Climate Types",
        color_discrete_sequence=[
            COLORS["burgundy"],
            COLORS["cherry_blossom_pink"],
            COLORS["silver_lake_blue"],
            COLORS["misty_rose"],
        ]
    )
    st.plotly_chart(fig, use_container_width=True)

    # Annual precipitation comparison
    st.subheader("🌧️ Annual Precipitation by City")
    
    fig = px.bar(
        weather_df.sort_values("annual_precipitation", ascending=True),
        x="annual_precipitation",
        y="name",
        orientation="h",
        title="Annual Precipitation (mm)",
        color="annual_precipitation",
        color_continuous_scale="Blues",
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Precipitation (mm)",
        yaxis_title="City"
    )
    st.plotly_chart(fig, use_container_width=True)


def render_city_details():
    """Render detailed climate information for a specific city."""
    st.subheader("🏙️ City Climate Details")

    cities = get_all_cities()
    city_names = {city["id"]: city["name"] for city in cities}
    
    selected_city_id = st.selectbox(
        "Select City",
        options=list(city_names.keys()),
        format_func=lambda x: city_names[x],
        key="weather_city_select",
    )

    weather_data = get_weather_data_by_city(selected_city_id)
    
    if not weather_data:
        st.warning(f"No weather data available for {city_names[selected_city_id]}.")
        return

    # City overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Annual Avg Temp", f"{weather_data['annual_avg_temp']:.1f}°C")
    
    with col2:
        st.metric("Annual Precipitation", f"{weather_data['annual_precipitation']:.0f}mm")
    
    with col3:
        st.metric("Avg Humidity", f"{weather_data['humidity_avg']:.0f}%")

    st.markdown(f"**Climate Type:** {weather_data['climate_type']}")
    st.markdown(f"**Best Months to Visit:** {weather_data['best_months']}")

    st.markdown("---")

    # Monthly temperature chart
    st.subheader("🌡️ Monthly Temperature Pattern")
    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_cols = ["january_avg_temp", "february_avg_temp", "march_avg_temp",
                   "april_avg_temp", "may_avg_temp", "june_avg_temp",
                   "july_avg_temp", "august_avg_temp", "september_avg_temp",
                   "october_avg_temp", "november_avg_temp", "december_avg_temp"]
    
    temps = [weather_data[col] for col in month_cols]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months,
        y=temps,
        mode='lines+markers',
        name='Temperature',
        line=dict(color=COLORS["burgundy"], width=3),
        marker=dict(size=8)
    ))
    
    # Add seasonal annotations
    fig.add_vrect(x0="Dec", x1="Feb", fillcolor="lightblue", opacity=0.3, annotation_text="Winter")
    fig.add_vrect(x0="Mar", x1="May", fillcolor="lightgreen", opacity=0.3, annotation_text="Spring")
    fig.add_vrect(x0="Jun", x1="Aug", fillcolor="orange", opacity=0.3, annotation_text="Summer")
    fig.add_vrect(x0="Sep", x1="Nov", fillcolor="brown", opacity=0.3, annotation_text="Fall")
    
    fig.update_layout(
        title=f"Monthly Temperature - {weather_data['name']}",
        xaxis_title="Month",
        yaxis_title="Temperature (°C)",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

    # Temperature range statistics
    st.subheader("📊 Temperature Statistics")
    
    temp_min = min(temps)
    temp_max = max(temps)
    temp_range = temp_max - temp_min
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Coldest Month", f"{temp_min:.1f}°C")
    
    with col2:
        st.metric("Warmest Month", f"{temp_max:.1f}°C")
    
    with col3:
        st.metric("Temperature Range", f"{temp_range:.1f}°C")


def render_climate_types():
    """Render cities grouped by climate type."""
    st.subheader("🌍 Explore by Climate Type")

    weather_data = get_all_weather_data()
    
    if not weather_data:
        st.warning("No weather data available.")
        return

    weather_df = pd.DataFrame(weather_data)
    climate_types = sorted(weather_df["climate_type"].unique())
    
    selected_climate = st.selectbox(
        "Select Climate Type",
        options=climate_types,
        key="climate_type_select",
    )

    climate_cities = get_weather_data_by_climate_type(selected_climate)
    
    if climate_cities:
        st.markdown(f"**Cities with {selected_climate} climate:**")
        
        for city in climate_cities:
            with st.expander(f"🏙️ {city['name']} ({city['region']})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Annual Avg Temp", f"{city['annual_avg_temp']:.1f}°C")
                
                with col2:
                    st.metric("Annual Precipitation", f"{city['annual_precipitation']:.0f}mm")
                
                with col3:
                    st.metric("Avg Humidity", f"{city['humidity_avg']:.0f}%")
                
                st.markdown(f"**Best Months:** {city['best_months']}")
    else:
        st.info(f"No cities found with {selected_climate} climate.")

    # Climate comparison chart
    st.subheader("📊 Climate Type Comparison")
    
    climate_summary = weather_df.groupby("climate_type").agg({
        "annual_avg_temp": "mean",
        "annual_precipitation": "mean",
        "humidity_avg": "mean",
        "name": "count"
    }).rename(columns={"name": "city_count"}).reset_index()
    
    fig = px.scatter(
        climate_summary,
        x="annual_avg_temp",
        y="annual_precipitation",
        size="city_count",
        color="climate_type",
        title="Climate Types: Temperature vs Precipitation",
        hover_data=["humidity_avg", "city_count"],
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Annual Average Temperature (°C)",
        yaxis_title="Annual Precipitation (mm)"
    )
    st.plotly_chart(fig, use_container_width=True)


def render_best_months():
    """Render cities by best months to visit."""
    st.subheader("📅 Best Months to Visit")

    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    
    selected_month = st.selectbox(
        "Select Month",
        options=months,
        key="best_month_select",
    )

    cities = get_cities_by_best_month(selected_month)
    
    if cities:
        st.markdown(f"**Cities recommended for {selected_month}:**")
        
        # Create columns for city cards
        cols = st.columns(min(3, len(cities)))
        
        for idx, city in enumerate(cities):
            with cols[idx % 3]:
                st.markdown(f"""
                <div style="background-color: {COLORS['misty_rose']}; padding: 15px; 
                            border-radius: 10px; margin-bottom: 10px;">
                    <h4>🏙️ {city['name']}</h4>
                    <p><strong>Region:</strong> {city['region']}</p>
                    <p><strong>Climate:</strong> {city['climate_type']}</p>
                    <p><strong>Avg Temp:</strong> {city['annual_avg_temp']:.1f}°C</p>
                    <p><strong>Best Months:</strong> {city['best_months']}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info(f"No cities specifically recommended for {selected_month}.")

    st.markdown("---")

    # Monthly recommendation heatmap
    st.subheader("🗓️ Monthly Recommendations Overview")
    
    weather_data = get_all_weather_data()
    if weather_data:
        weather_df = pd.DataFrame(weather_data)
        
        # Create a matrix of recommendations
        month_matrix = []
        for _, city in weather_df.iterrows():
            row = {"City": city["name"]}
            for month in months:
                row[month] = 1 if month.lower() in city["best_months"].lower() else 0
            month_matrix.append(row)
        
        matrix_df = pd.DataFrame(month_matrix)
        
        fig = px.imshow(
            matrix_df.set_index("City"),
            title="Best Months to Visit by City",
            color_continuous_scale="Reds",
            labels=dict(x="Month", y="City", color="Recommended")
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Month",
            yaxis_title="City"
        )
        st.plotly_chart(fig, use_container_width=True)
