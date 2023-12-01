def create_busbars(app, existing_lines, existing_lines_names, existing_lines_fullname):
    
    line_str_to_split = ["84-012.260-R-2-Skinne", "84-012.050-R-2-Skinne"]
    new_test_lines = []
    new_terminals_conmnected_to_splitlines = []
    
    for line_str in line_str_to_split:
        # Find the line in existing_lines_fullname
        test_line = existing_lines[next((index for index, s in enumerate(existing_lines_fullname) if line_str in s), None)]
        new_test_lines.append(test_line)

        # Perform the SplitLine operation
        terminal_connected = app.SplitLine(test_line, 70)
        split_lines = terminal_connected.GetConnectedElements()
        print("----------------------------------------\n")
        print(split_lines)
        new_terminals_conmnected_to_splitlines.append(terminal_connected)
    
    return 0