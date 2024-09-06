import tkinter as tk

class ModeSelectionUI(tk.Frame):
    def __init__(self, master, proceed_callback):
        super().__init__(master)
        self.master = master
        self.proceed_callback = proceed_callback
        self.simulation_mode = tk.IntVar()

        self.init_ui()

    def init_ui(self):
        tk.Label(self, text="Choose Simulation Mode:").pack(pady=10)

        modes = [
            ("Mode 1: Specific Timestamps", 1),
            ("Mode 2: Start Time and Interval", 2),
            ("Mode 3: All Timestamps with Interval", 3),
            ("Mode 4: All Timestamps", 4)
        ]

        for mode, val in modes:
            tk.Radiobutton(self, text=mode, variable=self.simulation_mode, value=val).pack(anchor=tk.W)

        # Button to Proceed to mode-specific input
        tk.Button(self, text="Next", command=self.proceed).pack(pady=20)

    def proceed(self):
        selected_mode = self.simulation_mode.get()
        if selected_mode in [1, 2, 3, 4]:
            self.proceed_callback(selected_mode)
