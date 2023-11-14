import pandas as pd

def calc_busbar_pos(km_df):
    # Ensure that km is treated as float
    km_df['km'] = km_df['km'].astype(float)

    # Function to format km value as required
    def format_km(km):
        return "{:07.3f}".format(km)

    # Function to determine the value of 'spor'
    def spor_value(spor):
        return '2' if 'ord' in spor else '1'

    # Applying the functions to create new columns
    km_df['koerledning_pos'] = km_df.apply(lambda x: f"{x['BTR']}-{format_km(x['km'])}-K-{spor_value(x['spor'])}", axis=1)
    km_df['retur_pos'] = km_df.apply(lambda x: f"{x['BTR']}-{format_km(x['km'])}-R-{spor_value(x['spor'])}", axis=1)

    km_df.to_csv('utils/busbar_pos.csv', index=False, header=True, encoding='utf-8-sig')
    
    return km_df