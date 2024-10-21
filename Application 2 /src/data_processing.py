"""
Module for processing weather data and generating summaries.
"""

import pandas as pd
from src.data_storage import get_weather_data, store_daily_summary
from src.alerting import check_alerts

def calculate_daily_summary():
    """
    Calculate daily summary statistics from weather data.
    
    Returns:
        pd.DataFrame: Daily summary of weather data.
    """
    df = get_weather_data()
    df['date'] = pd.to_datetime(df['dt'], unit='s').dt.date
    
    summary = df.groupby(['date', 'city']).agg(
        avg_temp=('temp', 'mean'),
        max_temp=('temp', 'max'),
        min_temp=('temp', 'min'),
        avg_humidity=('humidity', 'mean'),
        max_humidity=('humidity', 'max'),
        min_humidity=('humidity', 'min'),
        avg_wind_speed=('wind_speed', 'mean'),
        max_wind_speed=('wind_speed', 'max'),
        min_wind_speed=('wind_speed', 'min'),
        dominant_condition=('main', lambda x: x.mode()[0])
    ).reset_index()
    
    store_daily_summary(summary)
    return summary

def process_weather_data():
    """
    Process weather data, generate summaries, and check for alerts.
    """
    daily_summary = calculate_daily_summary()
    check_alerts(daily_summary)