import sys
import tkinter as tk
from ui.global_variables_ui import GlobalVariablesUI
from ui.mode_selection_ui import ModeSelectionUI
from ui.mode_input_ui import ModeInputUI
from ui.log_window_ui import LogWindow, RedirectText
from pf_sim_run.sims.sim_specific_start_time import sim_specific_start_time
from pf_sim_run.sims.sim_all_with_interval import sim_all_with_interval
from pf_sim_run.sims.sim_all import sim_all
from process_output.process_output import process_output
from pf_sim_run.sims.run_sim import run_sim
import json
import globals as globals

def run_simulation(timestamps):
    with open(globals.time_series_json_path, 'r') as file:
        data = json.load(file)
        
    return run_sim(timestamps, data)

def simulation_callback(mode, params):
    timestamps = []
    
    # Implement the simulation logic based on mode and params
    if mode == 1:
        print(f"Running Mode 1 with timestamps: {params['timestamps']}")
        timestamps = params['timestamps']
    elif mode == 2:
        print(f"Running Mode 2 with Start Time: {params['start_time']}, Interval: {params['interval']}, Total Timestamps: {params['total_timestamps']}")
        timestamps = sim_specific_start_time(params['start_time'], params['interval'], params['total_timestamps'])
    elif mode == 3:
        print(f"Running Mode 3 with Interval: {params['interval']}")
        timestamps = sim_all_with_interval(params['interval'])
    elif mode == 4:
        print(f"Running Mode 4: Simulating all timestamps")
        timestamps = sim_all()
    
    app = run_simulation(timestamps)
    process_output()
    
    del app
    
    # Add any output processing as needed
    print("Simulation complete!")

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RIS Loadflow Simulerings App")
        self.geometry("800x600")

        # Create a log window instance and pack it into the main window
        self.log_window = LogWindow(self)
        self.log_window.pack(fill=tk.BOTH, expand=True)

        # Redirect stdout and stderr to the log window
        sys.stdout = RedirectText(self.log_window)
        sys.stderr = RedirectText(self.log_window)

        # Create the initial UI (showing the global variables input screen)
        self.show_global_variables_ui()

    def show_global_variables_ui(self):
        self.clear_frame()
        self.global_variables_ui = GlobalVariablesUI(self, self.show_mode_selection_ui)
        self.global_variables_ui.pack(fill=tk.BOTH, expand=True)

    def show_mode_selection_ui(self):
        self.clear_frame()
        self.mode_selection_ui = ModeSelectionUI(self, self.show_mode_specific_input_ui)
        self.mode_selection_ui.pack(fill=tk.BOTH, expand=True)

    def show_mode_specific_input_ui(self, selected_mode):
        self.clear_frame()
        self.mode_input_ui = ModeInputUI(self, selected_mode, simulation_callback)
        self.mode_input_ui.pack(fill=tk.BOTH, expand=True)

    def clear_frame(self):
        for widget in self.winfo_children():
            if isinstance(widget, LogWindow):  # Keep the log window
                continue
            widget.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

    # Reset stdout and stderr after the application is done
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
