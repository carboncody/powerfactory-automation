# log_window_ui.py
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class LogWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Create a ScrolledText widget for displaying logs
        self.log_text = ScrolledText(self, state='disabled', wrap='word', height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def write_log(self, message):
        """Writes the message to the Text widget."""
        self.log_text.config(state='normal')  # Enable editing the text widget
        self.log_text.insert(tk.END, message + '\n')  # Insert the message
        self.log_text.yview(tk.END)  # Auto-scroll to the bottom
        self.log_text.config(state='disabled')  # Disable editing again

    def clear(self):
        """Clears the text in the log window."""
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')

class RedirectText:
    """Redirect print statements to the log window."""
    def __init__(self, log_window):
        self.log_window = log_window

    def write(self, message):
        if message.strip() != "":  # Avoid empty messages
            self.log_window.write_log(message)

    def flush(self):
        pass  # Not required, but Python expects it
