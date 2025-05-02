# withdrawals_screen.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import get_connection
from mysql.connector import Error

class WithdrawalsScreen(tk.Frame):
    def __init__(self, master, store_name, user, previous_screen, selected_month=None, selected_year=None, owner_name = None):
        super().__init__(master)
        self.columns = ("ID", "Employee Name", "Date", "Amount", "Notes")
        self.master = master
        self.store_name = store_name
        self.user = user
        self.previous_screen = previous_screen

        # Default selected_month and selected_year if not passed
        if selected_month is None or selected_year is None:
            self.selected_month = datetime.now().month
            self.selected_year = datetime.now().year
        else:
            self.selected_month = selected_month
            self.selected_year = selected_year
        self.owner_name = owner_name
        self.master.geometry("900x600")
        self.master.title("Withdrawals")
        self.create_widgets()
        self.fetch_withdrawal_data()

    def create_widgets(self):
        # Store Name Label
        store_label = ttk.Label(self, text=f"Withdrawals - {self.store_name}", font=("Arial", 18, "bold"))
        store_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Back Button
        back_button = ttk.Button(self, text="<- Back", command=self.go_back)
        back_button.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Table (Treeview)
        columns = ("ID", "Employee Name", "Date", "Amount", "Notes")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col, anchor="w")  # 'w' stands for "west" which aligns to the left
            self.tree.column(col, width=120, anchor="w")  # Ensures the column values are also left-aligned

        self.tree.grid(row=2, column=0, columnspan=6, padx=10, pady=10)

        # Row for the buttons (edit table, add row, delete row)
        gap_row = 3  # The row after the table for buttons
        edit_btn = ttk.Button(self, text="Edit Row", command=self.edit_row)
        edit_btn.grid(row=gap_row, column=0, pady=5)

        add_row_btn = ttk.Button(self, text="Add Row", command=self.add_row)
        add_row_btn.grid(row=gap_row, column=1, pady=5)

        delete_button = ttk.Button(self, text="Delete Row", command=self.delete_row)
        delete_button.grid(row=gap_row, column=2, padx=10, pady=5, sticky="w")

    def add_row(self):
        """ Open a pop-up window to add a new withdrawal entry """
        add_window = tk.Toplevel(self)
        add_window.title("Add Withdrawal Entry")
        add_window.geometry("300x220")

        tk.Label(add_window, text="Date (YYYY-MM-DD):").pack(pady=2)
        date_entry = tk.Entry(add_window)
        date_entry.pack(pady=2)

        tk.Label(add_window, text="Amount:").pack(pady=2)
        amount_entry = tk.Entry(add_window)
        amount_entry.pack(pady=2)

        tk.Label(add_window, text="Notes:").pack(pady=2)
        notes_entry = tk.Entry(add_window)
        notes_entry.pack(pady=2)

        # Save Button
        def save_entry():
            # Get the values entered by the user
            date_value = date_entry.get()
            amount_value = amount_entry.get()
            notes_value = notes_entry.get()

            # Validate date format
            try:
                date = datetime.strptime(date_value, "%Y-%m-%d").date()
                # Check if the entered date is within the selected month and year
                if date.month != self.selected_month or date.year != self.selected_year:
                    messagebox.showerror("Date Error",
                                         f"Please enter a date within {self.selected_month}/{self.selected_year}.")
                    return
            except ValueError:
                messagebox.showerror("Date Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            # Validate amount (must be a valid decimal)
            try:
                amount = float(amount_value)
            except ValueError:
                messagebox.showerror("Amount Error", "Amount must be a valid number.")
                return

            # Save the withdrawal to the database
            try:
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO withdrawals (storename, empname, amount, notes, date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (self.store_name, self.user, amount, notes_value, date))

                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "Withdrawal entry added successfully!")
                self.fetch_withdrawal_data()  # Refresh table with new data
                add_window.destroy()  # Close the add window

            except Exception as e:
                messagebox.showerror("Database Error", f"Error saving withdrawal entry: {e}")

        save_button = ttk.Button(add_window, text="Save", command=save_entry)
        save_button.pack(pady=10)

    def delete_row(self):
        """ Deletes a selected row from the Treeview and the database """
        selected_item = self.tree.selection()  # Get the selected item

        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a row to delete.")
            return

        # Get the ID of the selected row (assuming ID is in the first column)
        row_id = self.tree.item(selected_item, "values")[0]  # Assuming ID is the first value in the row

        # Confirm the deletion with the user
        confirm = messagebox.askyesno("Confirm Deletion",
                                      f"Are you sure you want to delete the withdrawal record with ID {row_id}?")

        if confirm:
            try:
                conn = get_connection()
                cursor = conn.cursor()

                # Delete the row with the corresponding ID from the withdrawals table
                cursor.execute("DELETE FROM withdrawals WHERE id = %s", (row_id,))
                conn.commit()

                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "Withdrawal entry deleted successfully!")
                self.fetch_withdrawal_data()  # Refresh table with updated data
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete withdrawal entry: {e}")

    def edit_row(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a row to edit.")
            return

        # Get the current values of the selected row
        row_values = self.tree.item(selected_item, "values")

        # Open the edit dialog
        self.open_edit_dialog(row_values)

    def open_edit_dialog(self, row_values):
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Withdrawal Entry")

        labels = ["Date (YYYY-MM-DD)", "Amount", "Notes"]
        entries = []

        for i, (label_text, value) in enumerate(zip(labels, row_values[2:])):  # Skip ID (row_values[0])
            tk.Label(edit_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(edit_window)

            if label_text == "Date (YYYY-MM-DD)":
                value = value.split(" ")[0]  # Trims time if present

            entry.insert(0, value)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        def save_changes():
            new_values = [entry.get() for entry in entries]

            # Validate date format
            try:
                date = datetime.strptime(new_values[0], "%Y-%m-%d").date()
                if date.month != self.selected_month or date.year != self.selected_year:
                    messagebox.showerror("Date Error",
                                         f"Please enter a date within {self.selected_month}/{self.selected_year}.")
                    return
            except ValueError:
                messagebox.showerror("Date Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            # Validate amount
            try:
                float(new_values[1])  # Amount
            except ValueError:
                messagebox.showerror("Input Error", "Amount must be a number.")
                return

            self.update_withdrawal_data(row_values[0], new_values)
            edit_window.destroy()

        save_button = ttk.Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=len(labels), columnspan=2, pady=10)

    def update_withdrawal_data(self, record_id, new_values):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE withdrawals
                SET date = %s, amount = %s, notes = %s
                WHERE id = %s
            """, (*new_values, record_id))

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Withdrawal record updated successfully!")
            self.fetch_withdrawal_data()  # Refresh table

        except Error as e:
            messagebox.showerror("Error", f"Error updating withdrawal data: {e}")

    def get_selected_month_year(self):
        return self.selected_month, self.selected_year

    def get_owner_name(self):
        return self.owner_name

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name, self.user)

    def fetch_withdrawal_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Debug print to verify selected_month and selected_year
            print(f"Fetching data for Month: {self.selected_month}, Year: {self.selected_year}")

            # Query to fetch withdrawals for the current store and selected month/year
            query = """
                SELECT id, empname, date, amount, notes
                FROM withdrawals
                WHERE storename = %s
                AND MONTH(date) = %s AND YEAR(date) = %s
                ORDER BY date DESC
            """
            query_params = [self.store_name, self.selected_month, self.selected_year]

            cursor.execute(query, tuple(query_params))
            data = cursor.fetchall()

            print(f"Fetched Data: {data}")

            if not data:
                print("No withdrawal data found for the given month/year.")

            # Clear existing entries in the tree
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Insert the new data
            for row in data:
                self.tree.insert("", "end", values=row)

            self.resize_columns()

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error fetching withdrawal data: {e}")

    def resize_columns(self):
        min_width = 80  # Minimum width for each column to ensure header is visible

        for i, col in enumerate(self.columns):
            # Start with the length of the column header
            max_length = len(col)

            # Calculate the max content length for each column
            for item in self.tree.get_children():
                value = self.tree.item(item)["values"][i]
                max_length = max(max_length, len(str(value)))

            # Adjust the column width dynamically based on content length, adding extra space for padding
            self.tree.column(col, width=max(min_width, max_length * 10))

            # Optionally, make sure the header fits as well
            header = self.tree.heading(col)["text"]
            header_length = len(header)
            self.tree.column(col, width=max(self.tree.column(col)["width"], header_length * 10))





