# revenue_screen.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import get_connection
import mysql.connector

class RevenueScreen(tk.Frame):
    def __init__(self, master, store_name, previous_screen):
        super().__init__(master)
        self.columns = ("ID", "Date", "Reg", "Credit", "Cash in Envelope")
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
        columns = ("ID", "Date", "Reg", "Credit", "Cash in Envelope")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col, anchor="w")  # 'w' stands for "west" which aligns to the left
            self.tree.column(col, width=120, anchor="w")  # Ensures the column values are also left-aligned

        self.tree.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Date Filter Inputs
        tk.Label(self, text="Start Date (YYYY-MM-DD):").grid(row=4, column=0, padx=10, pady=5)
        self.start_date_entry = tk.Entry(self)
        self.start_date_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self, text="End Date (YYYY-MM-DD):").grid(row=4, column=2, padx=10, pady=5)
        self.end_date_entry = tk.Entry(self)
        self.end_date_entry.grid(row=4, column=3, padx=10, pady=5)

        # Filter Button
        filter_btn = ttk.Button(self, text="Filter", command=self.filter_by_date)
        filter_btn.grid(row=4, column=4, padx=10, pady=5)

        # Edit Table Button
        edit_btn = ttk.Button(self, text="Edit Table", command=self.edit_table)
        edit_btn.grid(row=3, column=0, pady=5)

        # Add Row Button
        add_row_btn = ttk.Button(self, text="Add Row", command=self.add_row)
        add_row_btn.grid(row=3, column=1, pady=5)

        # Delete Row Button
        delete_button = ttk.Button(self, text="Delete Row", command=self.delete_row)
        delete_button.grid(row=3, column=2, padx=10, pady=5, sticky="w")

        # Clear Filter Button
        clear_filter_btn = ttk.Button(self, text="Clear Filter", command=self.clear_filter)
        clear_filter_btn.grid(row=3, column=3, pady=5)

    def add_row(self):
        """ Open a pop-up window to add a new revenue row """
        add_window = tk.Toplevel(self)
        add_window.title("Add Revenue Entry")
        add_window.geometry("300x250")

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
            except ValueError:
                messagebox.showerror("Date Error", "Invalid date format. Use YYYY-MM-DD.")
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

        cancel_btn = tk.Button(add_window, text="Cancel", command=add_window.destroy)  # Cancel Button
        cancel_btn.pack(pady=5)

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

                # Remove the row from the Treeview
                self.tree.delete(selected_item)

                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "Row deleted successfully!")
            except Error as e:
                messagebox.showerror("Error", f"Failed to delete row: {e}")

    def edit_table(self):
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
        edit_window.title("Edit Revenue Entry")

        labels = ["Date (YYYY-MM-DD)", "Reg", "Credit", "Cash in Envelope"]
        entries = []

        # We skip the first value (id) and assign remaining values to the fields
        for i, (label_text, value) in enumerate(zip(labels, row_values[1:])):  # Skip the first value (ID)
            tk.Label(edit_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(edit_window)
            entry.insert(0, value)  # Pre-fill with existing data
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        # Save button
        def save_changes():
            new_values = [entry.get() for entry in entries]

            # Debugging: Print the date value from the entry
            print(f"Date value entered: {new_values[0]}")

            # Validate date format
            try:
                # Try parsing the date to ensure it's in the correct format
                new_values[0] = datetime.strptime(new_values[0], "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Date Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            # Update the database with new values, and include the item_id (row's ID)
            self.update_revenue_data(item_id, row_values[0], new_values)
            edit_window.destroy()

        save_button = ttk.Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=len(labels), columnspan=2, pady=10)

    def update_revenue_data(self, item_id, old_date, new_values):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Update the database
            cursor.execute("""
                UPDATE revenue 
                SET date = %s, reg = %s, credit = %s, cashinenvelope = %s 
                WHERE storename = %s AND date = %s
            """, (*new_values, self.store_name, old_date))

            conn.commit()

            # Update Treeview display
            self.tree.item(item_id, values=new_values)

            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Revenue record updated successfully!")

        except Error as e:
            messagebox.showerror("Error", f"Error updating revenue data: {e}")

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name)

    def fetch_revenue_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, date, reg, credit, cashinenvelope 
                FROM revenue 
                WHERE storename = %s
                ORDER BY date DESC
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


        except mysql.connector.Error as e:

            messagebox.showerror("Database Error", f"Database error occurred: {e}")

        except Exception as e:

            messagebox.showerror("Error", f"An error occurred: {e}")

    def resize_columns(self):
        min_width = 80  # Minimum width for each column to ensure header is visible

        for i, col in enumerate(self.columns):
            # Set a minimal width to ensure header text is visible
            self.tree.column(col, width=max(min_width, len(col) * 10))

            max_length = len(col)

            # Calculate the max content length for each column
            for item in self.tree.get_children():
                value = self.tree.item(item)["values"][i]
                max_length = max(max_length, len(str(value)))

            # Adjust the column width dynamically based on content length
            self.tree.column(col, width=max(min_width, max_length * 10))

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
            conn = mysql.connector.connect(
                host="localhost", user="root", password="Cooldaisy662", database="store_manager"
            )
            cursor = conn.cursor()
            cursor.execute("""
                SELECT date, reg, credit, cashinenvelope 
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
        self.fetch_revenue_data()  # Fetches and displays all revenue data
        messagebox.showinfo("Filter Cleared", "All revenue data is now displayed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RevenueScreen(root, "aloha", None)  # Replace "aloha" with the actual store name
    root.mainloop()
