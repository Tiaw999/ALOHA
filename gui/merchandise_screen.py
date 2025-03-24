# merchandise_screen.py
import tkinter as tk
from tkinter import ttk

class MerchandiseScreen(tk.Frame):
    def __init__(self, master, store_name, previous_screen):
        super().__init__(master)
        self.master = master
        self.store_name = store_name
        self.previous_screen = previous_screen
        self.master.geometry("900x600")

        # Back and Edit buttons
        tk.Button(self, text="<-Back", bg="orange", command=self.go_back).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self, text="Merchandise", bg="pink").grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self, text="EDIT", bg="green").grid(row=0, column=2, padx=5, pady=5)

        # Table frame
        merchandise_frame = tk.Frame(self)
        merchandise_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Create table
        columns = ("Date", "Merch Type", "Merch Value")
        merchandise_table = ttk.Treeview(merchandise_frame, columns=columns, show="headings")

        for col in columns:
            merchandise_table.heading(col, text=col)
            merchandise_table.column(col, width=120)

        merchandise_table.pack()

        # Add row button
        tk.Button(self, text="Add row", bg="lightgreen", command=self.add_merchandise_row).grid(row=2, column=0, columnspan=3, pady=10)

    def add_merchandise_row(self):
        # You need to reference the table, use `self.merchandise_table` here
        self.merchandise_table.insert("", "end", values=("New Date", "New Type", "New Value"))

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name)