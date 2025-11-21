# Weather Application - Module 6 Lab

## Student Information
- **Name**: Rona Mae M. Quite
- **Student ID**: 231002336
- **Course**: CCCS 106 - Application Development and Emerging Technologies
- **Section**: BSCS 3A

## Project Overview
A modern weather application written in Python and Flet framework and gives real-time weather forecasts and information. The application has a smooth dark theme design, which enables the user to search in any city of the world and get the real time weather, hourly prognosis, and 7 days weather forecast.

## Features Implemented

### Base Features
- City search functionality with real-time results
- Current weather display (temperature, description, weather icon)
- Detailed weather metrics (humidity, wind speed, feels like, chance of rain)
- Dynamic weather icons from OpenWeatherMap
- Comprehensive error handling for network and API errors
- Modern dark theme UI
- Async operations using `page.run_task()`

### Enhanced Features

1. **Search History**
   - Automatically saves the last 5 searched cities
   - Displays in dropdown for quick access
   - Persistent storage using JSON files
   - Click any city to instantly load weather

2. **7-Day Weather Forecast**
   - Comprehensive weekly forecast in side panel
   - Shows daily high/low temperatures
   - Weather conditions and icons for each day
   - Parsed from OpenWeatherMap forecast API

### Additional Features
- Today's Hourly Forecast (6-hour preview)
- Air Conditions Panel (Real Feel, Wind, Humidity, UV Index)
- Premium Dark Theme Design

## Screenshots

### 🟦 Initial Screen (before searching)
![Initial Screen](screenshots/initial_screen.png)

---

### Weather Results – Manila
![Weather Results](screenshots/weather_results.png)

---

### Weather Details (Forecast + Air Conditions)
![Weather Details](screenshots/weather_details.png)

---

## Other Countries 

### 🇯🇵 Tokyo Weather
![Tokyo Weather](screenshots/tokyo_weather.png)

### 🇯🇵 Tokyo Weather Details (Forecast + Air Conditions)
![Tokyo Weather Details](screenshots/tokyo_weather_details.png)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- OpenWeatherMap API key (free)

### Setup Instructions

```bash
# Clone the repository
git clone https://github.com/chan-del/cccs106-projects.git
cd cccs106-projects/mod6_labs

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file and add your API key
cp .env.example .env

# Run the application
python main.py
```
