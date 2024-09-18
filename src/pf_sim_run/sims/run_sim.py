import globals as globals
from pf_sim_run.init_pf import init_pf
from pf_sim_run.pf_sim_run import *

def run_sim(timestamps, data):
    app, project = init_pf() # type: ignore
    
    if app is None or project is None:
        print("Failed to initialize PowerFactory. Please check the PowerFactory path and project.")
        # You can either raise an exception, return early, or handle it in another way.
        raise Exception("PowerFactory initialization failed.")
    else:
        
        user=app.GetCurrentUser()
        version = project.CreateVersion('auto_version')
        sim_run_count = 0
        busbar_name_kilometering_current_table = []
        rectifier_current_table = []
        simulation_success = 0
        
        for timestamp in timestamps:
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
                    
                    busbars_created = create_busbars(app, active_project.loc_name, busbar_koer, busbar_retur, timestamp)
                    
                    if len(busbars_created) == 0: # type: ignore
                        print("WARNING - No busbars created")
                        continue
                    
                    create_define_connect_load(grid, busbars_created, item["watt [kW]"])
                    
                [busbar_name_kilometering_current_table, rectifier_current_table, simulation_success] = clear_results_and_run_sim(app, active_project.loc_name, busbar_name_kilometering_current_table, rectifier_current_table, timestamp)
                
                if simulation_success == 0:
                    continue
            else :
                print(f"ERROR - Skipping timestamp: {timestamp} as it is not found in the data")

        # Process output
        ordered_busbar_name_kilometering_current_table = sorted(busbar_name_kilometering_current_table, key=lambda x: x[2])
        write_to_csv(ordered_busbar_name_kilometering_current_table, ['busbar_name', 'type [R or K]', 'busbar_kilometering [km]', 'voltage [V]', 'timestamp [HH:MM:SS]'], globals.get_main_sim_output_path())
        ordered_rectifier_current_table = sorted(rectifier_current_table, key=lambda x: x[0])
        write_to_csv(ordered_rectifier_current_table, ['rectifier_name', 'current [A]', 'timestamp [HH:MM:SS]'], globals.get_rectifier_table_output_path())
        
        return app
