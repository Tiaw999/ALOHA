# timesheet_screen.py

import tkinter as tk
from ttkbootstrap import ttk

class TimesheetScreen(tk.Frame):
    def __init__(self, master, store_name, previous_screen):
        super().__init__(master)
        self.master = master
        self.store_name = store_name
        self.previous_screen = previous_screen
        self.master.geometry("900x600")
        self.create_widgets()

    def create_widgets(self):
        # Store Name Label
        store_label = ttk.Label(self, text=f"Timesheet - {self.store_name}", font=("Arial", 18, "bold"))
        store_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Back Button
        back_button = ttk.Button(self, text="<- Back", command=self.go_back)
        back_button.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Timesheet Label/Button (for visual consistency)
        timesheet_label = ttk.Label(self, text="Timesheet", font=("Arial", 14))
        timesheet_label.grid(row=1, column=1, padx=10, pady=5)

        # Table (Treeview)
        columns = ("DATE", "EMPNAME", "CLOCKINTIME", "CLOCKOUTTIME", "REGIN", "REGOUT")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Edit Table Button
        edit_btn = ttk.Button(self, text="Edit Table", command=self.edit_table)
        edit_btn.grid(row=3, column=1, pady=5)

        # Add Row Button
        add_row_btn = ttk.Button(self, text="Add Row", command=self.add_row)
        add_row_btn.grid(row=3, column=2, pady=5)

        # Force redraw
        self.update()

    def add_row(self):
        self.tree.insert("", "end", values=("", "", "", "", "", ""))

    def edit_table(self):
        print("Edit table clicked")

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimesheetScreen(root, "Your Store")
    root.mainloop()