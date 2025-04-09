# withdrawals_screen.py
import tkinter as tk
from tkinter import ttk

import tkinter as tk
from tkinter import ttk


class WithdrawalsScreen(tk.Frame):
    def __init__(self, master, store_name, previous_screen=None):
        super().__init__(master)
        self.master = master
        self.store_name = store_name
        self.previous_screen = previous_screen

        self.configure(bg='lightgray')

        # Back Button
        self.back_button = tk.Button(self, text="<-Back", bg="orange", command=self.go_back)
        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Withdrawals Button
        self.withdrawals_button = tk.Button(self, text="Withdrawals", bg="purple", fg="white")
        self.withdrawals_button.grid(row=0, column=1, padx=10, pady=10)

        # Table
        self.tree = ttk.Treeview(self, columns=("Date", "Emp Name", "Amount", "Notes"), show="headings")
        self.tree.heading("Date", text="DATE")
        self.tree.heading("Emp Name", text="EMPNAME")
        self.tree.heading("Amount", text="AMOUNT")
        self.tree.heading("Notes", text="NOTES")
        self.tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Buttons
        self.edit_button = tk.Button(self, text="Edit Table", bg="green", command=self.edit_table)
        self.edit_button.grid(row=2, column=1, padx=10, pady=10)

        self.add_row_button = tk.Button(self, text="Add Row", bg="green", command=self.add_row)
        self.add_row_button.grid(row=2, column=2, padx=10, pady=10)

        # Store Name Label
        self.store_label = tk.Label(self, text=f"Store: {self.store_name}", bg="lightgray")
        self.store_label.grid(row=3, column=0, columnspan=3, pady=10)

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name)

    def edit_table(self):
        print("Edit Table clicked")

    def add_row(self):
        self.tree.insert("", "end", values=("", "", "", ""))

if __name__ == "__main__":
    root = tk.Tk()
    app = WithdrawalsScreen(root, "Your Store")
    root.mainloop()