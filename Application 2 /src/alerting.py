"""
Module for handling weather alerts and notifications.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from src.config import TEMP_THRESHOLD, ALERT_EMAIL, SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD

logger = logging.getLogger(__name__)

def send_email_alert(subject, body):
    """
    Send an email alert.
    
    Args:
        subject (str): Email subject.
        body (str): Email body.
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = ALERT_EMAIL
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Alert email sent: {subject}")
    except Exception as e:
        logger.error(f"Failed to send alert email: {str(e)}")

def check_alerts(daily_summary):
    """
    Check for temperature alerts based on daily summary data.
    
    Args:
        daily_summary (pd.DataFrame): Daily summary of weather data.
    """
    high_temp_cities = daily_summary[daily_summary['max_temp'] > TEMP_THRESHOLD]
    
    if not high_temp_cities.empty:
        subject = "Weather Alert: High Temperature Detected"
        body = "The following cities have exceeded the temperature threshold:\n\n"
        
        for _, row in high_temp_cities.iterrows():
            body += f"{row['city']}: {row['max_temp']}°C\n"
        
        send_email_alert(subject, body)