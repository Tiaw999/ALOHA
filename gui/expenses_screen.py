# expenses_screen.py
import tkinter as tk
from tkinter import ttk

class ExpensesScreen(tk.Frame):
    def __init__(self, master, store_name, previous_screen):
        super().__init__(master)
        self.master = master
        self.store_name = store_name
        self.previous_screen = previous_screen
        self.master.geometry("900x600")
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Store Name Label (centered)
        tk.Label(self, text=self.store_name, font=("Arial", 14, "bold")).grid(
            row=0, column=1, columnspan=2, pady=10
        )

        # Back Button (left aligned)
        tk.Button(self, text="<- Back", bg="orange", fg="black", font=("Arial", 12),
                  command=self.go_back).grid(row=1, column=0, padx=10, pady=5)

        # Expenses Button (right aligned)
        tk.Button(self, text="Expenses", bg="green", fg="white", font=("Arial", 12)).grid(
            row=1, column=2, padx=10, pady=5
        )

        # Table (Treeview)
        columns = ("Date", "Expense Type", "Expense Value")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Edit Table Button
        tk.Button(self, text="EDIT", bg="green", fg="white", font=("Arial", 12),
                  command=self.edit_table).grid(row=3, column=1, pady=5)

        # Add Row Button
        tk.Button(self, text="Add Row", bg="green", fg="white", font=("Arial", 12),
                  command=self.add_row).grid(row=3, column=2, pady=5)

    def add_row(self):
        self.tree.insert("", "end", values=("", "", ""))

    def edit_table(self):
        print("Edit table clicked")

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name)