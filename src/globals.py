import os
import json

# Function to get the correct base directory, considering PyInstaller's extraction
def get_base_dir():
    """Return the base directory path for both development and bundled execution."""
    try:
        # If running in a PyInstaller bundle, use _MEIPASS to get the temp directory
        return sys._MEIPASS  # type: ignore
    except AttributeError:
        # If not bundled, use the current directory
        return os.path.dirname(os.path.abspath(__file__))

# JSON file to store global variables
base_dir = get_base_dir()
json_file_path = os.path.join(base_dir, 'globals_config.json')

# Default global variables
default_globals = {
    'init_project_name': 'S-Banen(55)',
    'input_path': os.path.join(base_dir, 'src', 'input'),
    'output_path': os.path.join(base_dir, 'src', 'output'),
    'pf_path': r'C:/Program Files/DIgSILENT/PowerFactory 2023/Python/3.9',
    'simulation_run_count': 5
}

# Load global variables from the JSON file
def load_globals():
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            loaded_globals = json.load(f)
            # Validate paths are correct, fallback to defaults if missing
            if not isinstance(loaded_globals.get('input_path', ''), str) or not os.path.isdir(loaded_globals['input_path']):
                loaded_globals['input_path'] = default_globals['input_path']
            if not isinstance(loaded_globals.get('output_path', ''), str) or not os.path.isdir(loaded_globals['output_path']):
                loaded_globals['output_path'] = default_globals['output_path']
            return loaded_globals
    else:
        return default_globals

# Save global variables to the JSON file
def save_globals(new_globals):
    with open(json_file_path, 'w') as f:
        json.dump(new_globals, f, indent=4)

# Load current globals at runtime
globals_config = load_globals()

# Access global variables from the loaded configuration
init_project_name = globals_config.get('init_project_name')
input_path = globals_config.get('input_path')
output_path = globals_config.get('output_path')
pf_path = globals_config.get('pf_path')
simulation_run_count = globals_config.get('simulation_run_count')

def validate_path(path):
    if not isinstance(path, str) or not os.path.isdir(path):
        raise ValueError(f"Invalid path: {path}")
    return path

# Dynamic path calculation based on the current input/output paths
def get_time_series_json_path():
    return os.path.join(validate_path(input_path), 'timeseries.json')

def get_main_sim_output_path():
    return os.path.join(validate_path(output_path), 'main_sim_output.csv')

def get_rectifier_table_output_path():
    return os.path.join(validate_path(output_path), 'rectifier_table_output.csv')

def get_graphs_path():
    return os.path.join(validate_path(output_path), 'graphs')

def get_rectifier_graphs_path():
    return os.path.join(validate_path(output_path), 'graphs', 'rectifier')

def get_sorted_csvs_path():
    return os.path.join(validate_path(output_path), 'csv')

def get_input_csv_path():
    return os.path.join(validate_path(input_path), 'example.csv')
