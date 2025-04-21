import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import get_connection

class MerchandiseScreen(tk.Frame):
    def __init__(self, master, store_name, previous_screen, selected_month=None, selected_year=None):
        super().__init__(master)
        self.columns = ("ID", "Date", "Merchandise Type", "Value")
        self.master = master
        self.store_name = store_name
        self.previous_screen = previous_screen

        # Default selected_month and selected_year if not passed
        if selected_month is None or selected_year is None:
            now = datetime.now()
            self.selected_month = now.month
            self.selected_year = now.year
        else:
            self.selected_month = selected_month
            self.selected_year = selected_year

        self.master.geometry("900x600")
        self.master.title("Merchandise")
        self.create_widgets()
        self.fetch_merchandise_data()

    def create_widgets(self):
        # Store Name Label
        store_label = ttk.Label(self, text=f"Merchandise - {self.store_name}", font=("Arial", 18, "bold"))
        store_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Back Button
        back_button = ttk.Button(self, text="<- Back", command=self.go_back)
        back_button.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Table (Treeview)
        self.columns = ("ID", "Date", "Merchandise Type", "Value")
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, width=140, anchor="w")

        self.tree.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Row for the buttons (edit, add, delete)
        gap_row = 3
        edit_btn = ttk.Button(self, text="Edit Row", command=self.edit_row)
        edit_btn.grid(row=gap_row, column=0, pady=5)

        add_row_btn = ttk.Button(self, text="Add Row", command=self.add_row)
        add_row_btn.grid(row=gap_row, column=1, pady=5)

        delete_button = ttk.Button(self, text="Delete Row", command=self.delete_row)
        delete_button.grid(row=gap_row, column=2, padx=10, pady=5, sticky="w")

        # Adding gap below row buttons
        gap_row += 1

        # Date Filter Inputs
        tk.Label(self, text="Start Date (YYYY-MM-DD):").grid(row=gap_row, column=0, padx=1, pady=1, sticky="e")
        self.start_date_entry = tk.Entry(self, width=12)
        self.start_date_entry.grid(row=gap_row, column=1, padx=1, pady=2)

        tk.Label(self, text="End Date (YYYY-MM-DD):").grid(row=gap_row, column=2, padx=1, pady=1, sticky="e")
        self.end_date_entry = tk.Entry(self, width=12)
        self.end_date_entry.grid(row=gap_row, column=3, padx=1, pady=2)

        # Filter and Clear Filter Buttons
        filter_btn = ttk.Button(self, text="Filter", command=self.filter_by_date)
        filter_btn.grid(row=gap_row, column=4, padx=5, pady=5)

        clear_filter_btn = ttk.Button(self, text="Clear Filter", command=self.clear_filter)
        clear_filter_btn.grid(row=gap_row, column=5, padx=5, pady=5)

    def add_row(self):
        """ Open a pop-up window to add a new merchandise row """
        add_window = tk.Toplevel(self)
        add_window.title("Add Merchandise Entry")
        add_window.geometry("300x210")

        # Date
        tk.Label(add_window, text="Date (YYYY-MM-DD):").pack(pady=2)
        date_entry = tk.Entry(add_window)
        date_entry.pack(pady=2)

        # Merchandise Type
        tk.Label(add_window, text="Merchandise Type:").pack(pady=2)
        type_entry = tk.Entry(add_window)
        type_entry.pack(pady=2)

        # Merchandise Value
        tk.Label(add_window, text="Value:").pack(pady=2)
        value_entry = tk.Entry(add_window)
        value_entry.pack(pady=2)

        def save_entry():
            date_str = date_entry.get().strip()
            merch_type = type_entry.get().strip()
            merch_value = value_entry.get().strip()

            # All fields required
            if not date_str or not merch_type or not merch_value:
                messagebox.showwarning("Input Error", "All fields are required.")
                return

            # Date format & month/year check
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if date.month != self.selected_month or date.year != self.selected_year:
                    messagebox.showerror(
                        "Date Error",
                        f"Please enter a date within {self.selected_month}/{self.selected_year}."
                    )
                    return
            except ValueError:
                messagebox.showerror("Date Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            # Merchandise type must contain letters
            if merch_type.isnumeric():
                messagebox.showerror("Input Error", "Merchandise Type must contain letters.")
                return

            # Value must be numeric
            try:
                merch_value = float(merch_value)
            except ValueError:
                messagebox.showerror("Input Error", "Value must be a number.")
                return

            # Insert into DB
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO merchandise (storename, merchtype, merchvalue, date)
                    VALUES (%s, %s, %s, %s)
                """, (self.store_name, merch_type, merch_value, date))
                conn.commit()
            finally:
                cursor.close()
                conn.close()

            messagebox.showinfo("Success", "New merchandise record added successfully!")
            self.fetch_merchandise_data()  # Refresh table
            add_window.destroy()

        save_btn = ttk.Button(add_window, text="Save", command=save_entry)
        save_btn.pack(pady=10)

        add_window.grab_set()  # Make window modal

    def delete_row(self):
        """Deletes a selected merchandise record from the Treeview and the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a row to delete.")
            return

        row_id = self.tree.item(selected_item, "values")[0]  # ID is first column

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete merchandise ID {row_id}?"
        )
        if not confirm:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM merchandise WHERE id = %s", (row_id,))
            conn.commit()
            cursor.close()
            conn.close()

            # Remove from Treeview and refresh
            self.tree.delete(selected_item)
            self.fetch_merchandise_data()
            messagebox.showinfo("Success", "Merchandise record deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete merchandise record: {e}")

    def edit_row(self):
        """Open the edit dialog for the selected merchandise record."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a row to edit.")
            return

        # Extract the values for this row: (id, date, merchtype, merchvalue)
        row_values = self.tree.item(selected_item, "values")

        # Call your dialog, passing both the item identifier and its values
        self.open_edit_dialog(selected_item, row_values)

    def open_edit_dialog(self, item_id, row_values):
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Merchandise Entry")

        labels = ["Date (YYYY-MM-DD)", "Merch Type", "Merch Value"]
        entries = []

        # row_values is (id, date, merchtype, merchvalue)
        for i, (label_text, value) in enumerate(zip(labels, row_values[1:])):
            tk.Label(edit_window, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(edit_window)
            if i == 0:
                # strip off time portion
                value = value.split(" ")[0]
            entry.insert(0, value)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            entries.append(entry)

        def save_changes():
            new_date_str, new_type, new_value_str = [e.get().strip() for e in entries]

            # --- Validate Date ---
            try:
                new_date = datetime.strptime(new_date_str, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Date Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            if (new_date.month != self.selected_month or
                    new_date.year != self.selected_year):
                messagebox.showerror(
                    "Date Error",
                    f"Please enter a date within {self.selected_month}/{self.selected_year}."
                )
                return

            # --- Validate Merch Type ---
            if not new_type or new_type.isnumeric():
                messagebox.showerror("Input Error", "Merch Type must be non‑numeric text.")
                return

            # --- Validate Merch Value ---
            try:
                new_value = float(new_value_str)
                if new_value < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Input Error", "Merch Value must be a positive number.")
                return

            # All good — update the DB and UI
            self.update_merchandise_data(
                record_id=row_values[0],
                new_values=(new_date, new_type, new_value)
            )
            edit_window.destroy()

        save_btn = ttk.Button(edit_window, text="Save", command=save_changes)
        save_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def update_merchandise_data(self, record_id, new_values):
        """
        Update an existing merchandise record.
        new_values should be a tuple: (date: date, merchtype: str, merchvalue: float)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE merchandise
                SET date = %s,
                    merchtype = %s,
                    merchvalue = %s
                WHERE id = %s
            """, (*new_values, record_id))
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Merchandise record updated successfully!")
            self.fetch_merchandise_data()  # Refresh the table
        except Exception as e:
            messagebox.showerror("Error", f"Error updating merchandise data: {e}")

    def fetch_merchandise_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Debug print to verify selected_month and selected_year
            print(f"Fetching merchandise for Month: {self.selected_month}, Year: {self.selected_year}")

            # Base query to fetch merchandise data for the store
            query = """
                SELECT id, date, merchtype, merchvalue
                FROM merchandise
                WHERE storename = %s
                  AND MONTH(date) = %s
                  AND YEAR(date) = %s
                ORDER BY date DESC
            """
            cursor.execute(query, (self.store_name, self.selected_month, self.selected_year))
            data = cursor.fetchall()

            print(f"Fetched Merchandise Data: {data}")

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
            print(f"Error fetching merchandise data: {e}")

    def get_selected_month_year(self):
        return self.selected_month, self.selected_year

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name)

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
                SELECT id, date, merchtype, merchvalue
                FROM merchandise
                WHERE storename = %s
                  AND date BETWEEN %s AND %s
                ORDER BY date DESC
            """, (self.store_name, start_date, end_date))

            data = cursor.fetchall()

            # Clear table before adding filtered data
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Insert filtered merchandise rows
            for row in data:
                self.tree.insert("", "end", values=row)

            # Resize to fit
            self.resize_columns()

            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error filtering merchandise data: {e}")

    def clear_filter(self):
        """ Reset the table to show all merchandise data """
        # Clear the date entry fields
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)

        # Re-fetch and display all merchandise rows
        self.fetch_merchandise_data()

        messagebox.showinfo("Filter Cleared", "All merchandise data will now be displayed.")
