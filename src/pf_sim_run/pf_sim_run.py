from pf_sim_run.init_pf import init_pf
from pf_sim_run.get_project_state import get_project_state
from pf_sim_run.skip_existing_busbars import skip_existing_busbars
from pf_sim_run.create_busbars import create_busbars
from pf_sim_run.get_splitting_info import get_splitting_info

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

def pf_sim_run(busbar_pos_df):
    app = init_pf()
    
    existing_busbars = app.GetCalcRelevantObjects("*.ElmTerm")
    existing_busbar_names = [busbar.GetNodeName() for busbar in existing_busbars]
    
    busbar_tocreate_df = skip_existing_busbars(existing_busbar_names, busbar_pos_df)
    
    iteration_count = 0
    # Iterate through the busbars to create
    for _, row in busbar_tocreate_df.iterrows():
        if iteration_count >= 100:
            break  # Exit the loop if the counter is equal to or greater than 1
         
        [existing_busbar_names, existing_lines, existing_line_names] = get_project_state(app)
        
        busbar_info = parse_name(row['busbar_name'])
        if not busbar_info:
            continue

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
                        print('Busbar to be created - ', row['busbar_name'])
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
                                new_line_name = '-'.join([split_line.loc_name.split('-')[0], row['busbar_name'].split('-')[1]] + split_line.loc_name.split('-')[2:])
                                split_line.SetAttribute('loc_name', new_line_name)
                                print(f'Renamed line - {old_name} to {split_line.loc_name}')
                                
                                # Make a check if the new renamed line exists in the app
                                if check_renamed_line_exists(app, new_line_name):
                                    print(f'Line {new_line_name} successfully verified')
                                else:
                                    print(f'ERROR: Line {new_line_name} verification failed')
                                
                                new_connected_busbars = split_line.GetConnectedElements()
                                print('Newer lines connected busbars - ', new_connected_busbars)
            else:
                print('ERROR: Percent was none.')
        elif lower and not upper:
            # No need to create a split
            print(f"No need to create a split, busbar '{row['busbar_name']}' is at the same location as existing line '{lower[3]}'")
        else:
            print('ERROR: Lower or upper line could not be found.') 
            
        
        iteration_count += 1 
    
    print('Length of the busbardf - ', len(busbar_tocreate_df))
    
    # lines_tosplit_df = get_splitting_info(busbar_tocreate_df, existing_lines, existing_line_names)
    
    # create_busbars(app, existing_lines, existing_line_names, existing_lines_fullname)
    
    return app


# 81-008.975-R-2-Skinne