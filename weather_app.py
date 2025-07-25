import streamlit as st
import requests
from datetime import datetime
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# === Load API Key ===
load_dotenv()
API_KEY = os.getenv("API_KEY")

# === Function to fetch weather data ===
def get_weather(city, units='metric'):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    else:
        return None
    
# === Function to fetch weather forecast ===
def get_forecast(city, units='metric'):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={units}"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    else:
        return None
    
# === Function to add dynamic icons ===
def weather_icon(desc):
    desc = desc.lower()
    if 'cloud' in desc:
        return '☁️'
    elif 'rain' in desc:
        return '🌧️'
    elif 'clear' in desc:
        return '☀️'
    elif 'snow' in desc:
        return '❄️'
    elif 'strom' in desc or 'thunder' in desc:
        return '⛈️'
    else:
        return '🌡️'

# === Function to add background color based on weather ===
def bg_color(desc):
    desc = desc.lower()
    if 'clouds' in desc:
        return '#d6e0f0'
    elif 'rain' in desc:
        return '#a9c9ff'
    elif 'clear' in desc:
        return '#ffeaa7'
    elif 'snow' in desc:
        return '#ffffff'
    else:
        return '#f1f2f6'

# === Streamlit for UI ===
st.set_page_config(page_title="Real Time Weather App", layout="wide")

st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
            padding: 1rem 2rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .stApp {
            margin-top: 0rem !important;
            padding-top: 0rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class='main-header'>
        <h1>🌦️ Real-Time Weather Forecast</h1>
        <p>Get live temperature, humidity, and a 5-day forecast by city</p>
    </div>
""", unsafe_allow_html=True) 

# Unit toggle
unit_option = st.selectbox("Select Unit", ["Celsius", "Fahrenheit"])
units = "metric" if unit_option == "Celsius" else "imperial"

# To input city names
cities = st.text_input("Enter city names (comma-seperated)", "Mumbai, Delhi")

if cities:
    city_list = [c.strip() for c in cities.split(',')]
    for city in city_list:
        st.markdown("---")
        col1, col2 = st.columns([2, 3])

        # Get weather data
        weather = get_weather(city, units)
        if weather:
            with col1:
                weather_desc = weather['weather'][0]['description']
                icon = weather_icon(weather_desc)
                bg = bg_color(weather_desc)

                st.markdown(f"""
                    <div style='background-color:{bg}; padding:20px; border-radius:10px;'>
                        <h3>{city.title()}, {weather['sys']['country']}</h3>
                        <p><strong>{icon} {weather_desc.title()}</strong></p>
                        <p>🌡️ Temperature: {weather['main']['temp']}° {unit_option}</p>
                        <p>💧 Humidity: {weather['main']['humidity']}%</p>
                        <p>🌅 Sunrise: {datetime.utcfromtimestamp(weather['sys']['sunrise']).strftime('%H:%M:%S')} UTC</p>
                        <p>🌇 Sunset: {datetime.utcfromtimestamp(weather['sys']['sunset']).strftime('%H:%M:%S')} UTC</p>
                    </div>
                """, unsafe_allow_html=True)

            # 5 days forecast
            with col2:
                forecast = get_forecast(city, units)
                if forecast:
                    st.markdown("#### 📊 5-Days Forecast")
                    dates = []
                    temps = []

                    for i in range(0, len(forecast['list']), 8):
                        dt = forecast['list'][i]['dt_txt'].split()[0]
                        temp = forecast['list'][i]['main']['temp']  
                        dates.append(dt)
                        temps.append(temp)

                    fig, ax = plt.subplots()
                    ax.plot(dates, temps, marker='o', linestyle='-', color='skyblue')
                    ax.set_title(f"{city.title()} 5-Day Forecast")
                    ax.set_ylabel(f"Temp ({'°C' if units == 'metric' else '°F'})")
                    st.pyplot(fig)
        else:
            st.error(f"City '{city}' not found. Please check spelling.")