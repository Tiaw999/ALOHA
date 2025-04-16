
import tkinter as tk
from tkinter import ttk

import tkinter as tk
from tkinter import ttk, messagebox

class LogExpenses(tk.Frame):
    def __init__(self, root, store_name=None, previous_screen=None):
        super().__init__(root)
        self.root = root
        self.root.title("Log Expenses")
        self.store_name = store_name
        self.previous_screen = previous_screen
        self.expense_entries = []
        self.pack(fill=tk.BOTH, expand=True)

        # Back Button - Top Left
        self.back_button = tk.Button(self, text="<- Back", command=self.go_back)
        self.back_button.place(x=10, y=10)

        # Title
        tk.Label(self, text="Store Expenses", font=("Arial", 16)).pack(pady=10)

        # Treeview to display expenses
        self.tree = ttk.Treeview(self, columns=("type", "amount"), show="headings", selectmode="browse")
        self.tree.heading("type", text="Expense Type")
        self.tree.heading("amount", text="Amount ($)")
        self.tree.column("type", width=200)
        self.tree.column("amount", width=100)
        self.tree.pack(pady=10)

        # Input fields
        entry_frame = tk.Frame(self)
        entry_frame.pack(pady=10)

        tk.Label(entry_frame, text="Expense Type:").grid(row=0, column=0, padx=5)
        self.expense_type_entry = tk.Entry(entry_frame)
        self.expense_type_entry.grid(row=0, column=1, padx=5)

        tk.Label(entry_frame, text="Amount:").grid(row=0, column=2, padx=5)
        self.expense_amount_entry = tk.Entry(entry_frame)
        self.expense_amount_entry.grid(row=0, column=3, padx=5)

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        add_btn = tk.Button(button_frame, text="Add", bg="#007bff", fg="white", command=self.add_expense)
        add_btn.grid(row=0, column=0, padx=5)

        edit_btn = tk.Button(button_frame, text="Edit", command=self.edit_expense)
        edit_btn.grid(row=0, column=1, padx=5)

        delete_btn = tk.Button(button_frame, text="Delete", command=self.delete_expense)
        delete_btn.grid(row=0, column=2, padx=5)

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

        self.expense_entries.append((exp_type, f"${amount:.2f}"))
        self.tree.insert("", "end", values=(exp_type, f"${amount:.2f}"))

        self.expense_type_entry.delete(0, tk.END)
        self.expense_amount_entry.delete(0, tk.END)

    def edit_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select an entry to edit.")
            return

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

        index = self.tree.index(selected[0])
        self.expense_entries[index] = (exp_type, f"${amount:.2f}")
        self.tree.item(selected[0], values=(exp_type, f"${amount:.2f}"))

        self.expense_type_entry.delete(0, tk.END)
        self.expense_amount_entry.delete(0, tk.END)

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select an entry to delete.")
            return

        index = self.tree.index(selected[0])
        del self.expense_entries[index]
        self.tree.delete(selected[0])

        self.expense_type_entry.delete(0, tk.END)
        self.expense_amount_entry.delete(0, tk.END)

# Function to launch the LogExpenses screen
def run_log_expenses(root, store_name, previous_screen_callback):
    for widget in root.winfo_children():
        widget.destroy()
    log_expenses_screen = LogExpenses(root, store_name, previous_screen_callback)
    log_expenses_screen.pack(fill=tk.BOTH, expand=True)

