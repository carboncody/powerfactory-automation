import pandas as pd

def calc_busbar_pos(master_data):
    # Calculate the busbar position
    all_busbar_pos = master_data['km'].unique()
    print(all_busbar_pos)
    
    return all_busbar_pos