import schedule
import yaml
import database_operations, data_analysis

# Read Configuration
with open("config.yml", 'r') as stream:
    config = yaml.safe_load(stream)

# Extract configurations
db_name = config['database']['name']

def sample_and_analyze():
    sample = database_operations.sample_data(db_name, 50)
    if sample is not None:
        analysis_result = data_analysis.perform_eda_and_plot(sample)
        print("Analysis result:", analysis_result)  # or log it


# Initialize Scheduler
schedule.every(1).hours.do(sample_and_analyze)
