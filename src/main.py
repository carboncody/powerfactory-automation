import pandas as pd
from parse_csv import parse_csv
from resolution import resolution

def main():
    

    # Specify the file to read
    master_path = 'utils/example.csv'

    # Parse the data
    master_data = parse_csv(master_path)

    # Find the biggest gap in resolution
    largest_gap_str = resolution(master_data)

    # Print the largest gap
    print(f"The biggest resolution is: {largest_gap_str} in HH:MM:SS")
    print(f"The Resolution in simulation is = {largest_gap_str}")

if __name__ == "__main__":
    main()