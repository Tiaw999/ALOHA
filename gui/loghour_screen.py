import tkinter as tk
from tkinter import ttk
from datetime import datetime
##push changes
class LogHours(tk.Frame):
    def __init__(self, root, store_name, previous_screen):
        super().__init__(root)
        self.root = root
        self.store_name = store_name
        self.previous_screen = previous_screen
        self.root.geometry("900x600")
        self.root.title("Log Hours")

        self.entries = []

        # Title label
        label = tk.Label(self, text="Employee Hours", font=("Arial", 16))
        label.pack(pady=10)

        # Treeview to show logged hours
        self.tree = ttk.Treeview(self, columns=("name", "start", "end", "hours"), show="headings", selectmode="browse")
        self.tree.heading("name", text="Employee Name")
        self.tree.heading("start", text="Start Time")
        self.tree.heading("end", text="End Time")
        self.tree.heading("hours", text="Hours Worked")
        self.tree.column("name", width=150)
        self.tree.column("start", width=150)
        self.tree.column("end", width=150)
        self.tree.column("hours", width=100)
        self.tree.pack(pady=10)

        # Frame for input fields
        entry_frame = tk.Frame(self)
        entry_frame.pack(pady=10)

        # Entry for employee name
        tk.Label(entry_frame, text="Name:").grid(row=0, column=0, padx=5)
        self.name_entry = tk.Entry(entry_frame)
        self.name_entry.grid(row=0, column=1, padx=5)

        # Entry for start time
        tk.Label(entry_frame, text="Start Time (HH:MM):").grid(row=0, column=2, padx=5)
        self.start_entry = tk.Entry(entry_frame)
        self.start_entry.grid(row=0, column=3, padx=5)

        # Entry for end time
        tk.Label(entry_frame, text="End Time (HH:MM):").grid(row=0, column=4, padx=5)
        self.end_entry = tk.Entry(entry_frame)
        self.end_entry.grid(row=0, column=5, padx=5)

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        add_btn = tk.Button(button_frame, text="Add", command=self.add_entry)
        add_btn.grid(row=0, column=0, padx=5)

        edit_btn = tk.Button(button_frame, text="Edit", command=self.edit_entry)
        edit_btn.grid(row=0, column=1, padx=5)

        delete_btn = tk.Button(button_frame, text="Delete", command=self.delete_entry)
        delete_btn.grid(row=0, column=2, padx=5)

    def add_entry(self):
        name = self.name_entry.get().strip()
        start_time = self.start_entry.get().strip()
        end_time = self.end_entry.get().strip()

        if not name or not start_time or not end_time:
            messagebox.showerror("Input Error", "All fields (name, start time, end time) are required.")
            return

        try:
            start_dt = datetime.strptime(start_time, "%H:%M")
            end_dt = datetime.strptime(end_time, "%H:%M")
            if end_dt < start_dt:
                end_dt = end_dt.replace(day=start_dt.day + 1)  # assume shift goes past midnight
            duration = (end_dt - start_dt).total_seconds() / 3600
            hours_worked = round(duration, 2)
        except ValueError:
            messagebox.showerror("Format Error", "Time format must be HH:MM (24-hour).")
            return

        self.entries.append((name, start_time, end_time, hours_worked))
        self.tree.insert("", "end", values=(name, start_time, end_time, hours_worked))

        self.name_entry.delete(0, tk.END)
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)

    def edit_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select an entry to edit.")
            return

        name = self.name_entry.get().strip()
        start_time = self.start_entry.get().strip()
        end_time = self.end_entry.get().strip()

        if not name or not start_time or not end_time:
            messagebox.showerror("Input Error", "All fields are required.")
            return

        try:
            start_dt = datetime.strptime(start_time, "%H:%M")
            end_dt = datetime.strptime(end_time, "%H:%M")
            if end_dt < start_dt:
                end_dt = end_dt.replace(day=start_dt.day + 1)
            duration = (end_dt - start_dt).total_seconds() / 3600
            hours_worked = round(duration, 2)
        except ValueError:
            messagebox.showerror("Format Error", "Time format must be HH:MM (24-hour).")
            return

        index = self.tree.index(selected[0])
        self.entries[index] = (name, start_time, end_time, hours_worked)
        self.tree.item(selected[0], values=(name, start_time, end_time, hours_worked))

        self.name_entry.delete(0, tk.END)
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)

    def delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select an entry to delete.")
            return

        index = self.tree.index(selected[0])
        del self.entries[index]
        self.tree.delete(selected[0])

        self.name_entry.delete(0, tk.END)
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)