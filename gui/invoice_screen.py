import tkinter as tk
from tkinter import ttk


class InvoiceScreen(tk.Frame):
    def add_invoice_row():
        invoice_table.insert("", "end", values=("New Date", "New Invoice", "New Company", "New Amount", "New Due", "New Paid", "New Paid With", "New Date Paid"))

    # Create main window
    invoice_root = tk.Tk()
    invoice_root.title("Invoice Home Screen")
    invoice_root.geometry("900x300")

    # Back and Edit buttons
    tk.Button(invoice_root, text="<-Back", bg="orange").grid(row=0, column=0, padx=5, pady=5)
    tk.Button(invoice_root, text="Invoices", bg="orange").grid(row=0, column=1, padx=5, pady=5)
    tk.Button(invoice_root, text="Edit Table", bg="green").grid(row=0, column=2, padx=5, pady=5)

    # Table frame
    invoice_frame = tk.Frame(invoice_root)
    invoice_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    # Create table
    columns = ("Date Received", "Invoice Num", "Company", "Amount", "Due", "Paid", "Paid With", "Date Paid")
    invoice_table = ttk.Treeview(invoice_frame, columns=columns, show="headings")

    for col in columns:
        invoice_table.heading(col, text=col)
        invoice_table.column(col, width=100)

    invoice_table.pack()

    # Add row button
    tk.Button(invoice_root, text="Add row", bg="lightgreen", command=add_invoice_row).grid(row=2, column=0, columnspan=3, pady=10)

    invoice_root.mainloop()
