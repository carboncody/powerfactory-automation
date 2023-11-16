import pandas as pd

def get_existing_busbars(project_busbar_names, busbar_pos_df):
    pd.DataFrame(project_busbar_names).to_csv('utils/project_busbar_names.csv', index=False, header=True, encoding='utf-8-sig')
    print("\nBusbars in project saved to utils/project_busbar_names.csv")
    
    # Create DataFrame with busbar_name
    busbar_pos_tobe_added_df = pd.DataFrame({
        'busbar_name': pd.concat([busbar_pos_df['koerledning_pos'], busbar_pos_df['retur_pos']], ignore_index=True)
    })
    
    # Function to check if value is a substring in any busbar_names
    def is_substring_of_any(value, busbar_names):
        return any(value in busbar_name for busbar_name in busbar_names)

    # Function to get the matching project_busbar_name
    def get_matching_busbar_name(value, busbar_names):
        for busbar_name in busbar_names:
            if value in busbar_name:
                return busbar_name
        return None

    # Apply the functions
    busbar_pos_tobe_added_df['is_substring'] = busbar_pos_tobe_added_df['busbar_name'].apply(
        lambda x: is_substring_of_any(x + '-', project_busbar_names)
    )
    busbar_pos_tobe_added_df['project_busbar_name'] = busbar_pos_tobe_added_df['busbar_name'].apply(
        lambda x: get_matching_busbar_name(x + '-', project_busbar_names)
    )

    # Create new DataFrame with matches
    matched_busbar_df = busbar_pos_tobe_added_df[busbar_pos_tobe_added_df['is_substring']].drop(columns='is_substring')
    matched_busbar_df.to_csv('utils/matched_busbar_names.csv', index=False, header=True, encoding='utf-8-sig')
    print("\nMatching busbars saved to utils/matched_busbar_names.csv")
    
    print("\nMatching busbars found: ", len(matched_busbar_df))
    
    return matched_busbar_df
    