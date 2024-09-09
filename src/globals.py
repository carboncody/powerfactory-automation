import os

# Get the absolute path to the directory where globals.py is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Global variables with default values
init_project_name = 'S-Banen - Base - KS til 1 & 2 ved C'
input_path = r'C:/Users/mobh/Documents/GitHub/ris-sogm/src/input'
time_series_json_path = r'C:/Users/mobh/Documents/GitHub/ris-sogm/src/input\timeseries.json'
output_path = r'C:/Users/mobh/Documents/RIS out test/Output'
main_sim_output_path = r'C:/Users/mobh/Documents/RIS out test/Output\main_sim_output.csv'
rectifier_table_output_path = r'C:/Users/mobh/Documents/RIS out test/Output\rectifier_table_output.csv'
graphs_path = r'C:/Users/mobh/Documents/RIS out test/Output\graphs'
rectifier_graphs_path = r'C:/Users/mobh/Documents/RIS out test/Output\graphs\rectifier'
sorted_csvs_path = r'C:/Users/mobh/Documents/RIS out test/Output\csv'
input_csv_path = r'C:/Users/mobh/Documents/GitHub/ris-sogm/src/input\example.csv'
pf_path = r'C:/Program Files/DIgSILENT/PowerFactory 2022 SP4/Python/3.9'
simulation_run_count = 19

# Functions that should be preserved during saving
def update_globals(new_globals):
    """Update only the globals that are set in new_globals."""
    global init_project_name, input_path, output_path, pf_path, simulation_run_count, time_series_json_path, main_sim_output_path, rectifier_table_output_path, graphs_path, rectifier_graphs_path, sorted_csvs_path, input_csv_path
    
    # Update each global variable only if it's passed in new_globals
    init_project_name = new_globals.get('init_project_name', init_project_name)
    input_path = new_globals.get('input_path', input_path)
    output_path = new_globals.get('output_path', output_path)
    pf_path = new_globals.get('pf_path', pf_path)
    simulation_run_count = new_globals.get('simulation_run_count', simulation_run_count)
    time_series_json_path = os.path.join(input_path, "timeseries.json")
    main_sim_output_path = os.path.join(output_path, "main_sim_output.csv")
    rectifier_table_output_path = os.path.join(output_path, "rectifier_table_output.csv")
    graphs_path = os.path.join(output_path, "graphs")
    rectifier_graphs_path = os.path.join(output_path, "graphs\\rectifier")
    sorted_csvs_path = os.path.join(output_path, "csv")
    input_csv_path = os.path.join(input_path, 'example.csv')

def save_globals():
    """Update the global variables in globals.py without overwriting the functions."""
    globals_file = os.path.join(base_dir, 'globals.py')

    # Read the contents of globals.py
    with open(globals_file, 'r') as f:
        lines = f.readlines()

    # Separate variables section from functions section
    var_lines = []
    func_lines = []
    in_func_section = False
    for line in lines:
        if line.startswith("def "):  # We assume function definitions start with 'def'
            in_func_section = True
        if in_func_section:
            func_lines.append(line)
        else:
            var_lines.append(line)

    # Dictionary of variable assignments to update
    updated_vars = {
        'init_project_name': f"'{init_project_name}'",
        'input_path': f"r'{input_path}'",
        'output_path': f"r'{output_path}'",
        'pf_path': f"r'{pf_path}'",
        'simulation_run_count': simulation_run_count,
        'time_series_json_path': f"r'{time_series_json_path}'",
        'main_sim_output_path': f"r'{main_sim_output_path}'",
        'rectifier_table_output_path': f"r'{rectifier_table_output_path}'",
        'graphs_path': f"r'{graphs_path}'",
        'rectifier_graphs_path': f"r'{rectifier_graphs_path}'",
        'sorted_csvs_path': f"r'{sorted_csvs_path}'",
        'input_csv_path': f"r'{input_csv_path}'"
    }

    # Now modify only the variable section
    new_var_lines = []
    for line in var_lines:
        if any(var in line for var in updated_vars):
            var_name = line.split('=')[0].strip()  # Get variable name
            # Replace the line with the updated variable assignment
            new_var_lines.append(f"{var_name} = {updated_vars[var_name]}\n")
        else:
            # Keep the line unchanged if it's not a variable assignment
            new_var_lines.append(line)

    # Write back the updated file, first the variables, then the functions
    with open(globals_file, 'w') as f:
        f.writelines(new_var_lines)  # Write the updated variables section
        f.writelines(func_lines)  # Write the unchanged functions section
