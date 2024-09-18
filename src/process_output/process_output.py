import csv
import os
import globals as globals
import pandas as pd
from process_output.plot_busbar_voltages import plot_busbar_voltages
from process_output.plot_recitifer_currents import plot_recitifer_currents

def separate_by_type(csv_path):
    type_r_data = []
    type_k_data = []

    with open(csv_path, 'r') as file:
        csv_reader = csv.reader(file)
        
        for row in csv_reader:
            if 'R' in row[1]:
                type_r_data.append(row)
            elif 'K' in row[1]:
                type_k_data.append(row)
            else:
                print(f'Invalid busbar type: {row[1]}')

    return type_r_data, type_k_data

def separate_by_number_and_type(result_output_path, output_path):
    os.makedirs(output_path, exist_ok=True)
    
    csv_headers = ['busbar_name', 'type [R or K]', 'busbar_kilometering [km]', 'voltage [V]', 'timestamp [HH:MM:SS]']
    type_r_data, type_k_data = separate_by_type(result_output_path)
    data_by_number_and_type = {}

    for data, data_type in [(type_r_data[1:], 'R'), (type_k_data[1:], 'K')]:  # Ignore the first row (titles)
        for row in data:
            first_number = int(row[0].split('-')[0])  # Extract the first number from the first column
            key = f"{first_number}{data_type}"
            data_by_number_and_type.setdefault(key, []).append(row)

    # Save each array to a CSV file
    for key, array in data_by_number_and_type.items():
        csv_filename = os.path.join(output_path, f"{key}.csv")
        with open(csv_filename, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(csv_headers)
            csv_writer.writerows(array)

    return data_by_number_and_type

def process_output():
    data_by_number_and_type = separate_by_number_and_type(globals.get_main_sim_output_path(), globals.get_sorted_csvs_path())

    for key, array in data_by_number_and_type.items():
        print(f"Creating graphs for {key}...")
        plot_busbar_voltages(array, key, globals.get_graphs_path())
    
    # read recitifer_current_data from globals.get_rectifier_table_output_path()
    rectifier_current_data = pd.read_csv(globals.get_rectifier_table_output_path())
    plot_recitifer_currents(rectifier_current_data, globals.get_rectifier_graphs_path())
    
    print('All processing done. Goodbye!')