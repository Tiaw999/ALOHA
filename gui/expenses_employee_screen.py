import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

from db import get_connection


class LogExpenses(tk.Frame):
    def __init__(self, root, store_name, user, previous_screen):
        super().__init__(root)
        self.root = root
        self.root.title("Log Expenses")
        self.store_name = store_name
        self.user = user
        self.previous_screen = previous_screen
        self.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(self, text="Store Expenses", font=("Arial", 16)).pack(pady=20)

        # Back Button
        back_button = ttk.Button(self, text="← Back", command=self.go_back)
        back_button.pack(anchor="nw", padx=10, pady=5)

        # Input fields
        form_frame = ttk.Frame(self)
        form_frame.pack(padx=10, pady=10)

        ttk.Label(form_frame, text="Expense Type:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.expense_type_entry = ttk.Entry(form_frame)
        self.expense_type_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(form_frame, text="Amount ($):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.expense_amount_entry = ttk.Entry(form_frame)
        self.expense_amount_entry.grid(row=1, column=1, padx=10, pady=5)

        # Submit Button
        submit_btn = ttk.Button(form_frame, text="Submit Expense", command=self.add_expense)
        submit_btn.grid(row=2, columnspan=2, pady=15)

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name, self.user)

    def add_expense(self):
        exp_type = self.expense_type_entry.get().strip()
        amount = self.expense_amount_entry.get().strip()

        if not exp_type or not amount:
            messagebox.showerror("Input Error", "Both fields are required.")
            return
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number.")
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()
            connection.start_transaction()  # Explicitly start transaction

            cursor.execute(
                "INSERT INTO expenses (storename, expensetype, expensevalue) VALUES (%s, %s, %s)",
                (self.store_name, exp_type, amount)
            )

            connection.commit()  # Only commits if all queries succeed

            self.expense_type_entry.delete(0, tk.END)
            self.expense_amount_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Expense submitted successfully!")

        except mysql.connector.Error as err:
            if connection:
                connection.rollback()  # Roll back any partial changes
            messagebox.showerror("Database Error", f"Error: {err}")

        finally:
            if cursor: cursor.close()
            if connection: connection.close()

# Launch function
def run_log_expenses(root, store_name, previous_screen_callback):
    for widget in root.winfo_children():
        widget.destroy()
    log_expenses_screen = LogExpenses(root, store_name, previous_screen_callback)
    log_expenses_screen.pack(fill=tk.BOTH, expand=True)
