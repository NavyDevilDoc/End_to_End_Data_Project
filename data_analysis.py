# Import required libraries
import sqlite3
import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def query_to_dataframe(database_path, query):
    conn = sqlite3.connect(database_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def perform_eda_and_plot(df):
    """
    Perform exploratory data analysis and plot variables.
    
    Parameters:
    df (pd.DataFrame): Dataframe containing sensor data
    
    """
    
    # Convert 'timestamp' to datetime object
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Create an 'hours' column based on the time elapsed since the first timestamp
    df['hours'] = (df['timestamp'] - df['timestamp'].min()).dt.total_seconds() / 3600.0
    
    # Summary statistics
    print("Summary Statistics:")
    print(df.describe())
    
    # Convert the 'timestamp' column to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Set the timestamp as the index
    df.set_index('timestamp', inplace=True)
    
    # Plotting Temperature, Pressure, and Humidity against Time
    plt.figure(figsize=(20, 10))

    plt.subplot(3, 1, 1)
    plt.plot(df.index, df['temperature'], label='Temperature', color='r')
    plt.title('Temperature vs Time')
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    
    plt.subplot(3, 1, 2)
    plt.plot(df.index, df['pressure'], label='Pressure', color='g')
    plt.title('Pressure vs Time')
    plt.xlabel('Time')
    plt.ylabel('Pressure')
    
    plt.subplot(3, 1, 3)
    plt.plot(df.index, df['humidity'], label='Humidity', color='b')
    plt.title('Humidity vs Time')
    plt.xlabel('Time')
    plt.ylabel('Humidity')

    plt.tight_layout()
    plt.show()

    # Histograms
    df[['temperature', 'pressure', 'humidity']].hist(figsize=(14, 10), bins=20)
    plt.suptitle('Histograms of Temperature, Pressure, and Humidity')
    plt.show()

    # Box Plots
    plt.figure(figsize=(14, 6))
    df.boxplot(column=['temperature', 'pressure', 'humidity'])
    plt.title('Box Plots of Temperature, Pressure, and Humidity')
    plt.show()
    
    # Correlation Matrix
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.show()
    
    # Rolling Statistics - Rolling Mean for Temperature
    rolling_mean_temp = df['temperature'].rolling(window=50).mean()  # 50 is the window size
    plt.figure(figsize=(14, 6))
    plt.plot(df.index, df['temperature'], label='Actual Temperature')
    plt.plot(df.index, rolling_mean_temp, label='Rolling Mean Temperature', color='orange')
    plt.title('Temperature with Rolling Mean')
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.legend()
    plt.show()

    # Outlier Detection using Z-Score
    z_scores = np.abs(stats.zscore(df[['temperature', 'pressure', 'humidity']]))
    outliers = (z_scores > 3).any(axis=1)
    
    print(f"Number of outliers detected: {outliers.sum()}")
    
    # Remove Outliers
    df_cleaned = df[~outliers]
    
    # Print summary statistics of cleaned data
    print("Summary statistics after outlier removal:")
    print(df_cleaned.describe())
    
    # Note: Now using 'hours' for the x-axis and added units to y-axis labels
    plt.plot(df_cleaned['hours'], df_cleaned['temperature'], label='Temperature (°F)')
    plt.plot(df_cleaned['hours'], df_cleaned['pressure'], label='Pressure (kPa)')
    plt.plot(df_cleaned['hours'], df_cleaned['humidity'], label='Humidity (%)')
    
    plt.xlabel('Time (hours)')
    plt.ylabel('Sensor Readings')
    plt.title('Sensor Data (Cleaned)')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    database_path = "sensor_data.db"
    query = "SELECT * FROM Experimental_Data_Capture"
    sensor_data_df = query_to_dataframe(database_path, query)
    print(sensor_data_df.head())
    
    perform_eda_and_plot(sensor_data_df)
