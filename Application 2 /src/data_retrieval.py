"""
Module for retrieving weather data from the OpenWeatherMap API.
"""

import requests
import logging
from datetime import datetime
from threading import Timer
from src.config import API_KEY, BASE_URL, CITIES, INTERVAL
from src.data_storage import store_weather_data

logger = logging.getLogger(__name__)

def fetch_weather_data(city):
    """
    Fetch weather data for a given city from the OpenWeatherMap API.
    
    Args:
        city (str): Name of the city to fetch weather data for.
    
    Returns:
        dict: Weather information for the city.
    """
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # Use metric units to get temperature in Celsius
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        weather_info = {
            'city': city,
            'main': data['weather'][0]['main'],
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'dt': data['dt']
        }
        return weather_info
    except requests.RequestException as e:
        logger.error(f"Error fetching weather data for {city}: {str(e)}")
        return None

def fetch_and_store_data():
    """
    Fetch weather data for all cities and store it in the database.
    """
    all_weather_data = []
    for city in CITIES:
        data = fetch_weather_data(city)
        if data:
            all_weather_data.append(data)
    
    if all_weather_data:
        store_weather_data(all_weather_data)
        logger.info(f"Data fetched and stored for {len(all_weather_data)} cities at {datetime.now()}")
    else:
        logger.warning("No weather data fetched.")

def schedule_data_retrieval():
    """
    Schedule periodic data retrieval.
    """
    fetch_and_store_data()
    Timer(INTERVAL, schedule_data_retrieval).start()