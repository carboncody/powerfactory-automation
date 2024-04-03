import json
import globals
from pf_sim_run.sims.run_sim import run_sim
from pf_sim_run.pf_sim_run import *
from datetime import datetime, timedelta

def calculate_specific_timestamps(start_time_str, interval_seconds, total_timestamps, data):
    start_time = datetime.strptime(start_time_str, "%H:%M:%S")
    timestamps = []
    missing_count = 0
    
    for i in range(total_timestamps):
        while True:
            current_timestamp = start_time + timedelta(seconds=interval_seconds * (i + missing_count))
            current_timestamp_str = current_timestamp.strftime("%H:%M:%S")
            # Check if the timestamp exists in the data
            if current_timestamp_str in data:
                timestamps.append(current_timestamp_str)
                break
            else:
                print(f"WARNING: timestamp {current_timestamp_str} not found! Searching next available timestamp.")
                missing_count += 1

    print("Chosen timestamps:", timestamps)
    return timestamps


def sim_specific_start_time(start_time, interval_in_seconds, total_timestamps):
    with open(globals.time_series_json_path, 'r') as file:
        data = json.load(file)

    specific_timestamps = calculate_specific_timestamps(start_time, interval_in_seconds, total_timestamps, data)
    
    return run_sim(specific_timestamps, data)
