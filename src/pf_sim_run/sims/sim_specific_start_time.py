import json
import globals
from pf_sim_run.init_pf import init_pf
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
    app, project = init_pf()
    
    user=app.GetCurrentUser()
    version = project.CreateVersion('auto_version')

    with open(globals.time_series_json_path, 'r') as file:
        data = json.load(file)

    specific_timestamps = calculate_specific_timestamps(start_time, interval_in_seconds, total_timestamps, data)
    sim_run_count = 0
    busbar_name_kilometering_current_table = []
    
    for timestamp in specific_timestamps:
        if timestamp in data:
            sim_run_count += 1
            print(f"\n\n\n------------- Processing timestamp: {timestamp} / Simultation run: {sim_run_count} ------------- ")
            
            # Create a new project
            new_project = version.CreateDerivedProject('auto_project', user)
            project_activation_success = new_project.Activate()
            if project_activation_success != 0:
                raise Exception('Failed to activate new project')
            active_project = app.GetActiveProject()
            print('New project created and activated - ', active_project.loc_name)
            
            netdat = app.GetProjectFolder('netdat')
            grid = netdat.GetContents('*.ElmNet')[0]
            
            train_count = 0
            # Each item / train in the timestamp
            for item in data[timestamp]:
                train_count += 1
                print('\nProcessing train - ', train_count, ' / ', len(data[timestamp]), ' --- in simulation run ', sim_run_count)
                busbar_koer =  f"{item['BTR']}-{format_km(item['km'])}-K-{spor_value(item['spor'])}"
                busbar_retur = f"{item['BTR']}-{format_km(item['km'])}-R-{spor_value(item['spor'])}"
                
                busbars_to_create = []
                busbars_to_create.append({
                    'busbar_name': busbar_koer,
                    'koerledning_pos': busbar_koer,
                })
                
                busbars_created = create_busbars(app, busbar_koer, busbar_retur)
                
                if len(busbars_created) == 0:
                    print("WARNING - No busbars created")
                    continue
                
                create_define_connect_load(grid, busbars_created, item["watt [kW]"])
                
            busbar_name_kilometering_current_table = clear_results_and_run_sim(app, busbar_name_kilometering_current_table, timestamp)
        else :
            print(f"ERROR - Skipping timestamp: {timestamp} as it is not found in the data")

    # Process output
    ordered_busbar_name_kilometering_current_table = sorted(busbar_name_kilometering_current_table, key=lambda x: x[2])
    write_to_csv(ordered_busbar_name_kilometering_current_table, ['busbar_name', 'type [R or K]', 'busbar_kilometering [km]', 'voltage [V]', 'timestamp [HH:MM:SS]'], globals.main_sim_output_path)
            
    return app
