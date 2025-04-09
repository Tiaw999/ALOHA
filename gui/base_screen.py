import tkinter as tk
from tkinter import ttk
from db import get_connection

class BaseScreen(tk.Frame):
    def __init__(self, master, storename, title):
        super().__init__(master)
        self.storename = storename
        self.title = title
        master.geometry("900x600")

        # Database connection
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        # Top Frame for Buttons
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(pady=10)

        self.add_button = ttk.Button(self.top_frame, text="Add Row", command=self.add_row)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = ttk.Button(self.top_frame, text="Edit Selected", command=self.edit_selected)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.back_button = ttk.Button(self.top_frame, text="Back", command=self.destroy)
        self.back_button.pack(side=tk.LEFT, padx=5)

        # Treeview for displaying data
        self.tree = ttk.Treeview(self)
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Load data method placeholder (to be overridden by subclasses)
        self.load_data()

    def load_data(self):
        pass  # To be overridden in child classes

    def add_row(self):
        pass  # To be implemented

    def edit_selected(self):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            print("Edit row with values:", values)
            # Implement actual edit logic or open edit dialog here