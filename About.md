
# 🌦️ Real-Time Weather Forecast App

## 📌 Objective
A real-time weather app that allows users to check the current weather and a 5-day forecast for any city, using the OpenWeatherMap API.

## 🚀 Features
- 🌡️ Shows live temperature, humidity, weather description, sunrise & sunset.
- 📊 Displays a 5-day forecast chart using matplotlib.
- 🧠 Dynamic weather icons based on conditions (e.g., ☀️, 🌧️, ☁️).
- 🌍 Supports multiple cities input at once.
- 🔁 Toggle between Celsius and Fahrenheit units.
- ✨ Beautiful UI using Streamlit with custom CSS.

## 🛠️ Tools & Technologies Used
- Python 🐍
- Streamlit 🌐
- OpenWeatherMap API 🌦️
- Requests library 🔗
- Matplotlib 📊
- dotenv & os for API key handling 🔐

## 📄 How to Run

1. **Install dependencies**  
   ```bash
   pip install streamlit requests matplotlib python-dotenv
   ```

2. **Set your OpenWeatherMap API Key**  
   Create a `.env` file in the root directory:
   ```env
   API_KEY=your_openweathermap_api_key_here
   ```

3. **Run the app**
   ```bash
   streamlit run weather_app.py
   ```

4. **Enter city names** (comma-separated) in the input field and select the unit (Celsius or Fahrenheit).

---

## 🧪 Sample Cities to Try
- Mumbai, Delhi
- New York, London
- Tokyo, Paris, Turkey

## 📤 Output
- Current weather with temperature, humidity, and sunrise/sunset time.
- 5-day temperature forecast line chart.

## 📁 Project Structure
```
weather_app/
├── weather_app.py
├── .env
└── README.md
```

---

## 📬 API Source
[OpenWeatherMap](https://openweathermap.org/api)
