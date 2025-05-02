# revenue_screen.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import get_connection

class RevenueScreen(tk.Frame):
    def __init__(self, master, store_name, user, previous_screen, selected_month=None, selected_year=None):
        super().__init__(master)
        self.columns = ("ID", "Date", "Reg", "Credit", "Cash in Envelope")
        self.master = master
        self.store_name = store_name
        self.user = user
        self.previous_screen = previous_screen
        # Default selected_month and selected_year if not passed (for Manager)
        if selected_month is None or selected_year is None:
            self.selected_month = datetime.now().month
            self.selected_year = datetime.now().year
        else:
            self.selected_month = selected_month
            self.selected_year = selected_year
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


        # Table (Treeview)
        columns = ("ID", "Date", "Reg", "Credit", "Cash in Envelope")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

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
        """ Open a pop-up window to add a new revenue row """
        add_window = tk.Toplevel(self)
        add_window.title("Add Revenue Entry")
        add_window.geometry("300x260")

        tk.Label(add_window, text="Date (YYYY-MM-DD):").pack(pady=2)
        date_entry = tk.Entry(add_window)
        date_entry.pack(pady=2)

        tk.Label(add_window, text="Reg:").pack(pady=2)
        reg_entry = tk.Entry(add_window)
        reg_entry.pack(pady=2)

        tk.Label(add_window, text="Credit:").pack(pady=2)
        credit_entry = tk.Entry(add_window)
        credit_entry.pack(pady=2)

        tk.Label(add_window, text="Cash in Envelope:").pack(pady=2)
        cash_entry = tk.Entry(add_window)
        cash_entry.pack(pady=2)

        def save_entry():
            """ Save data and close window """
            date_str = date_entry.get().strip()
            reg = reg_entry.get().strip()
            credit = credit_entry.get().strip()
            cash_in_envelope = cash_entry.get().strip()

            if not date_str or not reg or not credit or not cash_in_envelope:
                messagebox.showwarning("Input Error", "All fields are required.")
                return

            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()

                # Check if the entered date is within the selected month and year
                if date.month != self.selected_month or date.year != self.selected_year:
                    messagebox.showerror("Date Error",
                                         f"Please enter a date within {self.selected_month}/{self.selected_year}.")
                    return

            except ValueError:
                messagebox.showerror("Date Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            try:
                float(reg)
                float(credit)
                float(cash_in_envelope)
            except ValueError:
                messagebox.showerror("Input Error", "Reg, Credit, and Cash in Envelope must be numbers.")
                return

            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO revenue (storename, reg, credit, cashinenvelope, date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (self.store_name, reg, credit, cash_in_envelope, date))
                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "New revenue record added successfully!")
                self.fetch_revenue_data()  # Refresh table
                add_window.destroy()  # Close window after saving

            except Error as e:
                messagebox.showerror("Error", f"Error adding revenue data: {e}")

        save_btn = tk.Button(add_window, text="Save", command=save_entry)
        save_btn.pack(pady=10)

        add_window.grab_set()  # Make window modal (prevents interaction with main window)

    # Delete Row Function
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
                # Delete the row with the corresponding ID
                cursor.execute("DELETE FROM revenue WHERE id = %s", (row_id,))
                conn.commit()

                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "Row deleted successfully!")
                self.fetch_revenue_data()  # Refresh table
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
        self.open_edit_dialog(row_values)

    def open_edit_dialog(self, row_values):
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Revenue Entry")

        labels = ["Date (YYYY-MM-DD)", "Reg", "Credit", "Cash in Envelope"]
        entries = []

        # We skip the first value (id) and assign remaining values to the fields
        for i, (label_text, value) in enumerate(zip(labels, row_values[1:])):  # Skip the first value (ID)
            tk.Label(edit_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(edit_window)
            # If it's the date (i == 0), format it
            if i == 0:
                value = value.split(" ")[0]  # handle "YYYY-MM-DD 00:00:00"
            entry.insert (0, value)  # Pre-fill with existing data
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        # Save button
        def save_changes():
            new_values = [entry.get() for entry in entries]

            # Debugging: Print the date value from the entry
            print(f"Date value entered: {new_values[0]}")

            # === Validate Date Format ===
            try:
                date = datetime.strptime(new_values[0], "%Y-%m-%d").date()

                # Check if the entered date is within the selected month and year
                if date.month != self.selected_month or date.year != self.selected_year:
                    messagebox.showerror("Date Error",
                                         f"Please enter a date within {self.selected_month}/{self.selected_year}.")
                    return

            except ValueError:
                messagebox.showerror("Date Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            # === Validate Decimal Fields ===
            for field_value, field_name in zip(new_values[1:], ["Reg", "Credit", "Cash in Envelope"]):
                try:
                    float(field_value)
                except ValueError:
                    messagebox.showerror("Input Error", f"{field_name} must be a number.")
                    return

            # If all validations pass, update the database
            self.update_revenue_data(row_values[0], new_values)
            edit_window.destroy()

        save_button = ttk.Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=len(labels), columnspan=2, pady=10)

    def update_revenue_data(self, record_id, new_values):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE revenue 
                SET date = %s, reg = %s, credit = %s, cashinenvelope = %s 
                WHERE id = %s
            """, (*new_values, record_id))

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Revenue record updated successfully!")
            self.fetch_revenue_data()  # Refresh table

        except Error as e:
            messagebox.showerror("Error", f"Error updating revenue data: {e}")

    def get_selected_month_year(self):
        return self.selected_month, self.selected_year

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name, self.user)

    def fetch_revenue_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Debug print to verify selected_month and selected_year
            print(f"Fetching data for Month: {self.selected_month}, Year: {self.selected_year}")

            # Base query to fetch revenue data for the store
            query = """
                SELECT id, date, reg, credit, cashinenvelope 
                FROM revenue 
                WHERE storename = %s
                AND MONTH(date) = %s AND YEAR(date) = %s
                ORDER BY date DESC
            """
            query_params = [self.store_name, self.selected_month, self.selected_year]

            # Execute the query with parameters
            cursor.execute(query, tuple(query_params))
            data = cursor.fetchall()

            # Debug print to check fetched data
            print(f"Fetched Data: {data}")

            if not data:
                print("No data found for the given month/year.")

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
                SELECT id, date, reg, credit, cashinenvelope 
                FROM revenue 
                WHERE storename = %s AND date BETWEEN %s AND %s
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
            messagebox.showerror("Error", f"Error filtering revenue data: {e}")

    def clear_filter(self):
        """ Reset the table to show all data """
        # Clear the date entry fields
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.fetch_revenue_data()  # Fetches and displays all revenue data
        messagebox.showinfo("Filter Cleared", "All revenue data will now be displayed.")
