import pandas as pd

def skip_existing_busbars(project_busbar_names, busbar_pos_df):
    pd.DataFrame(project_busbar_names).to_csv('utils/existing_busbars.csv', index=False, header=True, encoding='utf-8-sig')
    print("\nBusbars in project saved to utils/existing_busbars.csv")
    
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

    # Create new DataFrame with unqiue busbar positions that need to be added
    new_busbar_df = busbar_pos_tobe_added_df[~busbar_pos_tobe_added_df['is_substring']].drop(columns='is_substring')
    # Ensure there are no empty columns in the DataFrame
    new_busbar_df = new_busbar_df.dropna(axis=1, how='all')
    # Save the new busbars to be added to utils/busbars_tobeadded.csv
    new_busbar_df.to_csv('utils/busbar_tobeadded.csv', index=False, header=True, encoding='utf-8-sig')
    print("\nBusbars that need to be added: ", len(new_busbar_df))
    print("\nBusbars that will be added saved to utils/busbar_tobeadded.csv")
    print("\nExisting busbars found that will not be added: ", len(busbar_pos_tobe_added_df) - len(new_busbar_df))
    
    return new_busbar_df
    