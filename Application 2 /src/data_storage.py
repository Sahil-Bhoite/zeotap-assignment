"""
Module for handling data storage operations using SQLite.
"""

import sqlite3
import pandas as pd
from src.config import DB_PATH

def get_db_connection():
    """
    Create a database connection.
    
    Returns:
        sqlite3.Connection: Database connection object.
    """
    return sqlite3.connect(DB_PATH)

def init_db():
    """
    Initialize the database by creating necessary tables.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        main TEXT,
        temp REAL,
        feels_like REAL,
        humidity REAL,
        wind_speed REAL,
        dt INTEGER
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_summary (
        date TEXT,
        city TEXT,
        avg_temp REAL,
        max_temp REAL,
        min_temp REAL,
        avg_humidity REAL,
        max_humidity REAL,
        min_humidity REAL,
        avg_wind_speed REAL,
        max_wind_speed REAL,
        min_wind_speed REAL,
        dominant_condition TEXT,
        PRIMARY KEY (date, city)
    )
    ''')
    
    conn.commit()
    conn.close()

def store_weather_data(data):
    """
    Store weather data in the database.
    
    Args:
        data (list): List of dictionaries containing weather data.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for item in data:
        cursor.execute('''
        INSERT INTO weather_data (city, main, temp, feels_like, humidity, wind_speed, dt)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (item['city'], item['main'], item['temp'], item['feels_like'],
              item['humidity'], item['wind_speed'], item['dt']))
    
    conn.commit()
    conn.close()

def get_weather_data():
    """
    Retrieve all weather data from the database.
    
    Returns:
        pd.DataFrame: DataFrame containing all weather data.
    """
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM weather_data", conn)
    conn.close()
    return df

def store_daily_summary(summary):
    """
    Store daily summary data in the database.
    
    Args:
        summary (pd.DataFrame): DataFrame containing daily summary data.
    """
    conn = get_db_connection()
    summary.to_sql('daily_summary', conn, if_exists='replace', index=False)
    conn.close()

def get_daily_summary():
    """
    Retrieve daily summary data from the database.
    
    Returns:
        pd.DataFrame: DataFrame containing daily summary data.
    """
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM daily_summary", conn)
    conn.close()
    return df

# Initialize the database when the module is imported
init_db()