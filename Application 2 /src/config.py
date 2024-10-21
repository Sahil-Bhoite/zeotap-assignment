"""
Configuration module for the Weather Monitoring System.
Contains all configurable parameters and settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Cities to monitor
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

# Data retrieval interval (in seconds)
INTERVAL = 300  # 5 minutes

# Temperature threshold for alerts (in Celsius)
TEMP_THRESHOLD = 35

# Alert configuration
ALERT_EMAIL = os.getenv('ALERT_EMAIL')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')

# Database configuration
DB_PATH = 'weather_data.db'

# Logging configuration
LOG_FILE = 'weather_monitoring.log'
LOG_LEVEL = 'INFO'

# Create directories for storing data and logs if they don't exist
os.makedirs('data', exist_ok=True)
os.makedirs('logs', exist_ok=True)