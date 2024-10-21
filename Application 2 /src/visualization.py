"""
Module for creating visualizations of weather data.
"""

import matplotlib.pyplot as plt
from src.data_storage import get_daily_summary
import pandas as pd

def plot_daily_summary():
    """
    Create and display plots for daily weather summaries.
    """
    df = get_daily_summary()
    df['date'] = pd.to_datetime(df['date'])
    
    plt.figure(figsize=(15, 5))
    for city in df['city'].unique():
        city_data = df[df['city'] == city]
        plt.plot(city_data['date'], city_data['avg_temp'], label=city)
    
    plt.xlabel('Date')
    plt.ylabel('Average Temperature (°C)')
    plt.title('Daily Average Temperature by City')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('data/temperature_summary.png')
    plt.close()
    
    plt.figure(figsize=(15, 5))
    for city in df['city'].unique():
        city_data = df[df['city'] == city]
        plt.plot(city_data['date'], city_data['avg_humidity'], label=city)
    
    plt.xlabel('Date')
    plt.ylabel('Average Humidity (%)')
    plt.title('Daily Average Humidity by City')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('data/humidity_summary.png')
    plt.close()
    
    plt.figure(figsize=(15, 5))
    for city in df['city'].unique():
        city_data = df[df['city'] == city]
        plt.plot(city_data['date'], city_data['avg_wind_speed'], label=city)
    
    plt.xlabel('Date')
    plt.ylabel('Average Wind Speed (m/s)')
    plt.title('Daily Average Wind Speed by City')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('data/wind_speed_summary.png')
    plt.close()

def update_visualizations():
    """
    Update all visualizations with the latest data.
    """
    plot_daily_summary()