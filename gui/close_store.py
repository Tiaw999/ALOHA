# close_store.py
import tkinter as tk
import tkinter as tk
from tkinter import messagebox
import mysql.connector

from db import get_connection


class CloseStore(tk.Frame):
    def __init__(self, root, store_name, user, previous_screen):
        super().__init__(root)
        self.root = root
        self.root.title("Closing Tasks")
        self.store_name = store_name
        self.user = user
        self.previous_screen = previous_screen
        self.pack(fill=tk.BOTH, expand=True)

        # Back Button - Top Left
        self.back_button = tk.Button(self, text="<- Back", command=self.go_back)
        self.back_button.place(x=10, y=10)

        # Form Title
        tk.Label(self, text="Enter the following:").grid(row=1, columnspan=2, pady=20)

        # Reg Entry
        tk.Label(self, text="Reg:").grid(row=2, column=0, sticky='w', padx=10)
        self.reg_entry = tk.Entry(self)
        self.reg_entry.grid(row=2, column=1, padx=5)

        # Credit Entry
        tk.Label(self, text="Credit:").grid(row=3, column=0, sticky='w', padx=10)
        self.credit_entry = tk.Entry(self)
        self.credit_entry.grid(row=3, column=1, padx=5)

        # Cash Entry
        tk.Label(self, text="Cash In Envelope:").grid(row=4, column=0, sticky='w', padx=10)
        self.cash_entry = tk.Entry(self)
        self.cash_entry.grid(row=4, column=1, padx=5)

        # Enter Button
        self.enter_button = tk.Button(
            self,
            text="Enter",
            bg="#007bff",
            fg="white",
            activebackground="#0056b3",
            activeforeground="white",
            command=self.submit_data  # <== Hook up the logic
        )
        self.enter_button.grid(row=5, column=0, columnspan=2, pady=20)

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

            # Insert into revenue table
            query = """
                INSERT INTO revenue (storename, reg, credit, cashinenvelope)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (self.store_name, reg, credit, cash))
            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo("Success", "Closing data submitted successfully!")
            self.reg_entry.delete(0, tk.END)
            self.credit_entry.delete(0, tk.END)
            self.cash_entry.delete(0, tk.END)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def go_back(self):
        if self.previous_screen:
            self.root.switch_screen(self.previous_screen.__class__, self.store_name, self.user)
