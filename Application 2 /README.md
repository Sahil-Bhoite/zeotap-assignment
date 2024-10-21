# Weather Monitoring System

## Overview
This project is an advanced real-time weather monitoring system that retrieves, processes, and analyzes weather data from the OpenWeatherMap API for major cities in India. It generates daily summaries, provides alerts based on user-defined thresholds, and offers data visualization capabilities.

## Features
- Real-time weather data retrieval from OpenWeatherMap API
- Automatic temperature conversion from Kelvin to Celsius
- Daily weather summaries including:
  - Average, maximum, and minimum temperatures
  - Humidity levels
  - Wind speed
  - Dominant weather condition
- User-configurable alerting system for temperature thresholds
- Data visualization of daily summaries
- Robust error handling and logging
- Comprehensive unit and integration testing

## Project Structure
```
weather_monitoring/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_retrieval.py
│   ├── data_processing.py
│   ├── data_storage.py
│   ├── alerting.py
│   ├── visualization.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── test_unit.py
│   └── test_integration.py
├── data/
├── logs/
├── .env
├── requirements.txt
├── Dockerfile
└── README.md
```

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- OpenWeatherMap API key

### Build and Install
1. Clone the repository:
   ```
   cd weather-monitoring-system

   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your OpenWeatherMap API key:
   ```
   OPENWEATHERMAP_API_KEY=your_api_key_here
   ```

5. Configure the system by updating `src/config.py` with your preferred settings.

## Usage

### Running the Application
To start the Weather Monitoring System:
```
python src/main.py
```
This will initiate the data retrieval process and start generating daily summaries and alerts.

### Visualizing the Data
To generate and display visualizations of the daily weather summary:
```
python src/visualization.py
```
This will create plots in the `data/` directory, showing temperature, humidity, and wind speed trends for each city.

## Testing
To run the unit tests:
```
python -m unittest tests/test_unit.py
```

To run the integration tests:
```
python -m unittest tests/test_integration.py
```

To run all tests:
```
python -m unittest discover tests
```

## Docker Support
A Dockerfile is provided for containerization. To build and run the Docker image:
```
docker build -t weather-monitoring-system .
docker run -d --name weather-monitor weather-monitoring-system
```

## Contact
For more information about the developer, please visit my LinkedIn profile:
[Sahil Bhoite](https://www.linkedin.com/in/sahil-bhoite/)

