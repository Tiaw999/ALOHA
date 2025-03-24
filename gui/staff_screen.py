# staff_screen.py

import tkinter as tk
from tkinter import ttk

class StaffScreen(tk.Frame):
    def __init__(self, master, store_name):
        super().__init__(master)
        self.master = master
        self.store_name = store_name
        self.configure(bg="white")
        self.pack(fill="both", expand=True)

        self.create_widgets()

    def create_widgets(self):
        # Back Button
        back_button = tk.Button(self, text="<- Back", bg="orange", fg="black", font=("Arial", 12),
                                command=self.go_back)
        back_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Title Label
        title_label = tk.Label(self, text="Staff", bg="yellow", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=1, padx=5, pady=5)

        # Edit Table Button
        edit_button = tk.Button(self, text="Edit Table", bg="green", fg="white", font=("Arial", 12),
                                command=self.edit_table)
        edit_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # Table Frame
        table_frame = tk.Frame(self)
        table_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Table Columns
        columns = ("Emp Name", "Hourly Rate", "Bonus Rate", "Role", "Password")
        self.staff_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.staff_table.heading(col, text=col)
            self.staff_table.column(col, width=120)

        self.staff_table.pack()

        # Add Row Button
        add_row_button = tk.Button(self, text="Add Row", bg="lightgreen", fg="black", font=("Arial", 12),
                                   command=self.add_staff_row)
        add_row_button.grid(row=2, column=0, columnspan=3, pady=10)

    def add_staff_row(self):
        self.staff_table.insert("", "end", values=("New Employee", "New Hourly Rate", "New Bonus", "New Role", "New Password"))

    def edit_table(self):
        print("Edit Table clicked")

    def go_back(self):
        from gui.owner_home import OwnerHome  # Lazy import to prevent circular import issues
        self.master.switch_screen(OwnerHome, self.store_name)