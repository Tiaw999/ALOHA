# withdrawals_screen.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import get_connection

class WithdrawalsScreen(tk.Frame):
    def __init__(self, master, store_name, previous_screen, selected_month=None, selected_year=None):
        super().__init__(master)
        self.columns = ("ID", "Date", "Employee", "Amount", "Notes")
        self.master = master
        self.store_name = store_name
        self.previous_screen = previous_screen

        # Default selected_month and selected_year if not passed
        if selected_month is None or selected_year is None:
            self.selected_month = datetime.now().month
            self.selected_year = datetime.now().year
        else:
            self.selected_month = selected_month
            self.selected_year = selected_year

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

        # Withdrawals Label/Button (for visual consistency)
        withdrawals_label = ttk.Label(self, text="Withdrawals", font=("Arial", 14))
        withdrawals_label.grid(row=1, column=1, padx=10, pady=5)

        # Table (Treeview)
        columns = ("ID", "Date", "Employee", "Amount", "Notes")
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

        # Adding gap below row buttons
        gap_row += 1

        # Date Filter Inputs (moved below row buttons, adjusted to be more compact horizontally)
        tk.Label(self, text="Start Date (YYYY-MM-DD):").grid(row=gap_row, column=0, padx=1, pady=1, sticky="e")
        self.start_date_entry = tk.Entry(self, width=12)  # Reduced width for better fitting
        self.start_date_entry.grid(row=gap_row, column=1, padx=1, pady=2)

        tk.Label(self, text="End Date (YYYY-MM-DD):").grid(row=gap_row, column=2, padx=1, pady=1, sticky="e")
        self.end_date_entry = tk.Entry(self, width=12)  # Reduced width for better fitting
        self.end_date_entry.grid(row=gap_row, column=3, padx=1, pady=2)

        # Filter and Clear Filter Buttons (placed after the date filter inputs, more compact)
        filter_btn = ttk.Button(self, text="Filter", command=self.filter_by_date)
        filter_btn.grid(row=gap_row, column=4, padx=5, pady=5)

        clear_filter_btn = ttk.Button(self, text="Clear Filter", command=self.clear_filter)
        clear_filter_btn.grid(row=gap_row, column=5, padx=5, pady=5)

    def add_row(self):
        """ Open a pop-up window to add a new withdrawal entry """
        add_window = tk.Toplevel(self)
        add_window.title("Add Withdrawal Entry")
        add_window.geometry("300x300")

        tk.Label(add_window, text="Date (YYYY-MM-DD):").pack(pady=2)
        date_entry = tk.Entry(add_window)
        date_entry.pack(pady=2)

        tk.Label(add_window, text="Employee Name:").pack(pady=2)
        empname_entry = tk.Entry(add_window)
        empname_entry.pack(pady=2)

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
            empname_value = empname_entry.get()
            amount_value = amount_entry.get()
            notes_value = notes_entry.get()

            # Validate date format
            try:
                date = datetime.strptime(date_value, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Date Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            # Validate amount (must be a valid decimal)
            try:
                amount = float(amount_value)
            except ValueError:
                messagebox.showerror("Amount Error", "Amount must be a valid number.")
                return

            # Validate employee name
            if not empname_value:
                messagebox.showerror("Input Error", "Employee name is required.")
                return

            # Save the withdrawal to the database
            try:
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO withdrawals (storename, empname, amount, notes, date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (self.store_name, empname_value, amount, notes_value, date))

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
        self.open_edit_dialog(selected_item, row_values)
