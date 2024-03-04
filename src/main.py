import os
from process_input.process_input import process_input
import globals
from process_output.process_output import process_output
from user_preferences.user_preferences import *
from pf_sim_run.sims.sim_specific_start_time import sim_specific_start_time
from pf_sim_run.sims.sim_specific_timestamps import sim_specific_timestamps

def create_output_directory():
    os.makedirs(os.path.join('utils', 'output'), exist_ok=True)

def main():
    os.system('cls')
    print("-----------------------------------------------------")

    create_output_directory()
    # process_input()     # * THIS SAVES A JSON FILE WHICH HAS ALL THE TIMESERIES DATA IN utils/timeseries.json
    
    simulation_mode = choose_simulation_mode()
    print(f"You have chosen mode: {simulation_mode}")
    
    if simulation_mode == 1:
        timestamps = get_input_for_mode_specific_timestamps()
        print(f"Timestamps: {timestamps}")
        app = sim_specific_timestamps(timestamps)
    
    if simulation_mode == 2:
        start_time, interval, total_timestamps = get_input_for_mode_specific_start_time()
        print(f"Start Time: {start_time}, Interval: {interval}, Total Timestamps: {total_timestamps}")
        app = sim_specific_start_time(start_time, interval, total_timestamps)

    process_output()
    
    del app
    
if __name__ == "__main__":
    main()
