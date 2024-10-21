"""
Integration tests for the Weather Monitoring System.
"""

import unittest
import os
import pandas as pd
from unittest.mock import patch
from src.data_retrieval import fetch_and_store_data
from src.data_processing import process_weather_data
from src.data_storage import get_db_connection, get_weather_data, get_daily_summary
from src.visualization import update_visualizations
from src.config import CITIES, DB_PATH

class WeatherSystemIntegrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Use a test database
        cls.original_db_path = DB_PATH
        cls.test_db_path = 'test_weather_data.db'
        os.environ['DB_PATH'] = cls.test_db_path

    @classmethod
    def tearDownClass(cls):
        # Remove the test database and restore the original DB_PATH
        os.remove(cls.test_db_path)
        os.environ['DB_PATH'] = cls.original_db_path

    def setUp(self):
        # Clear the database before each test
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM weather_data")
        cursor.execute("DELETE FROM daily_summary")
        conn.commit()
        conn.close()

    @patch('src.data_retrieval.fetch_weather_data')
    def test_end_to_end_process(self, mock_fetch_weather):
        # Mock weather data for each city
        mock_weather_data = {
            'Delhi': {'main': 'Clear', 'temp': 30, 'feels_like': 32, 'humidity': 60, 'wind_speed': 5, 'dt': 1625097600},
            'Mumbai': {'main': 'Rain', 'temp': 28, 'feels_like': 30, 'humidity': 80, 'wind_speed': 7, 'dt': 1625097600},
            'Chennai': {'main': 'Clouds', 'temp': 32, 'feels_like': 34, 'humidity': 70, 'wind_speed': 6, 'dt': 1625097600},
            'Bangalore': {'main': 'Clear', 'temp': 26, 'feels_like': 27, 'humidity': 55, 'wind_speed': 4, 'dt': 1625097600},
            'Kolkata': {'main': 'Haze', 'temp': 33, 'feels_like': 35, 'humidity': 75, 'wind_speed': 3, 'dt': 1625097600},
            'Hyderabad': {'main': 'Clear', 'temp': 31, 'feels_like': 33, 'humidity': 65, 'wind_speed': 5, 'dt': 1625097600}
        }

        def side_effect(city):
            data = mock_weather_data[city].copy()
            data['city'] = city
            return data

        mock_fetch_weather.side_effect = side_effect

        # Test data retrieval and storage
        fetch_and_store_data()
        
        stored_data = get_weather_data()
        self.assertEqual(len(stored_data), len(CITIES))
        self.assertTrue(all(city in stored_data['city'].values for city in CITIES))

        # Test data processing
        process_weather_data()
        
        daily_summary = get_daily_summary()
        self.assertEqual(len(daily_summary), len(CITIES))
        self.assertTrue(all(city in daily_summary['city'].values for city in CITIES))

        # Test visualization update
        update_visualizations()
        
        self.assertTrue(os.path.exists('data/temperature_summary.png'))
        self.assertTrue(os.path.exists('data/humidity_summary.png'))
        self.assertTrue(os.path.exists('data/wind_speed_summary.png'))

    @patch('src.alerting.send_email_alert')
    def test_alerting_system(self, mock_send_email):
        # Insert test data that should trigger an alert
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO weather_data (city, main, temp, feels_like, humidity, wind_speed, dt)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('TestCity', 'Clear', 36, 38, 60, 5, int(pd.Timestamp.now().timestamp())))
        conn.commit()
        conn.close()

        # Run data processing, which should trigger an alert
        process_weather_data()

        # Check if the alert was sent
        self.assertTrue(mock_send_email.called)
        call_args = mock_send_email.call_args[0]
        self.assertIn('Weather Alert', call_args[0])
        self.assertIn('TestCity', call_args[1])

if __name__ == '__main__':
    unittest.main()