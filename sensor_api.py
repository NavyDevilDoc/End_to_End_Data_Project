from flask import Flask, request, jsonify
import threading
from datetime import datetime, timedelta
import sqlite3
from database_operations import create_db_and_table

create_db_and_table('sensor_data.db')

app = Flask(__name__)

def stop_server():
    print("Stopping server after 2 hours...")
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

# Function to check if data has been collected recently
def check_data_collection():
    global last_data_time
    print("Thread started")  # Debugging print statement
    while True:
        if last_data_time:
            time_since_last_data = datetime.now() - last_data_time
            print(f"Time since last data: {time_since_last_data}")  # Debugging print statement
            if time_since_last_data > timedelta(minutes=5):  # Change this to your desired interval
                print(f"Warning: No data received for the last {time_since_last_data}!")
        else:
            print("No data received yet.")  # Debugging print statement
        threading.Event().wait(60)  # Check every 60 seconds. You can adjust this.


last_data_time = None  # Initialize a variable to keep track of the last data insertion time.
@app.route('/api/data', methods=['POST'])
def post_data():
    global last_data_time  # Declare the variable as global so you can update it here
    last_data_time = datetime.now()  # Update when a POST request is received
    print(f"Data received at {last_data_time}")  # Debugging print statement
    try:
        content = request.json
        temperature = content.get('temperature')
        pressure = content.get('pressure')
        humidity = content.get('humidity')

        if None in [temperature, pressure, humidity]:
            return jsonify({"result": "failure", "reason": "Missing values"}), 400

        with sqlite3.connect('sensor_data.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO Experimental_Data_Capture (temperature, pressure, humidity) VALUES (?, ?, ?)",
                      (temperature, pressure, humidity))
            conn.commit()

        return jsonify({"result": "success"}), 201

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return jsonify({"result": "failure", "reason": str(e)}), 500

    except Exception as e:
        print(f"General error: {e}")
        return jsonify({"result": "failure", "reason": "An unknown error occurred"}), 500

if __name__ == '__main__':
    # Create a separate thread to run the data collection check
    monitor_thread = threading.Thread(target=check_data_collection)
    monitor_thread.start()
