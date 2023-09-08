import logging
import yaml
from src import sensor_api, database_operations

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
logging.basicConfig(filename='logs/app.log', level=log_level_map.get(log_level, logging.DEBUG))

# Initialize Database
database_operations.create_db_and_table(db_name)

# Initialize Flask
sensor_api.app.run(host=server_host, port=server_port)
