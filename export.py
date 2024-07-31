import csv
import time
import os

def save_to_db(elapsed_time_production, elapsed_time_pause, elapsed_time_panne, elapsed_time_reglage, elapsed_time_organisation, elapsed_time_changement):
    # Define the CSV file name
    csv_file = 'durations.csv'
    
    # Check if file exists to determine if we need to write the header
    file_exists = os.path.isfile(csv_file)
    
    # Get the current time for the timestamp
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    # Data to be written to the CSV
    data = [
        [current_time, elapsed_time_production, elapsed_time_pause, elapsed_time_panne, elapsed_time_reglage, elapsed_time_organisation, elapsed_time_changement]
    ]
    
    # Write data to CSV file
    with open(csv_file, mode='a', newline='') as file:  # 'a' mode opens the file for appending
        writer = csv.writer(file)
        if not file_exists:
            # Write the header if the file is new
            writer.writerow(['Timestamp', 'Production', 'Pause', 'Panne', 'Reglage', 'Organisation', 'Changement'])
        writer.writerows(data)
