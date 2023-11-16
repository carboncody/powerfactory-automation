def get_project_state(app, cubicle_busbar_1, new_busbar_1):
    # Get existing busbars
    existing_busbars = app.GetCalcRelevantObjects("*.ElmTerm")
    existing_busbar_fullnames = [busbar.GetFullName() for busbar in existing_busbars]
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

    line_str_to_split = "84-013.630-R-2-Skinne"
    test_line = existing_lines[next((index for index, s in enumerate(existing_lines_fullname) if line_str_to_split in s), None)]
    attributes = test_line.GetAttributes()[0]
    
    print("test break")
    
    # print(test_line.GetFullName())
    # terminal_conmnected_to_splitlines = app.SplitLine(test_line)
    # split_lines = terminal_conmnected_to_splitlines.GetConnectedElements()
    
    # print("Length of line before splitting :", test_line.MeasureLength(0))
    # print("Length of line 1 after splitting :", split_lines[0].MeasureLength(0))
    # print("Length of line 2 after splitting :", split_lines[1].MeasureLength(0))
            
    return [existing_busbar_names, existing_line_names]
