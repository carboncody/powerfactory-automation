import os

# Get the absolute path to the directory where globals.py is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the paths relative to the base_dir
init_project_name='S-Banen(55)'
utils_path = os.path.join(base_dir, "utils")
time_series_json_path = os.path.join(utils_path, "timeseries.json")
output_path = os.path.join(utils_path, "output")
main_sim_output_path = os.path.join(output_path, "main_sim_output.csv")
spole_table_output_path = os.path.join(output_path, "spole_table_output.csv")
graphs_path = os.path.join(output_path, "graphs")
sorted_csvs_path = os.path.join(output_path, "csv")
input_csv_path = os.path.join(utils_path, 'example.csv')
pf_path = r"C:\Program Files\DIgSILENT\PowerFactory 2023\Python\3.9"
