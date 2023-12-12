from pf_sim_run.init_pf import init_pf
from pf_sim_run.get_project_state import get_project_state
from pf_sim_run.skip_existing_busbars import skip_existing_busbars
from pf_sim_run.create_busbars import create_busbars
from pf_sim_run.get_splitting_info import get_splitting_info
import json

def parse_name(name):
    try:
        parts = name.split('-')
        bane_nr, kilometering, type = parts[0], float(parts[1]), parts[2][0]
        if type not in ['R', 'K'] or len(parts) < 3:
            return None
        return (bane_nr, kilometering, type, name)
    except:
        return None

def find_closest_lines(busbar, existing_line_names):
    bane_nr, kilometering, type, busbar_name = busbar
    existing_lines_info = [parse_name(name) for name in existing_line_names]
    existing_lines_info = [line for line in existing_lines_info if line is not None and line[0] == bane_nr and line[2] == type]
    
    if not existing_lines_info:
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
    """Check if the new renamed line exists in the app"""
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
    [existing_busbar_names, existing_lines, existing_line_names] = get_project_state(app)
    
    busbar_info = []
    for busbar_name in [busbar_koer , busbar_retur]:
        if busbar_name in existing_busbar_names:
            continue
        busbar_info = parse_name(busbar_name)
        if not busbar_info:
            return

    busbars_created = []
    for busbar_name in [busbar_koer , busbar_retur]:
        lower, upper = find_closest_lines(busbar_info, existing_line_names)
        if lower and upper:
            lower_kilometering = lower[1]
            upper_kilometering = upper[1]
            lower_line_name = lower[3]

            percent = calculate_percent(lower_kilometering, upper_kilometering, busbar_info[1])
            if percent is not None:
                for existing_line in existing_lines:
                    # Split the line
                    if lower_line_name == existing_line.loc_name:
                        print('Line to split - ', lower_line_name, ' with percentage - ', percent, ' %')
                        print('Busbar to be created - ', busbar_name)
                        print('Splitting line ------------------------')

                        old_connected_busbars = existing_line.GetConnectedElements()
                        print('Older lines connected busbars - ', old_connected_busbars)

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
                                print('Newer lines connected busbars - ', new_connected_busbars)
                                busbars_created.append(busbar_created)
            else:
                print('ERROR: Percent was none.')
        elif lower and not upper:
            print(f"No need to create a split, busbar '{busbar_name}' is at the same location as existing line '{lower[3]}'")
        else:
            print('ERROR: Lower or upper line could not be found.')
    
    return busbars_created

def create_define_connect_load(grid, busbars_created, load_value):
    # Create new load
    load = grid.CreateObject('ElmLod','new_test_load', load_value)  # NEED TO VERIFY HOW TO DEIFNE THE LOAD VALUE
    for busbar_created in busbars_created:
        cubicle = busbar_created.CreateObject('StaCubic','new_test_cubicle')
        cubicle.obj_id = load   # NEED TO VERIFY HOW DOES THE LOAD ACTUALLY CONNECT USING -    list = (obj StaCubic).GetConnections() 
    
    return grid

def pf_sim_run():
    app, project = init_pf()
    
    # Get the grid
    netdat = app.GetProjectFolder('netdat')
    grid = netdat.GetContents('*.ElmNet')[0]

    existing_busbars = app.GetCalcRelevantObjects("*.ElmTerm")
    existing_busbar_names = [busbar.GetNodeName() for busbar in existing_busbars]

    with open('utils/timeseries.json', 'r') as file:
        data = json.load(file)

    busbars_to_create = []
    counter = 0
    simulation_run_count = 0 
    interval_in_seconds = 123456789 # Set to run only once for now, define 10 for 10 second interval for a 10 second step
    for timestamp in data:
        counter += 1
        if counter % interval_in_seconds == 0:
            simulation_run_count += 1
            print(f"\nSimulation run: {simulation_run_count}")
            print(f"Processing timestamp: {timestamp}")
            for item in data[timestamp]:
                busbar_koer =  f"{item['BTR']}-{format_km(item['km'])}-K-{spor_value(item['spor'])}"
                busbar_retur = f"{item['BTR']}-{format_km(item['km'])}-R-{spor_value(item['spor'])}"
                
                busbars_to_create.append({
                    'busbar_name': busbar_koer,
                    'koerledning_pos': busbar_koer,
                })
                
                busbars_created = create_busbars(app, busbar_koer, busbar_retur, existing_busbar_names)
                
                grid = create_define_connect_load(grid, busbars_created, item["watt [kW]"])
    
            # run_simulation(app)
            # read_project_state
            # extract_data_from_project_state
            # write_data_to_file
            # create new version of project
            # activate_new_project(app, new_project_name)

            
    return app
