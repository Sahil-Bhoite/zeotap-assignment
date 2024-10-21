"""
Main module for the Weather Monitoring System.
Coordinates data retrieval, processing, and visualization.
"""

import logging
from threading import Timer
from src.config import LOG_FILE, LOG_LEVEL
from src.data_retrieval import schedule_data_retrieval
from src.data_processing import process_weather_data
from src.visualization import update_visualizations

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def schedule_daily_processing():
    """
    Schedule daily processing of weather data and update visualizations.
    """
    process_weather_data()
    update_visualizations()
    Timer(86400, schedule_daily_processing).start()  # 24 hours

if __name__ == '__main__':
    try:
        logger.info("Starting Weather Monitoring System")
        
        # Start data retrieval process
        schedule_data_retrieval()
        
        # Schedule daily processing
        schedule_daily_processing()
        
        logger.info("Weather Monitoring System is running")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")