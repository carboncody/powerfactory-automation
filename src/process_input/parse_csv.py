import pandas as pd

def parse_csv(file_path):
    
    print("Starting Parsing")
    
    # Read the CSV file and replace periods with colons
    master_data = pd.read_csv(file_path, encoding='utf-8')
    master_data['tid'] = pd.to_timedelta(master_data['tid'].str.replace('.', ':'))
    
    # Sort the data by time
    master_data = master_data.sort_values('tid')
    print("Raw data parsing done")

    
    return master_data
    