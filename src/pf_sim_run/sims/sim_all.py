import json
import globals as globals
import sys
from pf_sim_run.pf_sim_run import *
from pf_sim_run.sims.run_sim import run_sim


def list_all_timestamps(data):
    # Simply extract all the timestamps from the keys of the dictionary
    timestamps = list(data.keys())

    # Optionally, you might want to sort the timestamps to ensure they are in chronological order
    timestamps.sort()
    
    return timestamps

def sim_all():
    with open(globals.time_series_json_path, 'r') as file:
        data = json.load(file)

    return list_all_timestamps(data)
