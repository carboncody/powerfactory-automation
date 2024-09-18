import os
import sys
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

# Load global variables from the JSON file
def load_globals(config):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            loaded_globals = json.load(f)
            
            # Validate paths must exist, otherwise raise error
            if not isinstance(loaded_globals.get('input_path'), str):
                raise ValueError("input_path is missing or not a valid string in globals_config.json.")
            if not os.path.isdir(loaded_globals['input_path']):
                raise ValueError(f"Invalid input_path: {loaded_globals['input_path']} does not exist.")
            
            if not isinstance(loaded_globals.get('output_path'), str):
                raise ValueError("output_path is missing or not a valid string in globals_config.json.")
            if not os.path.isdir(loaded_globals['output_path']):
                raise ValueError(f"Invalid output_path: {loaded_globals['output_path']} does not exist.")
            
            return loaded_globals.get(config)
    else:
        # If no JSON file exists, raise an error to avoid unexpected behavior.
        raise FileNotFoundError(f"{json_file_path} not found. Please provide a valid globals_config.json file.")

# Save global variables to the JSON file
def save_globals(new_globals):
    with open(json_file_path, 'w') as f:
        json.dump(new_globals, f, indent=4)

def get_project_name():
    return load_globals('init_project_name')

def get_pf_path():
    return load_globals('pf_path')

def validate_path(path):
    if not isinstance(path, str) or not os.path.isdir(path):
        raise ValueError(f"Invalid path: {path}")
    return path

# Dynamic path calculation based on the current input/output paths
def get_main_sim_output_path():
    output_path = load_globals('output_path')
    return os.path.join(validate_path(output_path), 'main_sim_output.csv')

def get_rectifier_table_output_path():
    output_path = load_globals('output_path')
    return os.path.join(validate_path(output_path), 'rectifier_table_output.csv')

def get_graphs_path():
    output_path = load_globals('output_path')
    return os.path.join(validate_path(output_path), 'graphs')

def get_rectifier_graphs_path():
    output_path = load_globals('output_path')
    return os.path.join(validate_path(output_path), 'graphs', 'rectifier')

def get_sorted_csvs_path():
    output_path = load_globals('output_path')
    return os.path.join(validate_path(output_path), 'csv')

def get_input_csv_path():
    input_path = load_globals('input_path')
    return os.path.join(validate_path(input_path), 'example.csv')

def get_logs_csv_path():
    output_path = load_globals('output_path')
    return os.path.join(validate_path(output_path), 'logs.csv')

def get_output_json_file_path():
    output_path = load_globals('output_path')
    return os.path.join(validate_path(output_path), 'timeseries.json')