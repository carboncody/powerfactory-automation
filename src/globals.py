import os

cwd = os.getcwd()

utils_path = os.path.join(cwd, "utils")
time_series_json_path = os.path.join(utils_path, "timeseries.json")
output_path = os.path.join(utils_path, "output")
main_sim_output_path = os.path.join(output_path, "main_sim_output.csv")
graphs_path = os.path.join(output_path, "graphs")
sorted_csvs_path = os.path.join(output_path, "csv")
input_csv_path = 'utils/example.csv'
pf_path = r"C:\Program Files\DIgSILENT\PowerFactory 2023\Python\3.9"
