import tkinter as tk
from tkinter import ttk

class MerchandiseScreen(tk.Frame):
    def add_merchandise_row():
        merchandise_table.insert("", "end", values=("New Date", "New Type", "New Value"))

    # Create main window
    merchandise_root = tk.Tk()
    merchandise_root.title("Merchandise Home Screen")
    merchandise_root.geometry("500x300")

    # Back and Edit buttons
    tk.Button(merchandise_root, text="<-Back", bg="orange").grid(row=0, column=0, padx=5, pady=5)
    tk.Button(merchandise_root, text="Merchandise", bg="pink").grid(row=0, column=1, padx=5, pady=5)
    tk.Button(merchandise_root, text="EDIT", bg="green").grid(row=0, column=2, padx=5, pady=5)

    # Table frame
    merchandise_frame = tk.Frame(merchandise_root)
    merchandise_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    # Create table
    columns = ("Date", "Merch Type", "Merch Value")
    merchandise_table = ttk.Treeview(merchandise_frame, columns=columns, show="headings")

    for col in columns:
        merchandise_table.heading(col, text=col)
        merchandise_table.column(col, width=120)

    merchandise_table.pack()

    # Add row button
    tk.Button(merchandise_root, text="Add row", bg="lightgreen", command=add_merchandise_row).grid(row=2, column=0, columnspan=3, pady=10)

    merchandise_root.mainloop()
