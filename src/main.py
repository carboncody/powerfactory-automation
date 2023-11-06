import pandas as pd

def main():
    print("Starting Parsing")

    # Specify the file to read
    master_path = 'utils/example.csv'

    # Read the CSV file
    master_data = pd.read_csv(master_path)

    # Convert 'tid' to a timedelta object assuming the format is HH.MM.SS
    # We replace the periods with colons first
    master_data['tid'] = pd.to_timedelta(master_data['tid'].str.replace('.', ':'))

    # Sort the data by time, just in case it's not already
    master_data = master_data.sort_values('tid')

    # Calculate differences between each consecutive time entry
    master_data['time_diff'] = master_data['tid'].diff()

    # Find the largest gap
    largest_gap = master_data['time_diff'].max()
    
     # Format the largest gap to remove the 'days' part, if the largest gap is less than 1 day
    if largest_gap < pd.Timedelta(days=1):
        largest_gap_str = str(largest_gap).split(' days ')[-1]
    else:
        # Here we keep the days part if the gap is actually larger than 1 day
        largest_gap_str = str(largest_gap)

    # Print the largest gap
    print(f"The biggest resolution is: {largest_gap_str} in HH:MM:SS")
    print(f"The Resoluton in simulation is = {largest_gap_str} ")

if __name__ == "__main__":
    main()
