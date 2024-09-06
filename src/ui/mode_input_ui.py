import tkinter as tk

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
            tk.Button(self, text="Run Simulation", command=self.run_mode_1).pack(pady=10)

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

            tk.Button(self, text="Run Simulation", command=self.run_mode_2).pack(pady=10)

        elif self.mode == 3:
            tk.Label(self, text="Enter Interval (in seconds):").pack()
            self.interval_entry = tk.Entry(self)
            self.interval_entry.pack(fill=tk.X, padx=10, pady=5)
            tk.Button(self, text="Run Simulation", command=self.run_mode_3).pack(pady=10)

        elif self.mode == 4:
            tk.Label(self, text="Simulating all timestamps").pack()
            tk.Button(self, text="Run Simulation", command=self.run_mode_4).pack(pady=10)

    def run_mode_1(self):
        timestamps = self.timestamps_entry.get().split(',')
        self.proceed_callback(1, {"timestamps": timestamps})

    def run_mode_2(self):
        start_time = self.start_time_entry.get()
        interval = int(self.interval_entry.get())
        total_timestamps = int(self.total_timestamps_entry.get())
        self.proceed_callback(2, {"start_time": start_time, "interval": interval, "total_timestamps": total_timestamps})

    def run_mode_3(self):
        interval = int(self.interval_entry.get())
        self.proceed_callback(3, {"interval": interval})

    def run_mode_4(self):
        self.proceed_callback(4, {})
