"""
Unit tests for individual components of the Weather Monitoring System.
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime, date
from src.data_retrieval import fetch_weather_data
from src.data_processing import calculate_daily_summary
from src.data_storage import store_weather_data, get_weather_data, store_daily_summary, get_daily_summary
from src.alerting import check_alerts, send_email_alert
from src.config import TEMP_THRESHOLD

class WeatherSystemUnitTest(unittest.TestCase):

    @patch('src.data_retrieval.requests.get')
    def test_fetch_weather_data(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'weather': [{'main': 'Clear'}],
            'main': {'temp': 25.5, 'feels_like': 26.0, 'humidity': 60},
            'wind': {'speed': 5.2},
            'dt': 1625097600
        }
        mock_get.return_value = mock_response

        city = 'Delhi'
        data = fetch_weather_data(city)

        self.assertIsNotNone(data)
        self.assertEqual(data['city'], city)
        self.assertEqual(data['main'], 'Clear')
        self.assertEqual(data['temp'], 25.5)
        self.assertEqual(data['feels_like'], 26.0)
        self.assertEqual(data['humidity'], 60)
        self.assertEqual(data['wind_speed'], 5.2)
        self.assertEqual(data['dt'], 1625097600)

    @patch('src.data_storage.get_weather_data')
    @patch('src.data_storage.store_daily_summary')
    def test_calculate_daily_summary(self, mock_store_summary, mock_get_data):
        # Mock weather data
        mock_data = pd.DataFrame({
            'city': ['Delhi', 'Delhi', 'Mumbai', 'Mumbai'],
            'main': ['Clear', 'Rain', 'Clear', 'Clear'],
            'temp': [30, 28, 32, 33],
            'humidity': [60, 70, 65, 63],
            'wind_speed': [5, 6, 4, 4.5],
            'dt': [1625097600, 1625184000, 1625097600, 1625184000]
        })
        mock_get_data.return_value = mock_data

        summary = calculate_daily_summary()

        self.assertIsInstance(summary, pd.DataFrame)
        self.assertEqual(len(summary), 4)  # 2 days * 2 cities
        self.assertTrue(mock_store_summary.called)

    @patch('src.data_storage.get_db_connection')
    def test_data_storage(self, mock_conn):
        # Test storing and retrieving weather data
        test_data = [
            {'city': 'TestCity', 'main': 'Clear', 'temp': 25.5, 'feels_like': 26.0,
             'humidity': 60, 'wind_speed': 5.2, 'dt': int(datetime.now().timestamp())}
        ]
        store_weather_data(test_data)
        
        # Mock the database query result
        mock_conn.return_value.cursor().fetchall.return_value = [
            (1, 'TestCity', 'Clear', 25.5, 26.0, 60, 5.2, test_data[0]['dt'])
        ]
        
        retrieved_data = get_weather_data()
        self.assertIsInstance(retrieved_data, pd.DataFrame)
        self.assertEqual(len(retrieved_data), 1)
        self.assertEqual(retrieved_data.iloc[0]['city'], 'TestCity')

    @patch('src.alerting.send_email_alert')
    def test_check_alerts(self, mock_send_email):
        test_summary = pd.DataFrame({
            'date': [date.today(), date.today()],
            'city': ['HotCity', 'CoolCity'],
            'max_temp': [TEMP_THRESHOLD + 1, TEMP_THRESHOLD - 1]
        })

        check_alerts(test_summary)

        self.assertTrue(mock_send_email.called)
        call_args = mock_send_email.call_args[0]
        self.assertIn('Weather Alert', call_args[0])
        self.assertIn('HotCity', call_args[1])
        self.assertNotIn('CoolCity', call_args[1])

if __name__ == '__main__':
    unittest.main()