import os
import json
import globals as globals

def group_data_by_time(data):
    # Change the tid column to a string for grouping
    data['tid'] = data['tid'].apply(lambda x: str(x).replace('0 days ', '').replace('days ', 'day '))
    
    # Group data by 'tid' column
    grouped = data.groupby('tid')
    
    # Convert each group to a list of records and create a dictionary with 'tid' as keys
    grouped_data = {str(key): group.to_dict('records') for key, group in grouped}
    
    # Convert the dictionary to a JSON string using the custom handler
    grouped_json = json.dumps(grouped_data, indent=4,ensure_ascii=False)

    json_file_path = globals.get_output_json_file_path()

    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
    
    # Save the JSON string to a file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(grouped_json)
    
    return grouped_data