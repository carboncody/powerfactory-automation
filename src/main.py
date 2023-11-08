import os
from parse_csv import parse_csv
from calc_resolution import calc_resolution
from group_data_by_time import group_data_by_time
from calc_busbar_pos import calc_busbar_pos

def main():
    os.system('cls')

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
    # print(f"Data saved to grouped_data.json")
   
    
    df = calc_busbar_pos(master_data, 'utils\output.csv')

    # print(master_data)
if __name__ == "__main__":
    main()
    
    