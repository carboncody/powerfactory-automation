import tkinter as tk
import threading
import tkinter.messagebox as messagebox

class ModeInputUI(tk.Frame):
    def __init__(self, master, mode, proceed_callback):
        super().__init__(master)
        self.master = master
        self.mode = mode
        self.proceed_callback = proceed_callback
        self.init_ui()

    def init_ui(self):
        if self.mode == 1:
            tk.Label(self, text="Enter Timestamps (comma separated):").pack()
            self.timestamps_entry = tk.Entry(self)
            self.timestamps_entry.pack(fill=tk.X, padx=10, pady=5)
            self.run_button = tk.Button(self, text="Run Simulation", command=self.run_mode_1)
            self.run_button.pack(pady=10)

        elif self.mode == 2:
            tk.Label(self, text="Enter Start Time:").pack()
            self.start_time_entry = tk.Entry(self)
            self.start_time_entry.pack(fill=tk.X, padx=10, pady=5)

            tk.Label(self, text="Enter Interval (in seconds):").pack()
            self.interval_entry = tk.Entry(self)
            self.interval_entry.pack(fill=tk.X, padx=10, pady=5)

            tk.Label(self, text="Enter Total Timestamps:").pack()
            self.total_timestamps_entry = tk.Entry(self)
            self.total_timestamps_entry.pack(fill=tk.X, padx=10, pady=5)

            self.run_button = tk.Button(self, text="Run Simulation", command=self.run_mode_2)
            self.run_button.pack(pady=10)

        elif self.mode == 3:
            tk.Label(self, text="Enter Interval (in seconds):").pack()
            self.interval_entry = tk.Entry(self)
            self.interval_entry.pack(fill=tk.X, padx=10, pady=5)
            self.run_button = tk.Button(self, text="Run Simulation", command=self.run_mode_3)
            self.run_button.pack(pady=10)

        elif self.mode == 4:
            tk.Label(self, text="Simulating all timestamps").pack()
            self.run_button = tk.Button(self, text="Run Simulation", command=self.run_mode_4)
            self.run_button.pack(pady=10)

    def run_mode_1(self):
        timestamps = self.timestamps_entry.get().split(',')
        self.disable_ui()
        threading.Thread(target=self.run_simulation_thread, args=(1, {"timestamps": timestamps})).start()

    def run_mode_2(self):
        start_time = self.start_time_entry.get()
        interval = int(self.interval_entry.get())
        total_timestamps = int(self.total_timestamps_entry.get())
        self.disable_ui()
        threading.Thread(target=self.run_simulation_thread, args=(2, {"start_time": start_time, "interval": interval, "total_timestamps": total_timestamps})).start()

    def run_mode_3(self):
        interval = int(self.interval_entry.get())
        self.disable_ui()
        threading.Thread(target=self.run_simulation_thread, args=(3, {"interval": interval})).start()

    def run_mode_4(self):
        self.disable_ui()
        threading.Thread(target=self.run_simulation_thread, args=(4, {})).start()

    def disable_ui(self):
        # Disable the button
        self.run_button.config(state=tk.DISABLED)
        # Show a "Running simulation..." message
        self.status_label = tk.Label(self, text="Running simulation...")
        self.status_label.pack()

    def run_simulation_thread(self, mode, params):
        try:
            # Run the simulation
            self.proceed_callback(mode, params)
        except Exception as e:
            # Log the error
            print(f"An error occurred during the simulation: {e}")
        finally:
            # Update the GUI after simulation completes or fails
            self.master.after(0, self.simulation_complete)

    def simulation_complete(self):
        # Remove the "Running simulation..." message
        self.status_label.destroy()

        # Disable or remove the run button
        self.run_button.destroy()  # This will completely remove the button

        # Display a "Simulation Complete" message
        self.complete_label = tk.Label(self, text="Simulation Complete", font=('Arial', 16))
        self.complete_label.pack(pady=20)
