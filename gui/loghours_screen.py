import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import get_connection
import mysql.connector
##push change
class LogHours(tk.Frame):
    def __init__(self, root, store_name, previous_screen):
        super().__init__(root)
        self.root = root
        self.store_name = store_name
        self.previous_screen = previous_screen
        self.root.geometry("900x600")
        self.root.title("Log Hours")
        self.pack(fill=tk.BOTH, expand=True)

        # Title label
        tk.Label(self, text="Employee Hours", font=("Arial", 16)).pack(pady=10)

        # Back button at the top-left
        back_button = tk.Button(self, text="← Back", command=self.go_back)
        back_button.pack(anchor="nw", padx=10, pady=5)

        # Frame for input fields
        entry_frame = tk.Frame(self)
        entry_frame.pack(pady=20)

        tk.Label(entry_frame, text="Employee Name:").grid(row=0, column=0, padx=5)
        self.name_entry = tk.Entry(entry_frame)
        self.name_entry.grid(row=0, column=1, padx=5)

        tk.Label(entry_frame, text="Start Time (HH:MM):").grid(row=1, column=0, padx=5)
        self.start_entry = tk.Entry(entry_frame)
        self.start_entry.grid(row=1, column=1, padx=5)

        tk.Label(entry_frame, text="End Time (HH:MM):").grid(row=2, column=0, padx=5)
        self.end_entry = tk.Entry(entry_frame)
        self.end_entry.grid(row=2, column=1, padx=5)

        add_btn = tk.Button(self, text="Submit Hours", bg="#28a745", fg="white", command=self.add_entry)
        add_btn.pack(pady=20)

    def add_entry(self):
        name = self.name_entry.get().strip()
        start_time = self.start_entry.get().strip()
        end_time = self.end_entry.get().strip()

        if not name or not start_time or not end_time:
            messagebox.showerror("Input Error", "All fields are required.")
            return

        try:
            now = datetime.now()
            clock_in = datetime.strptime(start_time, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
            clock_out = datetime.strptime(end_time, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
            if clock_out < clock_in:
                clock_out = clock_out.replace(day=clock_out.day + 1)

            regin = float(clock_in.strftime('%H.%M'))
            regout = float(clock_out.strftime('%H.%M'))
        except ValueError:
            messagebox.showerror("Format Error", "Time format must be HH:MM (24-hour).")
            return

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user= 'root',
                password='rootroot',
                database='store_manager'
            )
            cursor = connection.cursor()

            # Check if employee exists first
            cursor.execute(
                "SELECT 1 FROM staff WHERE name = %s AND storename = %s",
                (name, self.store_name)
            )
            if not cursor.fetchone():
                messagebox.showerror(
                    "Input Error",
                    f"Employee '{name}' is not registered under store '{self.store_name}'."
                )
                connection.close()
                return

            query = """
                INSERT INTO timesheet (storename, empname, clock_in, clock_out, regin, regout)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (self.store_name, name, clock_in, clock_out, regin, regout))
            connection.commit()
            cursor.close()
            connection.close()

            messagebox.showinfo("Success", "Hours logged successfully!")

            self.name_entry.delete(0, tk.END)
            self.start_entry.delete(0, tk.END)
            self.end_entry.delete(0, tk.END)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name)