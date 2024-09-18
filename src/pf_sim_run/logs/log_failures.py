import os
import csv
from datetime import datetime
import globals as globals

def log_failures(type, busbar_name, message, timestamp, project_ref_in_pf='--'):
    logs_path = globals.get_logs_csv_path()
    
    # Check if logs.csv exists, if not create it and add headers
    if not os.path.exists(logs_path):
        with open(logs_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['type', 'busbar_name', 'message', 'timestamp', 'project in pf', 'time of log'])
    
    # Read the existing content of logs.csv to check if the record already exists
    existing_records = []
    with open(logs_path, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header
        for row in reader:
            existing_records.append(row)
    
    # Prepare the new record
    new_record = [type, busbar_name, message, timestamp, project_ref_in_pf, datetime.now().strftime("%H:%M:%S %d-%m-%Y")]
    
    # Check if the new record already exists
    if new_record not in existing_records:
        # Append the new record if it does not exist
        with open(logs_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_record)
    else:
        print("This record already exists in the log.")
