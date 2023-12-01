import pandas as pd

def extract_key_info(name):
    """Extracts the key parts (kilometering and type) from a name string."""
    if name.count('-') < 2 or (not '-R' in name and not '-K' in name):
        return None  # Invalid format, skip this element

    parts = name.split('-')
    if len(parts) < 3:
        return None  # Not enough parts, skip this element

    kilometering, type_ = parts[1], parts[2][0]
    return float(kilometering), type_

def find_closest_lines(busbar_name, existing_line_names):
    """Finds the closest existing line names to the given busbar_name."""
    busbar_info = extract_key_info(busbar_name)
    if not busbar_info:
        return None, None

    busbar_km, busbar_type = busbar_info
    closest_lower = None
    closest_upper = None
    min_diff_lower = float('inf')
    min_diff_upper = float('inf')

    for line_name in existing_line_names:
        line_info = extract_key_info(line_name)
        if not line_info:
            continue

        line_km, line_type = line_info
        if line_type == busbar_type:
            # Check for closest lower line
            if line_km <= busbar_km and busbar_km - line_km < min_diff_lower:
                closest_lower = line_name
                min_diff_lower = busbar_km - line_km
            # Check for closest upper line
            elif line_km > busbar_km and line_km - busbar_km < min_diff_upper:
                closest_upper = line_name
                min_diff_upper = line_km - busbar_km

    return closest_lower, closest_upper

def create_dataframe(busbar_df, existing_line_names):
    """Creates a DataFrame with the specified columns based on the given busbar DataFrame and existing line names."""
    data = []

    for busbar_name in busbar_df['busbar_name']:
        lower_line_name, upper_line_name = find_closest_lines(busbar_name, existing_line_names)
        if lower_line_name and upper_line_name:
            lower_km, _  = extract_key_info(lower_line_name)
            upper_km , _ = extract_key_info(upper_line_name)
            busbar_km, type_ = extract_key_info(busbar_name)
            percentage = ((busbar_km - lower_km) / (upper_km - lower_km)) * 100
            data.append([type_, busbar_name, lower_line_name, percentage])
    
    new_df = pd.DataFrame(data, columns=['type', 'busbar_name', 'existing_line_name', 'percentage'])
    return new_df

def get_splitting_info(busbar_tocreate_df, existing_lines, existing_line_names):
    busbar_tocreate_df = create_dataframe(busbar_tocreate_df, existing_line_names)
    # Save the DataFrame to a CSV file
    busbar_tocreate_df.to_csv('utils/line_splits.csv', index=False, header=True, encoding='utf-8-sig')
    return busbar_tocreate_df
