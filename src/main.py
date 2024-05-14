import os
from process_input.process_input import process_input
from process_output.process_output import process_output
from user_preferences.user_preferences import *
from pf_sim_run.sims.sim_specific_start_time import sim_specific_start_time
from pf_sim_run.sims.sim_specific_timestamps import sim_specific_timestamps
from pf_sim_run.sims.sim_all_with_interval import sim_all_with_interval
from pf_sim_run.sims.sim_all import sim_all

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
        print(f"Timestamps that will be simulated: {timestamps}")
        app = sim_specific_timestamps(timestamps)
    
    if simulation_mode == 2:
        # start_time, interval, total_timestamps = get_input_for_mode_specific_start_time()
        # print(f"Start Time: {start_time}, Interval (in seconds) between each simulation: {interval}, Total number of timestamps: {total_timestamps}")
        # app = sim_specific_start_time(start_time, interval, total_timestamps)
        app = sim_specific_start_time()
        
    if simulation_mode == 3:
        interval = get_input_for_mode_all_timestamps_with_interval()
        print(f"Interval (in seconds) between each simulation for all timestamps: {interval}")
        app = sim_all_with_interval(interval)
        
    if simulation_mode == 4:
        print("Simulating all timestamps -")
        app = sim_all()

    process_output()
    
    del app
    
if __name__ == "__main__":
    main()
