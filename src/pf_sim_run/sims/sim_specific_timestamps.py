import json
import globals as globals
from pf_sim_run.sims.run_sim import run_sim
from pf_sim_run.pf_sim_run import *

def sim_specific_timestamps(timestamps):
    with open(globals.time_series_json_path, 'r') as file:
        data = json.load(file)

    return run_sim(timestamps, data)