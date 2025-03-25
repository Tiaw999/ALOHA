# withdrawals_screen.py
import tkinter as tk
from tkinter import ttk

class WithdrawalsScreen(tk.Frame):
    def __init__(self, master, store_name, previous_screen):
        super().__init__(master)
        self.master = master
        self.store_name = store_name
        self.previous_screen = previous_screen
        self.withdrawals.title("Withdrawals")
        self.configure(bg="white")
        self.master.geometry("900x600")
        self.pack(fill="both", expand=True)

        self.create_widgets()

    def create_widgets(self):
        # Back Button
        back_button = tk.Button(self, text="<- Back", bg="orange", fg="black", font=("Arial", 12),
                                command=self.go_back)
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Title Label
        title_label = tk.Label(self, text="Withdrawals", bg="purple", fg="white", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=1, columnspan=2, pady=10)

        # Treeview Table
        columns = ("DATE", "EMPNAME", "AMOUNT", "NOTES")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Edit Table Button
        edit_button = tk.Button(self, text="Edit Table", bg="green", fg="white", font=("Arial", 12),
                                command=self.edit_table)
        edit_button.grid(row=2, column=0, pady=10)

        # Add Row Button
        add_row_button = tk.Button(self, text="Add Row", bg="green", fg="white", font=("Arial", 12),
                                   command=self.add_row)
        add_row_button.grid(row=2, column=2, pady=10)

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name)

    def edit_table(self):
        print("Edit table clicked")

    def add_row(self):
        self.tree.insert("", "end", values=("", "", "", ""))