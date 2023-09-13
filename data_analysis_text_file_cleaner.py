import os
from datetime import datetime

def filter_results():
    try:
        # Initialize variables
        prev_timestamp = None
        write_block = True
        last_line_was_delim = False

        # Define output filename
        output_filename = "updated_analysis_result.txt"

        # Check if the output file already exists
        if not os.path.exists(output_filename):
            open(output_filename, "w").close()

        # Check if the input file exists
        if not os.path.exists("analysis_result.txt"):
            raise FileNotFoundError("Input file 'analysis_result.txt' not found.")

        # Open the input and output files
        with open("analysis_result.txt", "r") as infile, open(output_filename, "w") as outfile:
            for line in infile:
                # Look for lines that start with "Timestamp"
                if line.startswith("Timestamp"):
                    _, timestamp_str = line.strip().split(": ")
                    curr_timestamp = datetime.fromisoformat(timestamp_str)

                    if prev_timestamp is not None and (curr_timestamp - prev_timestamp).seconds <= 120:
                        write_block = False
                    else:
                        write_block = True

                    prev_timestamp = curr_timestamp

                # Look for lines with "---"
                elif line.startswith("---"):
                    if last_line_was_delim:
                        write_block = False
                    else:
                        write_block = True
                        last_line_was_delim = True
                        continue

                else:
                    last_line_was_delim = False

                if write_block:
                    outfile.write(line)

    except FileNotFoundError as e:
        print(f"File error: {e}")
    except ValueError as e:
        print(f"Value error, could be due to incorrect datetime format: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    filter_results()
