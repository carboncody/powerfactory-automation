import csv

def get_project_state(app):
    # Get existing busbars
    transformer_busbars = []
    existing_busbars = app.GetCalcRelevantObjects("*.ElmTerm")
    
    for busbar in existing_busbars:
        if "Ensretter" in busbar.loc_name:
            transformer_busbars.append(busbar)
    
    # Get existing lines
    existing_lines = app.GetCalcRelevantObjects("*.ElmLne")
    
    filtered_types = ['koereledning','uic60']

    existing_lines_fullname = []
    for line in existing_lines:
        type = str(line.GetType()).lower()
        # Check if any element in filtered_types is a substring in type
        if any(ftype in type for ftype in filtered_types):
            existing_lines_fullname.append(line.GetFullName())

    existing_line_names = []
    for fullname in existing_lines:
        existing_line_names.append(fullname.loc_name)

    transformers = app.GetCalcRelevantObjects("*.ElmTr2")
    # return [existing_busbars, existing_lines, existing_line_names, transformer_busbars, transformers]
    return [existing_busbars, existing_lines, existing_line_names, transformers]
