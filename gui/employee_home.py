# employee_home.py
import tkinter as tk
from tkinter import ttk

class EmployeeHome(tk.Frame):
    def __init__(self, master, store_name, user, previous_screen):
        super().__init__(master)
        self.master.geometry("900x600")
        self.configure(bg="#f0f0f0")
        self.master.title("Employee Home")
        self.store_name = store_name
        self.user = user
        self.previous_screen = previous_screen

        # Back button (top left)
        back_button = ttk.Button(self, text="← Back", command=self.go_back)
        back_button.pack(anchor="nw", padx=10, pady=10)

        # Greeting
        greeting = ttk.Label(self, text=f"Employee Home - {self.store_name}", font=("Arial", 24))
        greeting.pack(pady=30)

        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)

        # Log Hours button
        log_hours_btn = ttk.Button(button_frame, text="Log Hours", width=20, command=self.log_hours)
        log_hours_btn.grid(row=0, column=0, padx=10, pady=10)

        # Log Expenses button
        log_expenses_btn = ttk.Button(button_frame, text="Log Expenses", width=20, command=self.log_expenses)
        log_expenses_btn.grid(row=1, column=0, padx=10, pady=10)

        # Close Store button
        close_store_btn = ttk.Button(button_frame, text="Close Store", width=20, style="Danger.TButton",
                                     command=self.close_store)
        close_store_btn.grid(row=2, column=0, padx=10, pady=20)

        # Style for close store button
        style = ttk.Style()
        style.configure("Danger.TButton", foreground="white", background="red")
        style.map("Danger.TButton", background=[("active", "#cc0000")])


    def log_hours(self):
        from gui.loghours_screen import LogHours
        print("Log Hours clicked")
        self.master.switch_screen(LogHours, self.store_name, self.user)


    def log_expenses(self):
        from gui.expenses_employee_screen import LogExpenses
        print("Log Expenses clicked")
        self.master.switch_screen(LogExpenses, self.store_name, self.user)

    def close_store(self):
        from gui.close_store import CloseStore
        print("Close Store clicked")
        self.master.switch_screen(CloseStore, self.store_name, self.user)

    def go_back(self):
        from gui.login_screen import LoginScreen
        self.master.switch_screen(LoginScreen)