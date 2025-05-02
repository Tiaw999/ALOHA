import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from db import get_connection
import mysql.connector

class LogHours(tk.Frame):
    def __init__(self, root, store_name, user, previous_screen):
        super().__init__(root)
        self.root = root
        self.store_name = store_name
        self.user = user
        self.previous_screen = previous_screen
        self.root.geometry("900x600")
        self.root.title("Log Hours")
        self.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(self, text="Employee Hours", font=("Arial", 16)).pack(pady=10)
        back_button = tk.Button(self, text="← Back", command=self.go_back)
        back_button.pack(anchor="nw", padx=10, pady=5)

        # Input Frame
        entry_frame = tk.Frame(self)
        entry_frame.pack(pady=20)

        labels = ["Start Time (HH:MM):", "End Time (HH:MM):",
                  "Register In Balance:", "Register Out Balance:"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            tk.Label(entry_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = tk.Entry(entry_frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label_text] = entry

        submit_btn = tk.Button(self, text="Submit Hours", bg="#28a745", fg="white", command=self.add_entry)
        submit_btn.pack(pady=20)

    def add_entry(self):
        start_time = self.entries["Start Time (HH:MM):"].get().strip()
        end_time = self.entries["End Time (HH:MM):"].get().strip()
        regin = self.entries["Register In Balance:"].get().strip()
        regout = self.entries["Register Out Balance:"].get().strip()

        if not all([start_time, end_time, regin, regout]):
            messagebox.showerror("Input Error", "All fields are required.")
            return

        try:
            now = datetime.now()
            clock_in = datetime.strptime(start_time, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
            clock_out = datetime.strptime(end_time, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
            if clock_out < clock_in:
                clock_out = clock_out.replace(day=clock_out.day + 1)

            regin_val = float(regin)
            regout_val = float(regout)
        except ValueError:
            messagebox.showerror("Format Error", "Check that time is HH:MM and balances are numbers.")
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO timesheet (storename, empname, clock_in, clock_out, regin, regout)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (self.store_name, self.user, clock_in, clock_out, regin_val, regout_val)
            )
            connection.commit()
            cursor.close()
            connection.close()

            messagebox.showinfo("Success", "Hours and balances logged successfully!")

            for entry in self.entries.values():
                entry.delete(0, tk.END)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name, self.user)
