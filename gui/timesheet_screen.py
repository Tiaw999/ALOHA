# timesheet_screen.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import get_connection

class TimesheetScreen(tk.Frame):
    def __init__(self, master, store_name, previous_screen, selected_month=None, selected_year=None):
        super().__init__(master)
        self.columns = ("ID", "Employee Name", "Clock In", "Clock Out", "Register In", "Register Out")
        self.master = master
        self.store_name = store_name
        self.previous_screen = previous_screen

        # Default selected_month and selected_year if not passed (for Manager)
        if selected_month is None or selected_year is None:
            self.selected_month = datetime.now().month
            self.selected_year = datetime.now().year
        else:
            self.selected_month = selected_month
            self.selected_year = selected_year

        self.master.geometry("900x600")
        self.master.title("Timesheet")
        self.create_widgets()
        self.fetch_timesheet_data()

    def create_widgets(self):
        # Store Name Label
        store_label = ttk.Label(self, text=f"Timesheet - {self.store_name}", font=("Arial", 18, "bold"))
        store_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Back Button
        back_button = ttk.Button(self, text="<- Back", command=self.go_back)
        back_button.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Timesheet Label
        timesheet_label = ttk.Label(self, text="Employee Timesheets", font=("Arial", 14))
        timesheet_label.grid(row=1, column=1, padx=10, pady=5)

        # Table (Treeview)
        self.columns = ("ID", "Employee Name", "Clock In", "Clock Out", "Register In", "Register Out")
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, width=140, anchor="w")

        self.tree.grid(row=2, column=0, columnspan=6, padx=10, pady=10)

        # Row for buttons
        gap_row = 3
        edit_btn = ttk.Button(self, text="Edit Row", command=self.edit_row)
        edit_btn.grid(row=gap_row, column=0, pady=5)

        add_row_btn = ttk.Button(self, text="Add Row", command=self.add_row)
        add_row_btn.grid(row=gap_row, column=1, pady=5)

        delete_button = ttk.Button(self, text="Delete Row", command=self.delete_row)
        delete_button.grid(row=gap_row, column=2, padx=10, pady=5, sticky="w")

        # Date filter section
        gap_row += 1
        tk.Label(self, text="Start Date (YYYY-MM-DD):").grid(row=gap_row, column=0, padx=1, pady=1, sticky="e")
        self.start_date_entry = tk.Entry(self, width=12)
        self.start_date_entry.grid(row=gap_row, column=1, padx=1, pady=2)

        tk.Label(self, text="End Date (YYYY-MM-DD):").grid(row=gap_row, column=2, padx=1, pady=1, sticky="e")
        self.end_date_entry = tk.Entry(self, width=12)
        self.end_date_entry.grid(row=gap_row, column=3, padx=1, pady=2)

        # Filter Buttons
        filter_btn = ttk.Button(self, text="Filter", command=self.filter_by_date)
        filter_btn.grid(row=gap_row, column=4, padx=5, pady=5)

        clear_filter_btn = ttk.Button(self, text="Clear Filter", command=self.clear_filter)
        clear_filter_btn.grid(row=gap_row, column=5, padx=5, pady=5)

    def add_row(self):
        """ Open a pop-up window to add a new timesheet entry """
        add_window = tk.Toplevel(self)
        add_window.title("Add Timesheet Entry")
        add_window.geometry("300x330")

        # Fetch employees for dropdown
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM staff WHERE storename = %s ORDER BY name", (self.store_name,))
            employee_names = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load employee list: {e}")
            return

        tk.Label(add_window, text="Employee:").pack(pady=2)
        employee_dropdown = ttk.Combobox(add_window, values=employee_names, state="readonly")
        employee_dropdown.pack(pady=2)

        # Clock In Entry
        tk.Label(add_window, text="Clock In (YYYY-MM-DD HH:MM:SS):").pack(pady=2)
        clock_in_entry = tk.Entry(add_window)
        clock_in_entry.pack(pady=2)

        # Clock Out Entry
        tk.Label(add_window, text="Clock Out (YYYY-MM-DD HH:MM:SS):").pack(pady=2)
        clock_out_entry = tk.Entry(add_window)
        clock_out_entry.pack(pady=2)

        # Register In Entry
        tk.Label(add_window, text="Register In:").pack(pady=2)
        regin_entry = tk.Entry(add_window)
        regin_entry.pack(pady=2)

        # Register Out Entry
        tk.Label(add_window, text="Register Out:").pack(pady=2)
        regout_entry = tk.Entry(add_window)
        regout_entry.pack(pady=2)

        def save_entry():
            """ Save data and close window """
            empname = employee_dropdown.get().strip()
            clock_in_str = clock_in_entry.get().strip()
            clock_out_str = clock_out_entry.get().strip()
            regin = regin_entry.get().strip()
            regout = regout_entry.get().strip()

            if not empname or not clock_in_str or not clock_out_str or not regin or not regout:
                messagebox.showwarning("Input Error", "All fields are required.")
                return

            # Validate datetime format for clock-in and clock-out
            try:
                clock_in = datetime.strptime(clock_in_str, "%Y-%m-%d %H:%M:%S")
                clock_out = datetime.strptime(clock_out_str, "%Y-%m-%d %H:%M:%S")
                # Check if the entered date is within the selected month and year
                if (clock_in.month != self.selected_month or clock_in.year != self.selected_year or clock_out.month != self.selected_month or clock_out.year != self.selected_year):
                    messagebox.showerror("Date Error",
                                         f"Please enter times within {self.selected_month}/{self.selected_year}.")
                    return
            except ValueError:
                messagebox.showerror("Date Error", "Invalid datetime format. Use YYYY-MM-DD HH:MM:SS.")
                return

            # Validate that Register In and Register Out are numeric
            try:
                float(regin)
                float(regout)
            except ValueError:
                messagebox.showerror("Input Error", "Register In and Register Out must be numbers.")
                return

            # Insert the data into the database
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO timesheet (storename, empname, clock_in, clock_out, regin, regout)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (self.store_name, empname, clock_in, clock_out, regin, regout))
                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "New timesheet entry added successfully!")
                self.fetch_timesheet_data()  # Refresh table
                add_window.destroy()  # Close window after saving

            except Error as e:
                messagebox.showerror("Error", f"Error adding timesheet data: {e}")

        save_btn = ttk.Button(add_window, text="Save", command=save_entry)
        save_btn.pack(pady=10)

        add_window.grab_set()  # Make window modal (prevents interaction with main window)

    # Delete Row Function
    def delete_row(self):
        """ Deletes a selected row from the Treeview and the database """
        selected_item = self.tree.selection()  # Get the selected item

        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a row to delete.")
            return

        # Get the ID of the selected row (assuming ID is the first value in the row)
        row_id = self.tree.item(selected_item, "values")[0]  # Assuming ID is the first value in the row

        # Confirm the deletion with the user
        confirm = messagebox.askyesno("Confirm Deletion",
                                      f"Are you sure you want to delete the record with ID {row_id}?")

        if confirm:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                # Delete the row with the corresponding ID from the timesheet table
                cursor.execute("DELETE FROM timesheet WHERE id = %s", (row_id,))
                conn.commit()

                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "Row deleted successfully!")
                self.fetch_timesheet_data()  # Refresh table
            except Error as e:
                messagebox.showerror("Error", f"Failed to delete row: {e}")

    def edit_row(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a row to edit.")
            return

        # Get the current values of the selected row
        row_values = self.tree.item(selected_item, "values")

        # Open the edit dialog and pass the selected item and its values
        self.open_edit_dialog(selected_item, row_values)

    def open_edit_dialog(self, item_id, row_values):
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Timesheet Entry")

        labels = ["Clock In (HH:MM)", "Clock Out (HH:MM)", "Register In", "Register Out"]
        entries = []

        # Skip ID, employee name
        for i, (label_text, value) in enumerate(zip(labels, row_values[2:])):
            tk.Label(edit_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(edit_window)
            entry.insert(0, value)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        def save_changes():
            new_values = [entry.get() for entry in entries]
            try:

                clock_in = datetime.strptime(new_values[0], "%Y-%m-%d %H:%M:%S")
                clock_out = datetime.strptime(new_values[1], "%Y-%m-%d %H:%M:%S")
                # Check if the entered date is within the selected month and year
                if (clock_in.month != self.selected_month or clock_in.year != self.selected_year or clock_out.month != self.selected_month or clock_out.year != self.selected_year):
                    messagebox.showerror("Date Error",
                                         f"Please enter times within {self.selected_month}/{self.selected_year}.")
                    return

                regin = float(new_values[2])
                regout = float(new_values[3])

            except ValueError as e:
                messagebox.showerror("Input Error", f"Invalid input: {e}")
                return

            self.update_timesheet_data(row_values[0], clock_in, clock_out, regin, regout)
            edit_window.destroy()

        save_button = ttk.Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=len(labels), columnspan=2, pady=10)

    def update_timesheet_data(self, record_id, clock_in, clock_out, regin, regout):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE timesheet 
                SET clock_in = %s, clock_out = %s, regin = %s, regout = %s
                WHERE id = %s
            """, (clock_in, clock_out, regin, regout, record_id))

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Timesheet record updated successfully!")
            self.fetch_timesheet_data()  # Refresh table

        except Error as e:
            messagebox.showerror("Error", f"Error updating timesheet data: {e}")

    def get_selected_month_year(self):
        return self.selected_month, self.selected_year

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name)

    def fetch_timesheet_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Debug print to verify selected_month and selected_year
            print(f"Fetching timesheet data for Month: {self.selected_month}, Year: {self.selected_year}")

            # Query to fetch timesheet data for the store
            query = """
                SELECT id, empname, clock_in, clock_out, regin, regout 
                FROM timesheet 
                WHERE storename = %s
                AND MONTH(clock_in) = %s AND YEAR(clock_in) = %s
                ORDER BY clock_in DESC
            """
            query_params = [self.store_name, self.selected_month, self.selected_year]

            cursor.execute(query, tuple(query_params))
            data = cursor.fetchall()

            print(f"Fetched Timesheet Data: {data}")

            # Clear existing entries
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Insert new data
            for row in data:
                self.tree.insert("", "end", values=row)

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
                SELECT id, empname, clock_in, clock_out, regin, regout 
                FROM timesheet 
                WHERE storename = %s AND clock_in BETWEEN %s AND %s
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
            messagebox.showerror("Error", f"Error filtering timesheet data: {e}")

    def clear_filter(self):
        """ Reset the table to show all timesheet data """
        # Clear the date entry fields
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.fetch_timesheet_data()  # Fetches and displays all timesheet data
        messagebox.showinfo("Filter Cleared", "All timesheet data will now be displayed.")

