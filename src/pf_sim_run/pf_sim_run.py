from pf_sim_run.init_pf import init_pf
from pf_sim_run.get_project_state import get_project_state
import json

def parse_name(name):
    try:
        parts = name.split('-')
        bane_nr, kilometering, type, direction = parts[0], float(parts[1]), parts[2], parts[3]
        if type not in ['R', 'K'] or len(parts) < 4:
            return None
        return (bane_nr, kilometering, type, name, direction)
    except:
        return None

def find_closest_lines(busbar, existing_line_names):
    bane_nr, kilometering, type, busbar_name, direction = busbar
    existing_lines_info = [parse_name(name) for name in existing_line_names]
    existing_lines_info = [line for line in existing_lines_info if line is not None and line[0] == bane_nr and line[2] == type and line[4] == direction]
    
    if not existing_lines_info:
        print('No lines found for busbar')
        return None, None

    # Sort the filtered lines by kilometering
    sorted_lines = sorted(existing_lines_info, key=lambda x: x[1])
        
    lower, upper = None, None
    for i in range(len(sorted_lines)):
        if sorted_lines[i][1] == kilometering:
            lower = sorted_lines[i]
            upper = None
            break
        elif sorted_lines[i][1] < kilometering and (i + 1 < len(sorted_lines) and sorted_lines[i + 1][1] > kilometering):
            lower = sorted_lines[i]
            upper = sorted_lines[i + 1]
            break

    return lower, upper

def calculate_percent(lower, upper, busbar_kilometering):
    if upper == lower:  # Avoid division by zero
        return None
    return (busbar_kilometering - lower) / (upper - lower) * 100

def check_renamed_line_exists(app, new_line_name):
    existing_lines = app.GetCalcRelevantObjects("*.ElmLne")
    for line in existing_lines:
        if line.loc_name == new_line_name:
            return True
    return False

# Function to format km value as required
def format_km(km):
    return "{:07.3f}".format(float(km))

# Function to determine the value of 'spor'
def spor_value(spor):
    return '2' if 'ord' in spor else '1'

def create_busbars(app, busbar_koer, busbar_retur):
    busbars_to_create = [busbar_koer, busbar_retur]
    print('Busbars to create: ', busbars_to_create)
    [existing_busbars, existing_lines, existing_line_names] = get_project_state(app)
    
    busbars_created = []
    busbars_to_keep = []
    busbars_info = []

    # Parse busbar names and check for existing busbars
    for busbar_name in busbars_to_create:
        busbar_info = parse_name(busbar_name)
        if not busbar_info:
            print('ERROR: Invalid busbar name - ', busbar_name)
            return

        busbar_exists = False
        for existing_busbar in existing_busbars:
            if busbar_name in existing_busbar.GetNodeName():
                print('Busbar already exists - ', busbar_name)
                busbars_created.append(existing_busbar)
                busbar_exists = True
                break
        
        if not busbar_exists:
            busbars_to_keep.append(busbar_name)
            busbars_info.append(busbar_info)  # Append info only for busbars to keep

    # Process the busbars to be created
    for busbar_name, busbar_info in zip(busbars_to_keep, busbars_info):
        lower, upper = find_closest_lines(busbar_info, existing_line_names)
        
        if not lower and not upper:
            print('ERROR: Lower or upper line could not be found.')
            continue
        
        if lower and not upper:
            print(f"No need to create a split for busbar '{busbar_name}', there is one at the same location as existing line '{lower[3]}'")
            for line in existing_lines:
                if line.loc_name == lower[3]:
                    busbars_connected_to_exisitng_line = line.GetConnectedElements()
                    print('Busbars connected to line - ', {b.GetNodeName() for b in busbars_connected_to_exisitng_line}) # TODO:  NEED TO VERIFY THIS AND THEN APPEND THE CORRECT BUSBAR TO busbars_created
            continue
        
        if lower and upper:
            lower_kilometering = lower[1]
            upper_kilometering = upper[1]
            lower_line_name = lower[3]

            percent = calculate_percent(lower_kilometering, upper_kilometering, busbar_info[1])
            if percent is None:
                print('ERROR: Could not calculate percentage for busbar - ', busbar_name)
                continue
            
            for existing_line in existing_lines:
                if existing_line.loc_name != lower_line_name:
                    return
                
                # Split the line
                print('Line to split - ', lower_line_name, ' with percentage - ', percent, ' %')
                print('Busbar to be created - ', busbar_name)
                print('Splitting line ------------------------')

                old_connected_busbars = existing_line.GetConnectedElements()
                print('Older lines connected busbars - ', {b.GetNodeName() for b in old_connected_busbars})

                # Split line
                busbar_created = app.SplitLine(existing_line, percent)
                split_lines = busbar_created.GetConnectedElements()

                # Renaming the split line
                for split_line in split_lines:
                    if split_line.loc_name != lower_line_name:
                        old_name = split_line.loc_name
                        new_line_name = '-'.join([split_line.loc_name.split('-')[0], busbar_name.split('-')[1]] + split_line.loc_name.split('-')[2:])
                        split_line.SetAttribute('loc_name', new_line_name)
                        print(f'Renamed line - {old_name} to {split_line.loc_name}')

                        # Make a check if the new renamed line exists in the app
                        if check_renamed_line_exists(app, new_line_name):
                            print(f'Line {new_line_name} successfully verified')
                        else:
                            print(f'ERROR: Line {new_line_name} verification failed')

                        new_connected_busbars = split_line.GetConnectedElements()
                        print('Newer lines connected busbars - ', {b.GetNodeName() for b in new_connected_busbars})
                        busbars_created.append(busbar_created)
            
    return busbars_created

def create_define_connect_load(grid, busbars_created, load_value):
    # Create new load and set value
    load = grid.CreateObject('ElmLoddcbi','new_test_load')
    load.SetAttribute('plini', load_value)
    # TODO : verify the connection process here. What should get connected to what?
    for busbar_created in busbars_created:
        cubicle = busbar_created.CreateObject('StaCubic','new_test_cubicle')
        cubicle.obj_id = load 

    return load

def pf_sim_run():
    app, project = init_pf()
    
    user=app.GetCurrentUser()
    version = project.CreateVersion('auto_version')

    with open('utils/timeseries.json', 'r') as file:
        data = json.load(file)

    busbars_to_create = []
    counter = 0
    simulation_run_count = 0 
    interval_in_seconds = 10 # * Define 10 for 10 second interval for a 10 second step, 120 for a 2min interval
    for timestamp in data:
        if counter % interval_in_seconds == 0:
            simulation_run_count += 1
            print(f"\nSimulation run: {simulation_run_count}")
            print(f"Processing timestamp: {timestamp}")
            
            # Create a new project
            new_project = version.CreateDerivedProject('auto_project', user)
            project_activation_success = new_project.Activate()
            if project_activation_success != 0:
                raise Exception('Failed to activate new project')
            active_project = app.GetActiveProject()
            print('New project created and activated - ', active_project.loc_name)
            
            netdat = app.GetProjectFolder('netdat')
            grid = netdat.GetContents('*.ElmNet')[0]
            
            for item in data[timestamp]:
                busbar_koer =  f"{item['BTR']}-{format_km(item['km'])}-K-{spor_value(item['spor'])}"
                busbar_retur = f"{item['BTR']}-{format_km(item['km'])}-R-{spor_value(item['spor'])}"
                
                busbars_to_create.append({
                    'busbar_name': busbar_koer,
                    'koerledning_pos': busbar_koer,
                })
                
                busbars_created = create_busbars(app, busbar_koer, busbar_retur)
                
                if len(busbars_created) == 0:
                    continue
                
                load = create_define_connect_load(grid, busbars_created, item["watt [kW]"])
                
                busbars_created = []
                
                counter += 1            
                # ! adding these breaks to test run it only once
                break
    
            break
            # run_simulation(app) ComLdf.Execute()  ComLdf.IsAC()   ComLdf.IsDC()   
            # read_project_state
            # extract_data_from_project_state
            # write_data_to_file

    return app
