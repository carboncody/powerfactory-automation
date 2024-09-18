import json
import globals as globals
from pf_sim_run.pf_sim_run import *
from datetime import datetime, timedelta

def calculate_specific_timestamps(interval_seconds, data):
    start_time_str = list(data.keys())[0]
    start_time = datetime.strptime(start_time_str, "%H:%M:%S")
    
    timestamps = []
    
    current_time = start_time
    while True:
        current_timestamp_str = current_time.strftime("%H:%M:%S")
        
        # Break if the current timestamp is beyond the last timestamp in the dataset
        if current_timestamp_str not in data:
            break
        
        timestamps.append(current_timestamp_str)
        
        # Increment the current_time by interval_seconds
        current_time += timedelta(seconds=interval_seconds)
    
    print("Chosen timestamps:", timestamps)
    return timestamps


def sim_all_with_interval(interval_in_seconds):
    with open(globals.get_time_series_json_path(), 'r') as file:
        data = json.load(file)

    return calculate_specific_timestamps(interval_in_seconds, data)
