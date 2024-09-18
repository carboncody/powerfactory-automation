import json
import globals as globals
from process_input.parse_csv import parse_csv
from process_input.calc_resolution import calc_resolution
from process_input.group_data_by_time import group_data_by_time
from process_input.calc_kms import calc_kms
from process_input.calc_busbar_pos import calc_busbar_pos

def process_input():
    # Parse the data
    master_data = parse_csv(globals.get_input_csv_path())

    # Find the biggest gap in resolution
    resolution = calc_resolution(master_data)
    
    # Print the largest gap
    print(f"\nThe biggest resolution is: {resolution} in HH:MM:SS")
    print(f"The Resolution in simulation is = {resolution}")
    
    # Remove the extra column added by calc_resolution to master_data for calculating
    master_data = master_data.drop('time_diff', axis=1)
  
    # # Group the data by time and dump it as a JSON
    timely_grouped_json = group_data_by_time(master_data)
    print(f"Data saved to timeseries.json")
   
    # km_df = calc_kms(master_data, 'utils/km_pos.csv')
    # busbar_pos_df= calc_busbar_pos(km_df)
    
    return timely_grouped_json
    # return busbar_pos_df
