import logging
import yaml
import threading
import schedule  
from scheduler import sample_and_analyze
from data_analysis_text_file_cleaner import filter_results
import sensor_api, database_operations
import time
import os

# Create the logs folder if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Read Configuration
with open("config.yml", 'r') as stream:
    config = yaml.safe_load(stream)

# Extract configurations
db_name = config['database']['name']
server_host = config['server']['host']
server_port = config['server']['port']
log_level = config['logging']['level']

# Set up logging
log_level_map = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
    }

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Initialize Logging for the main app
    logging.basicConfig(filename='logs/app.log', level=log_level_map.get(log_level, logging.DEBUG))

    # Initialize Database
    database_operations.create_db_and_table(db_name)

    # Schedule the sampling and analysis to run every 30 minutes
    schedule.every(30).minutes.do(sample_and_analyze)
    
    # Schedule the text file cleaner to run every 2 hours
    schedule.every(2).hours.do(filter_results)

    # Start the scheduler in a new thread
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # Start the Flask app and initialize the logger for Flask/Werkzeug
    handler = logging.FileHandler('logs/flask_werkzeug.log')
    handler.setLevel(log_level_map.get(log_level, logging.ERROR))  # Log errors and above to this file
    
    # Get the Flask app's logger and add the new handler to it.
    sensor_api.app.logger.addHandler(handler)
    sensor_api.app.run(host=server_host, port=server_port)
