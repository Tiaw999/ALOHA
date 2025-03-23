import tkinter as tk
from tkinter import ttk


class StaffScreen(tk.Frame):
    def add_staff_row():
        staff_table.insert("", "end", values=("New Employee", "New Hourly Rate", "New Bonus", "New Role", "New Password"))

    # Create main window
    staff_root = tk.Tk()
    staff_root.title("Staff Home Screen")
    staff_root.geometry("600x300")

    # Back and Edit buttons
    tk.Button(staff_root, text="<-Back", bg="orange").grid(row=0, column=0, padx=5, pady=5)
    tk.Button(staff_root, text="Staff", bg="yellow").grid(row=0, column=1, padx=5, pady=5)
    tk.Button(staff_root, text="Edit Table", bg="green").grid(row=0, column=2, padx=5, pady=5)

    # Table frame
    staff_frame = tk.Frame(staff_root)
    staff_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    # Create table
    columns = ("Emp Name", "Hourly Rate", "Bonus Rate", "Role", "Password")
    staff_table = ttk.Treeview(staff_frame, columns=columns, show="headings")

    for col in columns:
        staff_table.heading(col, text=col)
        staff_table.column(col, width=100)

    staff_table.pack()

    # Add row button
    tk.Button(staff_root, text="Add row", bg="lightgreen", command=add_staff_row).grid(row=2, column=0, columnspan=3, pady=10)

    staff_root.mainloop()
