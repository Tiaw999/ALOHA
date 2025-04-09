# invoice_screen.py

import tkinter as tk
from tkinter import ttk

class InvoiceScreen(tk.Frame):
    def __init__(self, master, store_name, previous_screen):
        super().__init__(master)
        self.master = master
        self.previous_screen = previous_screen
        self.store_name = store_name
        self.master.title("Invoices")
        self.master.geometry("900x600")

        # Back and Edit buttons
        tk.Button(self, text="<-Back", bg="orange", command=self.go_back).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self, text="Invoices", bg="orange").grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self, text="Edit Table", bg="green").grid(row=0, column=2, padx=5, pady=5)

        # Table frame
        invoice_frame = tk.Frame(self)
        invoice_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Create table
        columns = ("Date Received", "Invoice Num", "Company", "Amount", "Due", "Paid", "Paid With", "Date Paid")
        self.invoice_table = ttk.Treeview(invoice_frame, columns=columns, show="headings")

        for col in columns:
            self.invoice_table.heading(col, text=col)
            self.invoice_table.column(col, width=100)

        self.invoice_table.pack()

        # Add row button
        tk.Button(self, text="Add row", bg="lightgreen", command=self.add_invoice_row).grid(row=2, column=0, columnspan=3, pady=10)

    def add_invoice_row(self):
        # Add a new row to the invoice table
        self.invoice_table.insert("", "end", values=("New Date", "New Invoice", "New Company", "New Amount", "New Due", "New Paid", "New Paid With", "New Date Paid"))

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name)