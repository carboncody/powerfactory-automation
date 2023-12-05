import pandas as pd

def calc_kms(master_data, csv_file_path):
    
    print("\nStarting calculations of busbar positions")
    
    # Remove duplicates based on 'km', 'BTR', and 'spor' but ignore 'id'
    unique_data = master_data.drop_duplicates(subset=['km', 'BTR', 'spor'], keep='first')
    
    # Select only the required columns, excluding 'id' if it's not needed
    # Include 'id' if it is needed in the output
    processed_data = unique_data[['id', 'km', 'BTR', 'spor']].copy()
    
    # Write the processed DataFrame to a CSV file
    # processed_data.to_csv(csv_file_path, index=False, header=True, encoding='utf-8-sig')
    
    # print(f"\nProcessed data saved to {csv_file_path}")
    
    return processed_data
