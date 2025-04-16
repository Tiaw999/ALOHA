# payroll_screen.py
# payroll_screen.py
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

        # Payroll Label/Button (for visual consistency)
        payroll_label = ttk.Label(self, text="Payroll Information", font=("Arial", 14))
        payroll_label.grid(row=1, column=1, padx=10, pady=5)

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
        """ Open a pop-up window to add a new payroll row """
        add_window = tk.Toplevel(self)
        add_window.title("Add Payroll Entry")
        add_window.geometry("300x300")

        tk.Label(add_window, text="Employee Name:").pack(pady=2)
        empname_entry = tk.Entry(add_window)
        empname_entry.pack(pady=2)

        tk.Label(add_window, text="Store Name:").pack(pady=2)
        storename_entry = tk.Entry(add_window)
        storename_entry.pack(pady=2)

        tk.Label(add_window, text="Regular Pay:").pack(pady=2)
        regularpay_entry = tk.Entry(add_window)
        regularpay_entry.pack(pady=2)

        tk.Label(add_window, text="Bonus:").pack(pady=2)
        bonus_entry = tk.Entry(add_window)
        bonus_entry.pack(pady=2)

        tk.Label(add_window, text="Pay Date (YYYY-MM-DD):").pack(pady=2)
        paydate_entry = tk.Entry(add_window)
        paydate_entry.pack(pady=2)

        def save_entry():
            """ Save data and close window """
            empname = empname_entry.get().strip()
            storename = storename_entry.get().strip()
            regularpay = regularpay_entry.get().strip()
            bonus = bonus_entry.get().strip()
            paydate_str = paydate_entry.get().strip()

            if not empname or not storename or not regularpay or not bonus or not paydate_str:
                messagebox.showwarning("Input Error", "All fields are required.")
                return

            try:
                paydate = datetime.strptime(paydate_str, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Date Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            try:
                float(regularpay)
                float(bonus)
            except ValueError:
                messagebox.showerror("Input Error", "Regular Pay and Bonus must be numbers.")
                return

            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO payroll (empname, storename, regularpay, bonus, paydate)
                    VALUES (%s, %s, %s, %s, %s)
                """, (empname, storename, regularpay, bonus, paydate))
                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "New payroll record added successfully!")
                self.fetch_payroll_data()  # Refresh table
                add_window.destroy()  # Close window after saving

            except Error as e:
                messagebox.showerror("Error", f"Error adding payroll data: {e}")

        save_btn = tk.Button(add_window, text="Save", command=save_entry)
        save_btn.pack(pady=10)

        add_window.grab_set()  # Make window modal (prevents interaction with main window)

