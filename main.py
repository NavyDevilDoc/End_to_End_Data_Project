import logging
import yaml
import threading
import schedule  
from scheduler import sample_and_analyze
from src import sensor_api, database_operations
import time  

# Read Configuration
with open("config.yaml", 'r') as stream:
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
    # Initialize Logging
    logging.basicConfig(filename='logs/app.log', level=log_level_map.get(log_level, logging.DEBUG))

    # Initialize Database
    database_operations.create_db_and_table(db_name)

    # Schedule the sampling and analysis to run every hour
    schedule.every(1).hours.do(sample_and_analyze)

    # Start the scheduler in a new thread
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # Start the Flask app
    sensor_api.app.run(host=server_host, port=server_port)
