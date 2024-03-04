import json
import globals
from pf_sim_run.init_pf import init_pf
from pf_sim_run.pf_sim_run import *

def sim_specific_timestamps(timestamps):
    app, project = init_pf()
    
    user = app.GetCurrentUser()
    version = project.CreateVersion('auto_version')

    with open(globals.time_series_json_path, 'r') as file:
        data = json.load(file)

    sim_run_count = 0
    busbar_name_kilometering_current_table = []
    
    for timestamp in timestamps:
        if timestamp not in data:
            print(f"WARNING: Timestamp {timestamp} not found in the data and therefore skipped.")
            continue  # Skip to the next timestamp if the current one is not found

        sim_run_count += 1
        print(f"\n\n\n------------- Processing timestamp: {timestamp} / Simulation run: {sim_run_count} ------------- ")
        
        # Create a new project
        new_project = version.CreateDerivedProject('auto_project' + timestamp.replace(':', '_'), user)  # Replace ':' with '_' to avoid invalid characters in names
        project_activation_success = new_project.Activate()
        if project_activation_success != 0:
            raise Exception('Failed to activate new project')
        active_project = app.GetActiveProject()
        print('New project created and activated - ', active_project.loc_name)
        
        netdat = app.GetProjectFolder('netdat')
        grid = netdat.GetContents('*.ElmNet')[0]
        
        train_count = 0
        # Process each item/train in the timestamp
        for item in data[timestamp]:
            train_count += 1
            print(f'\nProcessing train - {train_count} / {len(data[timestamp])} --- in simulation run {sim_run_count}')
            busbar_koer = f"{item['BTR']}-{format_km(item['km'])}-K-{spor_value(item['spor'])}"
            busbar_retur = f"{item['BTR']}-{format_km(item['km'])}-R-{spor_value(item['spor'])}"
            
            busbars_created = create_busbars(app, busbar_koer, busbar_retur)
            
            if not busbars_created:
                print("WARNING - No busbars created")
                continue
            
            create_define_connect_load(grid, busbars_created, item["watt [kW]"])
            
            busbar_name_kilometering_current_table = clear_results_and_run_sim(app, busbar_name_kilometering_current_table, timestamp)

    # Process output
    ordered_busbar_name_kilometering_current_table = sorted(busbar_name_kilometering_current_table, key=lambda x: x[2])
    write_to_csv(ordered_busbar_name_kilometering_current_table, ['busbar_name', 'type [R or K]', 'busbar_kilometering [km]', 'voltage [V]', 'timestamp'], globals.main_sim_output_path)
            
    return app