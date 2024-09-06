import tkinter as tk
from tkinter import filedialog
import globals as globals

class GlobalVariablesUI(tk.Frame):
    def __init__(self, master, proceed_callback):
        super().__init__(master)
        self.master = master
        self.proceed_callback = proceed_callback
        self.init_ui()

    def init_ui(self):
        tk.Label(self, text="Set Global Variables").pack(pady=10)

        # Project Name Input
        tk.Label(self, text="Project Name:").pack(fill=tk.X)
        self.project_name_entry = tk.Entry(self)
        self.project_name_entry.insert(0, globals.init_project_name)
        self.project_name_entry.pack(fill=tk.X, padx=10, pady=5)

        # Input Path Selection
        tk.Label(self, text="Input Path:").pack(fill=tk.X)
        self.input_path_entry = tk.Entry(self)
        self.input_path_entry.insert(0, globals.input_path)
        self.input_path_entry.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(self, text="Browse", command=self.browse_input_path).pack(pady=5)

        # Output Path Selection
        tk.Label(self, text="Output Path:").pack(fill=tk.X)
        self.output_path_entry = tk.Entry(self)
        self.output_path_entry.insert(0, globals.output_path)
        self.output_path_entry.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(self, text="Browse", command=self.browse_output_path).pack(pady=5)

        # PF Path Selection
        tk.Label(self, text="PowerFactory Path:").pack(fill=tk.X)
        self.pf_path_entry = tk.Entry(self)
        self.pf_path_entry.insert(0, globals.pf_path)
        self.pf_path_entry.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(self, text="Browse", command=self.browse_pf_path).pack(pady=5)

        # Proceed Button
        tk.Button(self, text="Proceed", command=self.proceed).pack(pady=20)

    def browse_input_path(self):
        path = filedialog.askdirectory()
        if path:
            self.input_path_entry.delete(0, tk.END)
            self.input_path_entry.insert(0, path)

    def browse_output_path(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, path)

    def browse_pf_path(self):
        path = filedialog.askdirectory()
        if path:
            self.pf_path_entry.delete(0, tk.END)
            self.pf_path_entry.insert(0, path)

    def proceed(self):
        input_path = self.input_path_entry.get()
        output_path = self.output_path_entry.get()
        pf_path = self.pf_path_entry.get()
        project_name = self.project_name_entry.get()

        globals.update_globals({
            'init_project_name': project_name,
            'input_path': input_path,
            'output_path': output_path,
            'pf_path': pf_path,
            'simulation_run_count': globals.simulation_run_count + 1
        })
        globals.save_globals()

        # Proceed to next step (simulation mode selection)
        self.proceed_callback()
