# payroll_screen.py
# payroll_screen.py
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import get_connection

class PayrollScreen(tk.Frame):
    def __init__(self, master, store_name, previous_screen, selected_month=None, selected_year=None):
        super().__init__(master)
        self.columns = ("ID", "Employee Name", "Store", "Regular Pay", "Bonus", "Pay Date")
        self.master = master
        self.store_name = store_name
        self.previous_screen = previous_screen

        if selected_month is None or selected_year is None:
            self.selected_month = datetime.now().month
            self.selected_year = datetime.now().year
        else:
            self.selected_month = selected_month
            self.selected_year = selected_year

        self.master.geometry("900x600")
        self.master.title("Payroll")
        self.create_widgets()
        self.fetch_payroll_data()

    def create_widgets(self):
        # Store Name Label
        store_label = ttk.Label(self, text=f"Payroll - {self.store_name}", font=("Arial", 18, "bold"))
        store_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Back Button
        back_button = ttk.Button(self, text="<- Back", command=self.go_back)
        back_button.grid(row=1, column=0, padx=10, pady=5, sticky="w")


        # Table (Treeview)
        self.columns = ("ID", "Employee Name", "Store", "Regular Pay", "Bonus", "Pay Date")
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col, anchor="w")  # 'w' stands for "west" which aligns to the left
            self.tree.column(col, width=120, anchor="w")  # Ensures the column values are also left-aligned

        self.tree.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

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
        # Create a modal window for adding payroll data
        add_window = tk.Toplevel(self)  # Create a new window (modal)
        add_window.title("Add Payroll Entry")

        # Create form frame inside the new window
        self.form_frame = tk.Frame(add_window)
        self.form_frame.pack(pady=10)

        # Fetch employee names from the database for the dropdown
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM staff WHERE storename = %s", (self.store_name,))
            employee_names = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()

            if not employee_names:
                messagebox.showwarning("No Employees", "No employees found for this store.")
                return
        except Error as e:
            messagebox.showerror("Error", f"Error fetching employees: {e}")
            return
        # Sort employee names alphabetically
        employee_names.sort()

        # Employee Name dropdown
        tk.Label(self.form_frame, text="Employee Name").grid(row=0, column=0, padx=10, pady=5)
        self.empname_var = tk.StringVar()  # Variable to store selected employee name
        self.empname_dropdown = ttk.Combobox(self.form_frame, textvariable=self.empname_var, values=employee_names)
        self.empname_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # Regular Pay field
        tk.Label(self.form_frame, text="Regular Pay").grid(row=1, column=0, padx=10, pady=5)
        self.regularpay_entry = tk.Entry(self.form_frame)
        self.regularpay_entry.grid(row=1, column=1, padx=10, pady=5)

        # Bonus field
        tk.Label(self.form_frame, text="Bonus").grid(row=2, column=0, padx=10, pady=5)
        self.bonus_entry = tk.Entry(self.form_frame)
        self.bonus_entry.grid(row=2, column=1, padx=10, pady=5)

        # Pay Date field
        tk.Label(self.form_frame, text="Pay Date (YYYY-MM-DD)").grid(row=3, column=0, padx=10, pady=5)
        self.paydate_entry = tk.Entry(self.form_frame)
        self.paydate_entry.grid(row=3, column=1, padx=10, pady=5)

        # Save button
        save_button = ttk.Button(self.form_frame, text="Save Entry", command=lambda: self.save_entry(add_window))
        save_button.grid(row=4, columnspan=2, pady=10)

        # Make the new window modal
        add_window.grab_set()  # Prevent interaction with the main window until this window is closed

    def save_entry(self, add_window):
        """ Save data and close window """
        empname = self.empname_var.get().strip()
        regularpay = self.regularpay_entry.get().strip()
        bonus = self.bonus_entry.get().strip()
        paydate_str = self.paydate_entry.get().strip()

        # Validate inputs
        if not empname or not regularpay or not bonus or not paydate_str:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        try:
            paydate = datetime.strptime(paydate_str, "%Y-%m-%d").date()
            # Check if the entered date is within the selected month and year
            if paydate.month != self.selected_month or paydate.year != self.selected_year:
                messagebox.showerror("Date Error",
                                     f"Please enter a date within {self.selected_month}/{self.selected_year}.")
                return
        except ValueError:
            messagebox.showerror("Date Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        try:
            float(regularpay)
            float(bonus)
        except ValueError:
            messagebox.showerror("Input Error", "Regular Pay and Bonus must be numbers.")
            return

        # Attempt to save to database
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO payroll (empname, storename, regularpay, bonus, paydate)
                VALUES (%s, %s, %s, %s, %s)
            """, (empname, self.store_name, regularpay, bonus, paydate))
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "New payroll record added successfully!")
            self.fetch_payroll_data()  # Refresh table
            add_window.destroy()  # Close the modal window after saving

        except Error as e:
            messagebox.showerror("Error", f"Error adding payroll data: {e}")

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
                                      f"Are you sure you want to delete the record with ID {row_id}?")

        if confirm:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                # Delete the row with the corresponding ID from the payroll table
                cursor.execute("DELETE FROM payroll WHERE id = %s", (row_id,))
                conn.commit()

                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "Row deleted successfully!")
                self.fetch_payroll_data()  # Refresh table
            except Error as e:
                messagebox.showerror("Error", f"Failed to delete row: {e}")

    def edit_row(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a row to edit.")
            return

        # Get the current values of the selected row
        row_values = self.tree.item(selected_item, "values")

        # Open the edit dialog
        self.open_edit_dialog(selected_item, row_values)

    def open_edit_dialog(self, item_id, row_values):
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Payroll Entry")

        labels = ["Employee Name", "Store Name", "Regular Pay", "Bonus", "Pay Date"]
        entries = []

        # Create form frame inside the new window
        self.form_frame = tk.Frame(edit_window)
        self.form_frame.pack(pady=10)

        # Fetch employee names from the database for the dropdown
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM staff WHERE storename = %s", (self.store_name,))
            employee_names = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()

            if not employee_names:
                messagebox.showwarning("No Employees", "No employees found for this store.")
                return
        except Error as e:
            messagebox.showerror("Error", f"Error fetching employees: {e}")
            return

        # Sort employee names alphabetically
        employee_names.sort()
        # Set default employee name (this is based on row_values)
        employee_name = row_values[1]  # Assuming employee name is in index 1 of row_values

        # Employee Name dropdown
        tk.Label(self.form_frame, text="Employee Name").grid(row=0, column=0, padx=10, pady=5)
        self.empname_var = tk.StringVar()  # Variable to store selected employee name
        self.empname_dropdown = ttk.Combobox(self.form_frame, textvariable=self.empname_var, values=employee_names)
        self.empname_dropdown.set(employee_name)  # Set current employee name from row_values
        self.empname_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # Loop through the rest of the fields
        for i, (label_text, value) in enumerate(
                zip(labels[1:], row_values[2:])):  # Skip the first value (ID and Employee)
            tk.Label(self.form_frame, text=label_text).grid(row=i + 1, column=0, padx=10, pady=5)
            entry = tk.Entry(self.form_frame)

            # If it's the pay date (i == 4), format it
            if i == 3:  # Pay date is at index 3 in labels
                value = value.split(" ")[0]  # Handle "YYYY-MM-DD 00:00:00"

            entry.insert(0, value)  # Pre-fill with existing data
            entry.grid(row=i + 1, column=1, padx=10, pady=5)
            entries.append(entry)

        # Save button
        save_button = ttk.Button(self.form_frame, text="Save Entry",
                                 command=lambda: self.save_edited_entry(item_id, entries))
        save_button.grid(row=len(labels), columnspan=2, pady=10)

        edit_window.grab_set()  # Make window modal

        # Save button
        def save_changes():
            new_values = [entry.get() for entry in entries]

            # === Validate Input Fields ===
            for field_value, field_name in zip(new_values[:4], ["Employee Name", "Store Name", "Regular Pay", "Bonus"]):
                if not field_value.strip():
                    messagebox.showwarning("Input Error", f"{field_name} is required.")
                    return

            try:
                # Validate Pay Date
                paydate = datetime.strptime(new_values[4], "%Y-%m-%d").date()
                # Check if the entered date is within the selected month and year
                if paydate.month != self.selected_month or paydate.year != self.selected_year:
                    messagebox.showerror("Date Error",
                                         f"Please enter a date within {self.selected_month}/{self.selected_year}.")
            except ValueError:
                messagebox.showerror("Date Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            try:
                # Validate Regular Pay and Bonus as numbers
                float(new_values[2])  # Regular Pay
                float(new_values[3])  # Bonus
            except ValueError:
                messagebox.showerror("Input Error", "Regular Pay and Bonus must be valid numbers.")
                return

            # If all validations pass, update the database
            self.update_payroll_data(item_id, new_values)
            edit_window.destroy()

        save_button = ttk.Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=len(labels), columnspan=2, pady=10)

    def update_payroll_data(self, record_id, new_values):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE payroll 
                SET empname = %s, storename = %s, regularpay = %s, bonus = %s, paydate = %s
                WHERE id = %s
            """, (*new_values, record_id))

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Payroll record updated successfully!")
            self.fetch_payroll_data()  # Refresh table with updated data

        except Error as e:
            messagebox.showerror("Error", f"Error updating payroll data: {e}")

    def get_selected_month_year(self):
        return self.selected_month, self.selected_year

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name)

    def fetch_payroll_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Debug print to verify selected_month and selected_year
            print(f"Fetching data for Month: {self.selected_month}, Year: {self.selected_year}")

            # Base query to fetch payroll data for the store and date
            query = """
                SELECT id, empname, storename, regularpay, bonus, paydate 
                FROM payroll 
                WHERE storename = %s
                AND MONTH(paydate) = %s AND YEAR(paydate) = %s
                ORDER BY paydate DESC
            """
            query_params = [self.store_name, self.selected_month, self.selected_year]

            # Execute the query with parameters
            cursor.execute(query, tuple(query_params))
            data = cursor.fetchall()

            # Debug print to check fetched data
            print(f"Fetched Data: {data}")

            if not data:
                print("No payroll data found for the given month/year.")

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
        except Exception as e:
            print(f"Error: {e}")

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

    def filter_by_date(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        if not start_date or not end_date:
            messagebox.showwarning("Input Error", "Please enter both start and end dates.")
            return

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Date Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, empname, storename, regularpay, bonus, paydate
                FROM payroll
                WHERE storename = %s AND paydate BETWEEN %s AND %s
            """, (self.store_name, start_date, end_date))

            data = cursor.fetchall()

            # Clear table before adding filtered data
            for row in self.tree.get_children():
                self.tree.delete(row)

            for row in data:
                self.tree.insert("", "end", values=row)

            cursor.close()
            conn.close()

        except Error as e:
            messagebox.showerror("Error", f"Error filtering payroll data: {e}")

    def clear_filter(self):
        """ Reset the table to show all payroll data """
        # Clear the date entry fields
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.fetch_payroll_data()  # Fetches and displays all payroll data
        messagebox.showinfo("Filter Cleared", "All payroll data will now be displayed.")
