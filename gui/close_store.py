# close_store.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

from db import get_connection


class CloseStore(tk.Frame):
    def __init__(self, root, store_name, user, previous_screen):
        super().__init__(root)
        self.root = root
        self.store_name = store_name
        self.user = user
        self.previous_screen = previous_screen
        self.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(self, text="Store Close", font=("Arial", 16)).pack(pady=20)

        # Back Button
        back_button = ttk.Button(self, text="← Back", command=self.go_back)
        back_button.pack(anchor="nw", padx=10, pady=10)

        # Input fields
        form_frame = ttk.Frame(self)
        form_frame.pack(padx=10, pady=10)

        # Reg Entry
        ttk.Label(form_frame, text="Reg:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.reg_entry = ttk.Entry(form_frame)
        self.reg_entry.grid(row=0, column=1, padx=5, pady=5)

        # Credit Entry
        ttk.Label(form_frame, text="Credit:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.credit_entry = ttk.Entry(form_frame)
        self.credit_entry.grid(row=1, column=1, padx=5, pady=5)

        # Cash Entry
        ttk.Label(form_frame, text="Cash In Envelope:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.cash_entry = ttk.Entry(form_frame)
        self.cash_entry.grid(row=2, column=1, padx=5, pady=5)

        # Submit Button
        submit_btn = ttk.Button(form_frame, text="Enter", command=self.submit_data)
        submit_btn.grid(row=3, columnspan=2, pady=20)

    def submit_data(self):
        try:
            reg = float(self.reg_entry.get())
            credit = float(self.credit_entry.get())
            cash = float(self.cash_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()
            connection.start_transaction()

            query = """
                INSERT INTO revenue (storename, reg, credit, cashinenvelope)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (self.store_name, reg, credit, cash))
            connection.commit()

            # Only clear if commit succeeded
            self.reg_entry.delete(0, tk.END)
            self.credit_entry.delete(0, tk.END)
            self.cash_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Closing data submitted successfully!")

        except mysql.connector.Error as err:
            if connection:
                connection.rollback()
            messagebox.showerror("Database Error", f"Error: {err}")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def go_back(self):
        if self.previous_screen:
            self.root.switch_screen(self.previous_screen.__class__, self.store_name, self.user)
