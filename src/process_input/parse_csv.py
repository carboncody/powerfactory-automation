import pandas as pd

def parse_csv(file_path):
    
    print("Starting Parsing")
    
    # Read the CSV file with the correct delimiter
    master_data = pd.read_csv(file_path, encoding='utf-8', sep=';')
    
    # Convert the , to . as decimal separator for the km values
    master_data['km'] = master_data['km'].str.replace(',', '.')
    
    # Convert the 'tid' column to timedelta
    master_data['tid'] = pd.to_timedelta(master_data['tid'])
    
    # Sort the data by time
    master_data = master_data.sort_values('tid')
    print("Raw data parsing done")
    
    return master_data
