def choose_simulation_mode():
    print("Please choose the simulation mode:")
    print("1. Specific timestamps")
    print("2. Start timestamp + interval + total number of timestamps")
    print("3. All timestamps with interval")
    print("4. All timestamps")
    
    while True:
        try:
            choice = int(input("Enter your choice (1-4): "))
            if choice in [1, 2, 3, 4]:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            
def get_input_for_mode_specific_start_time():
    # Validate start time using the validate_timestamp function
    while True:
        start_time = input("Enter start time (HH:MM:SS): ")
        validated_start_time = validate_timestamp(start_time)
        if validated_start_time:
            break
        else:
            print("Invalid time. Please ensure your time is in the format HH:MM:SS.")
    
    # Validate interval
    while True:
        try:
            interval = int(input("Enter interval in seconds (integer, 1 or bigger): "))
            if interval >= 1:
                break
            else:
                print("Interval in seconds must be 1 or bigger.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    # Validate total number of timestamps
    while True:
        try:
            total_timestamps = int(input("Enter total number of timestamps (integer, 1 or bigger): "))
            if total_timestamps >= 1:
                break
            else:
                print("Total number of timestamps must be 1 or bigger.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    return validated_start_time, interval, total_timestamps

def get_input_for_mode_specific_timestamps():
    print("Enter specific timestamps separated by space (HH:MM:SS format):")
    while True:
        input_string = input()
        timestamps = input_string.split()  # Assuming space as the separator
        validated_timestamps = [validate_timestamp(timestamp) for timestamp in timestamps]
        
        # Check if all timestamps are valid
        if None not in validated_timestamps:
            return validated_timestamps
        else:
            print("One or more timestamps are invalid. Please ensure they are in the format HH:MM:SS.")
            
def get_input_for_mode_all_timestamps_with_interval():
    print("Enter interval in seconds (integer, 1 or bigger):")
    while True:
        input_string = input()
        try:
            interval = int(input_string)
            if interval >= 1:
                return interval
            else:
                print("Interval in seconds must be 1 or bigger.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def validate_timestamp(timestamp):
    try:
        hours, minutes, seconds = map(int, timestamp.split(":"))
        if 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return None
    except ValueError:
        return None
