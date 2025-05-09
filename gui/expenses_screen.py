# expenses_screen.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import get_connection
from mysql.connector import Error


class ExpensesScreen(tk.Frame):
    def __init__(self, master, store_name, user, previous_screen, selected_month=None, selected_year=None):
        super().__init__(master)
        self.columns = ("ID", "Date", "Expense Type", "Expense Value")
        self.master = master
        self.store_name = store_name
        self.user = user
        self.previous_screen = previous_screen

        # Default to current month/year if not provided
        if selected_month is None or selected_year is None:
            self.selected_month = datetime.now().month
            self.selected_year = datetime.now().year
        else:
            self.selected_month = selected_month
            self.selected_year = selected_year

        self.master.geometry("900x600")
        self.master.title("Expenses")
        self.create_widgets()
        self.fetch_expense_data()


    def create_widgets(self):
        # Store Name Label
        store_label = ttk.Label(self, text=f"Expenses - {self.store_name}", font=("Arial", 18, "bold"))
        store_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Back Button
        back_button = ttk.Button(self, text="<- Back", command=self.go_back)
        back_button.grid(row=1, column=0, padx=10, pady=5, sticky="w")


        # Table (Treeview)
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, width=150, anchor="w")

        self.tree.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Row for the buttons
        gap_row = 3
        edit_btn = ttk.Button(self, text="Edit Row", command=self.edit_row)
        edit_btn.grid(row=gap_row, column=0, pady=5)

        add_row_btn = ttk.Button(self, text="Add Row", command=self.add_row)
        add_row_btn.grid(row=gap_row, column=1, pady=5)

        delete_button = ttk.Button(self, text="Delete Row", command=self.delete_row)
        delete_button.grid(row=gap_row, column=2, padx=10, pady=5, sticky="w")

        # Date Filter Inputs
        gap_row += 1
        tk.Label(self, text="Start Date (YYYY-MM-DD):").grid(row=gap_row, column=0, padx=1, pady=1, sticky="e")
        self.start_date_entry = tk.Entry(self, width=12)
        self.start_date_entry.grid(row=gap_row, column=1, padx=1, pady=2)

        tk.Label(self, text="End Date (YYYY-MM-DD):").grid(row=gap_row, column=2, padx=1, pady=1, sticky="e")
        self.end_date_entry = tk.Entry(self, width=12)
        self.end_date_entry.grid(row=gap_row, column=3, padx=1, pady=2)

        # Filter and Clear Buttons
        filter_btn = ttk.Button(self, text="Filter", command=self.filter_by_date)
        filter_btn.grid(row=gap_row, column=4, padx=5, pady=5)

        clear_filter_btn = ttk.Button(self, text="Clear Filter", command=self.clear_filter)
        clear_filter_btn.grid(row=gap_row, column=5, padx=5, pady=5)

    def add_row(self):
        """ Open a pop-up window to add a new expense row """
        add_window = tk.Toplevel(self)
        add_window.title("Add Expense Entry")
        add_window.geometry("380x180")

        form_frame = tk.Frame(add_window)
        form_frame.pack(padx=10, pady=10)

        # Date field
        tk.Label(form_frame, text="Date (YYYY-MM-DD)").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        date_entry = tk.Entry(form_frame)
        date_entry.grid(row=0, column=1, padx=10, pady=5)

        # Expense Type field
        tk.Label(form_frame, text="Expense Type").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        type_entry = tk.Entry(form_frame)
        type_entry.grid(row=1, column=1, padx=10, pady=5)

        # Expense Value field
        tk.Label(form_frame, text="Expense Value").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        value_entry = tk.Entry(form_frame)
        value_entry.grid(row=2, column=1, padx=10, pady=5)

        # Save button
        save_button = ttk.Button(form_frame, text="Save Expense", command=lambda: save_entry())
        save_button.grid(row=3, columnspan=2, pady=10)

        add_window.grab_set()  # Make the window modal

        def save_entry():
            """ Save data and close window """
            date_str = date_entry.get().strip()
            expensetype = type_entry.get().strip()
            expensevalue = value_entry.get().strip()

            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if date.month != self.selected_month or date.year != self.selected_year:
                    messagebox.showerror("Date Error",
                                         f"Please enter a date within {self.selected_month}/{self.selected_year}.")
                    return
            except ValueError:
                messagebox.showerror("Date Error", "Invalid date format. Please use YYYY-MM-DD.")
                return

            conn = None
            cursor = None
            try:
                conn = get_connection()
                cursor = conn.cursor()
                conn.start_transaction()

                cursor.execute("""
                    CALL insert_expense(%s, %s, %s, %s);
                """, (self.store_name, expensetype, expensevalue, date))

                conn.commit()
                messagebox.showinfo("Success", "New expense record added successfully!")
                add_window.destroy()
                self.fetch_expense_data()
            except Error as e:
                if conn:
                    conn.rollback()
                messagebox.showerror("Error", f"Error adding expense data: {e}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

    def delete_row(self):
        """ Deletes a selected expense row from the Treeview and the database """
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a row to delete.")
            return

        row_id = self.tree.item(selected_item, "values")[0]

        confirm = messagebox.askyesno("Confirm Deletion",
                                      f"Are you sure you want to delete the expense record with ID {row_id}?")

        if confirm:
            conn = None
            cursor = None
            try:
                conn = get_connection()
                cursor = conn.cursor()
                conn.start_transaction()

                cursor.execute("DELETE FROM expenses WHERE id = %s", (row_id,))

                conn.commit()
                messagebox.showinfo("Success", "Expense record deleted successfully!")
                self.fetch_expense_data()
            except Error as e:
                if conn:
                    conn.rollback()
                messagebox.showerror("Error", f"Failed to delete expense record: {e}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

    def edit_row(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a row to edit.")
            return

        # Get the current values of the selected expense row
        row_values = self.tree.item(selected_item, "values")

        # Open the edit dialog for expenses
        self.open_edit_dialog(selected_item, row_values)

    def open_edit_dialog(self, item_id, row_values):
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Expense Entry")

        labels = ["Date (YYYY-MM-DD)", "Expense Type", "Expense Value"]
        entries = []

        # We skip the first value (id) and assign remaining values to the fields
        for i, (label_text, value) in enumerate(zip(labels, row_values[1:])):  # Skip the first value (ID)
            tk.Label(edit_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(edit_window)
            # If it's the date (i == 0), format it
            if i == 0:
                value = value.split(" ")[0]  # handle "YYYY-MM-DD 00:00:00"
            entry.insert(0, value)  # Pre-fill with existing data
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

            # If all validations pass, update the database
            self.update_expense_data(row_values[0], new_values, edit_window)

        save_button = ttk.Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=len(labels), columnspan=2, pady=10)

    from mysql.connector import Error  # Ensure this is imported

    def update_expense_data(self, record_id, new_values, edit_window):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            conn.start_transaction()

            cursor.execute("""
                CALL update_expense(%s, %s, %s, %s)
            """, (record_id, *new_values))

            conn.commit()

            messagebox.showinfo("Success", "Expense record updated successfully!")
            edit_window.destroy()
            self.fetch_expense_data()

        except Error as e:
            if conn:
                conn.rollback()
            messagebox.showerror("Error", f"Error updating expense data: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_selected_month_year(self):
        return self.selected_month, self.selected_year

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name, self.user)

    def fetch_expense_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Debug print to verify selected_month and selected_year
            print(f"Fetching expense data for Month: {self.selected_month}, Year: {self.selected_year}")

            # Base query to fetch expense data for the store
            query = """
                SELECT id, date, expensetype, expensevalue
                FROM expenses
                WHERE storename = %s
                AND MONTH(date) = %s AND YEAR(date) = %s
                ORDER BY date DESC
            """
            query_params = [self.store_name, self.selected_month, self.selected_year]

            # Execute the query with parameters
            cursor.execute(query, tuple(query_params))
            data = cursor.fetchall()

            # Debug print to check fetched data
            print(f"Fetched Expense Data: {data}")

            if not data:
                print("No expenses found for the given month/year.")

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
            print(f"Error fetching expense data: {e}")

    def resize_columns(self):
        min_width = 80  # Minimum width to ensure headers aren't cut off

        for i, col in enumerate(self.columns):
            # Start by setting the column width based on the header's length
            max_length = len(self.tree.heading(col)["text"])  # Get the header length

            # Measure content length for each row
            for item in self.tree.get_children():
                value = self.tree.item(item)["values"][i]
                max_length = max(max_length, len(str(value)))  # Take the longest value

            # Set column width based on the longest content, but ensuring a minimum width
            self.tree.column(col, width=max(min_width, max_length * 10))  # Adjust multiplier if needed

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

            # Modify query to filter by date for expenses
            cursor.execute("""
                SELECT id, date, expensetype, expensevalue 
                FROM expenses 
                WHERE storename = %s AND date BETWEEN %s AND %s
            """, (self.store_name, start_date, end_date))

            data = cursor.fetchall()

            # Clear table before adding filtered data
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Insert filtered data into the table
            for row in data:
                self.tree.insert("", "end", values=row)

            cursor.close()
            conn.close()

        except Error as e:
            messagebox.showerror("Error", f"Error filtering expense data: {e}")

    def clear_filter(self):
        """ Reset the table to show all expenses data """
        # Clear the date entry fields
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)

        # Fetch and display all expense data
        self.fetch_expense_data()  # This will fetch and display all expense data from the database

        messagebox.showinfo("Filter Cleared", "All expense data will now be displayed.")


