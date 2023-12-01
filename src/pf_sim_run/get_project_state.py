import csv

def get_project_state(app):
    # Get existing busbars
    existing_busbars = app.GetCalcRelevantObjects("*.ElmTerm")
    existing_busbar_names = [busbar.GetNodeName() for busbar in existing_busbars]
    
    # Get existing lines
    existing_lines = app.GetCalcRelevantObjects("*.ElmLne")
    existing_lines_fullname = [line.GetFullName() for line in existing_lines]
    existing_line_names = []
    for fullname in existing_lines_fullname:
        parts = fullname.rsplit('\\', 1)
        if len(parts) > 1:
            extracted_string = parts[-1].split('.ElmLne')[0]
            existing_line_names.append(extracted_string)
    
    with open('utils/existing_lines.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows([[item] for item in existing_line_names])

    return [existing_busbar_names, existing_lines, existing_line_names, existing_lines_fullname]
