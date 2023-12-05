import pandas as pd

def parse_name(name):
    try:
        parts = name.split('-')
        bane_nr, kilometering, type = parts[0], float(parts[1]), parts[2][0]
        if type not in ['R', 'K'] or len(parts) < 3:
            return None
        return bane_nr, kilometering, type
    except:
        return None

def find_closest_lines(busbar, existing_lines):
    bane_nr, kilometering, type = busbar
    filtered_lines = [line for line in existing_lines if line[0] == bane_nr and line[2] == type]
    sorted_lines = sorted(filtered_lines, key=lambda x: x[1])
    lower, upper = None, None
    for i in range(len(sorted_lines) - 1):
        if sorted_lines[i][1] < kilometering < sorted_lines[i + 1][1]:
            lower, upper = sorted_lines[i], sorted_lines[i + 1]
            break
    return lower, upper

def calculate_percent(lower, upper, busbar_kilometering):
    if upper[1] == lower[1]:  # Avoid division by zero
        return None
    return (busbar_kilometering - lower[1]) / (upper[1] - lower[1]) * 100

def create_dataframe(busbar_tocreate_df, existing_line_names):
    existing_lines = [parse_name(name) for name in existing_line_names]
    existing_lines = [line for line in existing_lines if line is not None]

    rows = []
    for _, row in busbar_tocreate_df.iterrows():
        busbar = parse_name(row['busbar_name'])
        if not busbar:
            continue
        lower, upper = find_closest_lines(busbar, existing_lines)
        if lower and upper:
            percent = calculate_percent(lower, upper, busbar[1])
            if percent is not None:
                rows.append([busbar[2], busbar[0], row['busbar_name'], '-'.join(map(str, lower)), percent])

    return pd.DataFrame(rows, columns=['type', 'bane_nr', 'busbar_name', 'lower_existing_line_name', 'percent'])

def get_splitting_info(busbar_tocreate_df, existing_lines, existing_line_names):
    line_splitting_df = create_dataframe(busbar_tocreate_df, existing_line_names)
    line_splitting_df.to_csv('line_splits.csv', index=False, header=True, encoding='utf-8-sig')
    return line_splitting_df
