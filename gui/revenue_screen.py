# revenue_screen.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
from datetime import datetime
import mysql.connector
from mysql.connector import Error


class RevenueScreen(tk.Frame):
    def __init__(self, master, store_name, previous_screen):
        super().__init__(master)
        self.columns = ("Date", "Reg", "Credit", "Cash in Envelope")
        self.master = master
        self.store_name = store_name
        self.previous_screen = previous_screen
        self.master.geometry("900x600")
        self.master.title("Revenue")
        self.create_widgets()
        self.fetch_revenue_data()


    def create_widgets(self):
        # Store Name Label
        store_label = ttk.Label(self, text=f"Revenue - {self.store_name}", font=("Arial", 18, "bold"))
        store_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Back Button
        back_button = ttk.Button(self, text="<- Back", command=self.go_back)
        back_button.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Revenue Label/Button (for visual consistency)
        revenue_label = ttk.Label(self, text="Revenue", font=("Arial", 14))
        revenue_label.grid(row=1, column=1, padx=10, pady=5)

        # Table (Treeview)
        columns = ("Date", "Reg", "Credit", "Cash in Envelope")
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

    def add_row(self):
        # Ask for values to add to the row
        date_str = askstring("Input", "Enter the Date (YYYY-MM-DD):")
        reg = askstring("Input", "Enter Reg:")
        credit = askstring("Input", "Enter Credit:")
        cash_in_envelope = askstring("Input", "Enter Cash in Envelope:")

        # Validate date format
        if date_str:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Date Error", "Invalid date format. Please use YYYY-MM-DD.")
                return
        else:
            messagebox.showwarning("Input Error", "Date is required.")
            return

        if reg and credit and cash_in_envelope:
            try:
                # Connect to the database
                conn = mysql.connector.connect(
                    host="localhost", user="root", password="Cooldaisy662", database="store_manager"
                )
                cursor = conn.cursor()

                # Insert the new revenue record into the database
                cursor.execute("""
                    INSERT INTO revenue (storename, reg, credit, cashinenvelope, date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (self.store_name, reg, credit, cash_in_envelope, date))

                conn.commit()

                # Fetch the new data to update the table
                self.fetch_revenue_data()

                # Close the connection
                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "New revenue record added successfully!")

            except Error as e:
                messagebox.showerror("Error", f"Error adding revenue data: {e}")
        else:
            messagebox.showwarning("Input Error", "All fields are required.")

    def edit_table(self):
        print("Edit table clicked")

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name)

    def fetch_revenue_data(self):
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="Cooldaisy662", database="store_manager"
            )
            cursor = conn.cursor()
            cursor.execute("""
                SELECT date, reg, credit, cashinenvelope 
                FROM revenue 
                WHERE storename = %s
            """, (self.store_name,))
            data = cursor.fetchall()

            # Clear the current entries in the table before inserting new ones
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Insert the fetched data into the Treeview
            for row in data:
                self.tree.insert("", "end", values=row)

            # Resize columns to fit content
            self.resize_columns()

            cursor.close()
            conn.close()

        except Error as e:
            messagebox.showerror("Error", f"Error fetching revenue data: {e}")

    def resize_columns(self):
        """ Resize the columns based on the longest value in each column """
        for col in self.columns:
            max_length = 0
            # Check all rows for the maximum length
            for row in self.tree.get_children():
                item = self.tree.item(row)
                max_length = max(max_length, len(str(item['values'][self.columns.index(col)])))
            # Add some padding to the width
            self.tree.column(col, width=max_length * 10)

if __name__ == "__main__":
    root = tk.Tk()
    app = RevenueScreen(root, "aloha", None)  # Replace "aloha" with the actual store name
    root.mainloop()
