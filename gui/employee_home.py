import tkinter as tk

class EmployeeHome(tk.Frame):
    def __init__(self, master, store):
        super().__init__(master)
        self.master = master
        self.store = store
        self.master.title(f"Employee Home - {store}")
        self.create_widgets()

    def create_widgets(self):
        welcome_label = tk.Label(self, text=f"Welcome, Employee of {self.store}!", font=("Arial", 18))
        welcome_label.pack(pady=20)
        # Add more widgets as needed