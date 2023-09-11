import yaml
import database_operations, data_analysis
from datetime import datetime
import os
import pandas as pd

# Read Configuration
with open("config.yml", 'r') as stream:
    config = yaml.safe_load(stream)

# Extract configurations
db_name = config['database']['name']


def sample_and_analyze():
    sample = database_operations.sample_data(db_name)
    if sample is not None and len(sample) > 0:
        columns = ['id', 'temperature', 'pressure', 'humidity', 'timestamp']
        df_sample = pd.DataFrame(sample, columns=columns)
        analysis_result = data_analysis.perform_eda_and_plot(df_sample)
        print("Analysis result:", analysis_result)

        # Check if the file exists, and create it if it doesn't
        if not os.path.exists("analysis_result.txt"):
            with open("analysis_result.txt", "w") as f:
                f.write("Analysis Results Log\n")
                f.write("====================\n")

        # Write analysis result to a text file
        with open("analysis_result.txt", "a") as f:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # get the current time
            f.write(f"Timestamp: {current_time}\n")  # write the timestamp to the file
            f.write("Analysis result:\n")
            f.write(str(analysis_result))
            f.write("\n---\n")
