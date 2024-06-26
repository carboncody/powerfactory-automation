import pandas as pd
def calc_resolution(master_data):
    # Calculate differences between each consecutive time entry
    master_data['time_diff'] = master_data['tid'].diff()
    
    # Find the largest gap
    largest_gap = master_data['time_diff'].max()
    
    # Format the largest gap to remove the 'days' part, if less than 1 day
    if largest_gap < pd.Timedelta(days=1):
        largest_gap_str = str(largest_gap).split(' days ')[-1]
    else:
        largest_gap_str = str(largest_gap)
    
    return largest_gap_str 
