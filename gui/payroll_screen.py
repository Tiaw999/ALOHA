# payroll_screen.py
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from db import get_connection


class PayrollScreen(tk.Frame):
    def __init__(self, master, store_name, user, previous_screen, selected_month=None, selected_year=None):
        super().__init__(master)
        self.columns = ("ID", "Employee Name", "Regular Pay", "Bonus", "Pay Date")
        self.master = master
        self.store_name = store_name
        self.user = user
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
        self.columns = ("ID", "Employee Name", "Regular Pay", "Bonus", "Pay Date")
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col, anchor="w")  # 'w' stands for "west" which aligns to the left
            self.tree.column(col, width=120, anchor="w")  # Ensures the column values are also left-aligned

        self.tree.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Row for the buttons (edit table, add row, delete row)
        gap_row = 3  # The row after the table for buttons

        # Date Filter Inputs (moved below row buttons, adjusted to be more compact horizontally)
        tk.Label(self, text="Pay Date (YYYY-MM-DD):").grid(row=gap_row, column=0, padx=1, pady=1, sticky="e")
        self.pay_date_entry = tk.Entry(self, width=12)  # Reduced width for better fitting
        self.pay_date_entry.grid(row=gap_row, column=1, padx=1, pady=2)

        # Prefill with today's date
        today_str = datetime.now().strftime("%Y-%m-%d")
        self.pay_date_entry.insert(0, today_str)

        # Filter and Clear Filter Buttons (placed after the date filter inputs, more compact)
        filter_btn = ttk.Button(self, text="Calculate", command=self.calculate)
        filter_btn.grid(row=gap_row, column=2, padx=5, pady=5)

        # Adding gap below row buttons
        gap_row += 1
        delete_button = ttk.Button(self, text="Delete Row", command=self.delete_row)
        delete_button.grid(row=gap_row, column=2, padx=10, pady=5, sticky="w")

    def calculate(self):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            conn.start_transaction()

            # Get paydate from user input or use today as fallback
            pay_date_str = self.pay_date_entry.get().strip()

            # Validate pay_date input
            try:
                pay_date = datetime.strptime(pay_date_str, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter a valid Pay Date in YYYY-MM-DD format.")
                return

            start_date = pay_date - timedelta(days=14)
            end_date = pay_date

            # Get hours worked (clock_in to clock_out) and bonus hours (regout - regin)
            cursor.execute("""
                SELECT 
                    t.empname,
                    SUM(TIMESTAMPDIFF(MINUTE, t.clock_in, t.clock_out)) / 60.0 AS hours_worked,
                    SUM(t.regout - t.regin) AS sales,
                    s.bonusrate,
                    s.hourlyrate
                FROM timesheet t
                JOIN staff s ON lower(t.empname) = lower(s.name)
                WHERE t.storename = %s
                  AND t.clock_in >= %s AND t.clock_in <= %s
                GROUP BY t.empname, s.bonusrate, s.hourlyrate
            """, (self.store_name, start_date, end_date))

            results = cursor.fetchall()

            for empname, hours_worked, sales, bonus_rate, hourly_rate in results:
                regular_pay = hours_worked * hourly_rate
                bonus = sales * bonus_rate

                cursor.execute("""
                    INSERT INTO payroll (empname, storename, regularpay, bonus, paydate)
                    VALUES (%s, %s, %s, %s, %s)
                """, (empname, self.store_name, regular_pay, bonus, pay_date))

            conn.commit()
            messagebox.showinfo("Success", "Payroll calculated successfully!")
            self.fetch_payroll_data()

        except Error as e:
            if conn:
                conn.rollback()
            messagebox.showerror("Error", f"Error adding payroll data: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_row(self):
        """ Deletes a selected row from the Treeview and the database """
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a row to delete.")
            return

        row_id = self.tree.item(selected_item, "values")[0]  # Assuming ID is the first value

        confirm = messagebox.askyesno("Confirm Deletion",
                                      f"Are you sure you want to delete the record with ID {row_id}?")
        if not confirm:
            return

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            conn.start_transaction()  # Start transaction

            cursor.execute("DELETE FROM payroll WHERE id = %s", (row_id,))
            conn.commit()

            self.tree.delete(selected_item)
            self.fetch_payroll_data()
            messagebox.showinfo("Success", "Row deleted successfully!")

        except Error as e:
            if conn:
                conn.rollback()
            messagebox.showerror("Error", f"Failed to delete row: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_selected_month_year(self):
        return self.selected_month, self.selected_year

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name, self.user)

    def fetch_payroll_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Debug print to verify selected_month and selected_year
            print(f"Fetching data for Month: {self.selected_month}, Year: {self.selected_year}")

            # Base query to fetch payroll data for the store and date
            query = """
                SELECT id, empname, regularpay, bonus, paydate 
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
