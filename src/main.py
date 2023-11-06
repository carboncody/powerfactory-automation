import os
import pandas as pd
from parse_csv import parse_csv
from calc_resolution import calc_resolution
from group_data_by_time import group_data_by_time

def main():
    os.system('cls')

    # Specify the file to read
    master_path = 'utils/example.csv'

    # Parse the data
    master_data = parse_csv(master_path)

     # Find the biggest gap in resolution
    resolution = calc_resolution(master_data)
    #Remove the extra column added by calc_resolution to master_data for calculating
    master_data = master_data.drop('time_diff', axis=1)
    
    # Group the data by time and dump it as a JSON
    group_data_by_time(master_data)

    # print(master_data)
if __name__ == "__main__":
    main()