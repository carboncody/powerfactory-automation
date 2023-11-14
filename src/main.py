import os
from process_input.parse_csv import parse_csv
from process_input.calc_resolution import calc_resolution
from process_input.group_data_by_time import group_data_by_time
from process_input.calc_kms import calc_kms
from pf_sim_run.init_PF import init_PF
from process_input.calc_busbar_pos import calc_busbar_pos

def main():
    os.system('cls')
    print("-----------------------------------------------------")

    # Specify the file to read
    master_path = 'utils/example.csv'

    # Parse the data
    master_data = parse_csv(master_path)

    # Find the biggest gap in resolution
    resolution = calc_resolution(master_data)
    
    # Print the largest gap
    print(f"\nThe biggest resolution is: {resolution} in HH:MM:SS")
    print(f"The Resolution in simulation is = {resolution}")
    
    #Remove the extra column added by calc_resolution to master_data for calculating
    master_data = master_data.drop('time_diff', axis=1)
  
    # Group the data by time and dump it as a JSON
    timely_grouped_json = group_data_by_time(master_data)
    print(f"Data saved to grouped_data.json")
   
    km_df = calc_kms(master_data, 'utils/km_pos.csv')
    busbar_pos_df= calc_busbar_pos(km_df)
    
if __name__ == "__main__":
    main()
    