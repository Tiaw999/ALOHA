import tkinter as tk
from tkinter import messagebox
import mysql.connector

class LogExpenses(tk.Frame):
    def __init__(self, root, store_name=None, previous_screen=None):
        super().__init__(root)
        self.root = root
        self.root.title("Log Expenses")
        self.store_name = store_name
        self.previous_screen = previous_screen
        self.pack(fill=tk.BOTH, expand=True)

        # Back Button - Top Left
        self.back_button = tk.Button(self, text="<- Back", command=self.go_back)
        self.back_button.place(x=10, y=10)

        # Title
        tk.Label(self, text="Store Expenses", font=("Arial", 16)).pack(pady=20)

        # Input fields
        entry_frame = tk.Frame(self)
        entry_frame.pack(pady=10)

        tk.Label(entry_frame, text="Expense Type:").grid(row=0, column=0, padx=5, pady=5)
        self.expense_type_entry = tk.Entry(entry_frame)
        self.expense_type_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(entry_frame, text="Amount ($):").grid(row=1, column=0, padx=5, pady=5)
        self.expense_amount_entry = tk.Entry(entry_frame)
        self.expense_amount_entry.grid(row=1, column=1, padx=5, pady=5)

        # Submit button
        add_btn = tk.Button(
            self,
            text="Submit Expense",
            bg="#007bff",
            fg="white",
            command=self.add_expense
        )
        add_btn.pack(pady=20)

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name)

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
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='rootroot',
                database='store_manager'
            )
            cursor = connection.cursor()

            cursor.execute(
                "INSERT INTO expenses (storename, expensetype, expensevalue) VALUES (%s, %s, %s)",
                (self.store_name, exp_type, amount)
            )
            connection.commit()
            cursor.close()
            connection.close()

            self.expense_type_entry.delete(0, tk.END)
            self.expense_amount_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Expense submitted successfully!")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

# Launch function
def run_log_expenses(root, store_name, previous_screen_callback):
    for widget in root.winfo_children():
        widget.destroy()
    log_expenses_screen = LogExpenses(root, store_name, previous_screen_callback)
    log_expenses_screen.pack(fill=tk.BOTH, expand=True)
