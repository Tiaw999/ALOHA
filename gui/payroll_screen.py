# payroll_screen.py
import tkinter as tk
from tkinter import ttk

class PayrollScreen(tk.Frame):
    def __init__(self, master, store_name):
        super().__init__(master)
        self.master = master
        self.store_name = store_name  # store_name argument passed from the previous screen

        self.master.title("Payroll Home Screen")
        self.master.geometry("600x400")

        # Back Button
        tk.Button(self.master, text="<- Back", bg="orange", command=self.go_back).pack(anchor='nw', padx=10, pady=10)

        # Payroll Label
        tk.Label(self.master, text="Payroll", bg="lightblue", font=("Arial", 14)).pack()

        # Frame for the table
        frame = tk.Frame(self.master)
        frame.pack(pady=10)

        # Treeview table columns
        columns = ("PAYDATE", "EMPNAME", "REGULARPAY", "BONUS")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")

        # Setting up columns headers
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Adjust width as needed
        self.tree.pack()

        # Edit and Add Row buttons
        tk.Button(self.master, text="Edit Table", bg="green", command=self.edit_table).pack(side='left', padx=10, pady=10)
        tk.Button(self.master, text="Add Row", bg="green", command=self.add_row).pack(side='right', padx=10, pady=10)

    def go_back(self):
        print("Returning to Owner Home")
        from gui.owner_home import OwnerHome
        self.master.switch_screen(OwnerHome, self.store_name)

    def add_row(self):
        """Adds an empty row to the table."""
        self.tree.insert("", "end", values=("", "", "", ""))

    def edit_table(self):
        """Function to handle editing (placeholder for actual implementation)."""
        print("Edit table clicked")


# If you want to run this screen as a standalone window:
if __name__ == "__main__":
    root = tk.Tk()
    app = PayrollScreen(root, "StoreName")  # Pass store_name here
    app.pack()
    root.mainloop()