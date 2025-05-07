# invoice_screen.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import get_connection
import mysql.connector
from mysql.connector import Error


class InvoiceScreen(tk.Frame):
    def __init__(self, master, store_name, user, previous_screen, selected_month=None, selected_year=None, owner_name=None):
        super().__init__(master)
        self.master = master
        self.store_name = store_name
        self.user = user
        self.previous_screen = previous_screen
        self.owner_name = owner_name  # unused except if needed
        # Default month/year
        if selected_month is None or selected_year is None:
            now = datetime.now()
            self.selected_month = now.month
            self.selected_year = now.year
        else:
            self.selected_month = selected_month
            self.selected_year = selected_year
        self.columns = ("Invoice #", "Date Received", "Company", "Amount", "Due Date", "Paid", "Date Paid", "Paid With")
        self.master.title("Invoices")
        self.master.geometry("900x600")
        self.create_widgets()
        self.fetch_invoice_data()

    def create_widgets(self):
        # Header
        title = ttk.Label(self, text=f"Invoices - {self.store_name}", font=("Arial", 18, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)

        # Back button
        back_btn = ttk.Button(self, text="<- Back", command=self.go_back)
        back_btn.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Treeview
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, width=100, anchor="w")
        self.tree.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

        # Buttons
        btn_row = 3
        ttk.Button(self, text="Edit Row", command=self.edit_row).grid(row=btn_row, column=0, pady=5)
        ttk.Button(self, text="Add Row", command=self.add_row).grid(row=btn_row, column=1, pady=5)
        ttk.Button(self, text="Delete Row", command=self.delete_row).grid(row=btn_row, column=2, pady=5)

        # Filter row
        filter_row = btn_row + 1
        tk.Label(self, text="Start Date Received (YYYY-MM-DD):").grid(row=filter_row, column=0, sticky="e")
        self.start_date_entry = tk.Entry(self, width=12)
        self.start_date_entry.grid(row=filter_row, column=1)
        tk.Label(self, text="End Date Received (YYYY-MM-DD):").grid(row=filter_row, column=2, sticky="e")
        self.end_date_entry = tk.Entry(self, width=12)
        self.end_date_entry.grid(row=filter_row, column=3)

        ttk.Button(self, text="Filter", command=self.filter_by_date).grid(row=filter_row, column=4, padx=5)
        ttk.Button(self, text="Clear Filter", command=self.clear_filter).grid(row=filter_row, column=5)

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name, self.user)

    def get_selected_month_year(self):
        return self.selected_month, self.selected_year

    def add_row(self):
        """ Open a pop-up window to add a new invoice """
        add_window = tk.Toplevel(self)
        add_window.title("Add Invoice Entry")
        add_window.geometry("460x350")

        form_frame = tk.Frame(add_window)
        form_frame.pack(padx=10, pady=10)

        # Invoice Number
        tk.Label(form_frame, text="Invoice Number").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        invoice_entry = tk.Entry(form_frame)
        invoice_entry.grid(row=0, column=1, padx=10, pady=5)

        # Date Received
        tk.Label(form_frame, text="Date Received (YYYY-MM-DD)").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        date_received_entry = tk.Entry(form_frame)
        date_received_entry.grid(row=1, column=1, padx=10, pady=5)

        # Company
        tk.Label(form_frame, text="Company").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        company_entry = tk.Entry(form_frame)
        company_entry.grid(row=2, column=1, padx=10, pady=5)

        # Amount
        tk.Label(form_frame, text="Amount").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        amount_entry = tk.Entry(form_frame)
        amount_entry.grid(row=3, column=1, padx=10, pady=5)

        # Due Date
        tk.Label(form_frame, text="Due Date (YYYY-MM-DD)").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        due_date_entry = tk.Entry(form_frame)
        due_date_entry.grid(row=4, column=1, padx=10, pady=5)

        # Paid
        tk.Label(form_frame, text="Paid (True/False)").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        paid_entry = tk.Entry(form_frame)
        paid_entry.grid(row=5, column=1, padx=10, pady=5)

        # Date Paid
        tk.Label(form_frame, text="Date Paid (YYYY-MM-DD, optional)").grid(row=6, column=0, padx=10, pady=5, sticky="e")
        date_paid_entry = tk.Entry(form_frame)
        date_paid_entry.grid(row=6, column=1, padx=10, pady=5)

        # Paid With
        tk.Label(form_frame, text="Paid With (CREDIT/CASH, optional)").grid(row=7, column=0, padx=10, pady=5,
                                                                            sticky="e")
        paid_with_entry = tk.Entry(form_frame)
        paid_with_entry.grid(row=7, column=1, padx=10, pady=5)

        # Save Button
        save_button = ttk.Button(form_frame, text="Save Invoice", command=lambda: save_entry())
        save_button.grid(row=8, columnspan=2, pady=15)

        add_window.grab_set()  # Make the window modal

        def save_entry():
            """ Save invoice entry and close window """
            invoicenum = invoice_entry.get().strip()
            date_received = date_received_entry.get().strip()
            company = company_entry.get().strip()
            amount = amount_entry.get().strip()
            due_date = due_date_entry.get().strip()
            paid = paid_entry.get().strip().lower()
            date_paid = date_paid_entry.get().strip()
            paid_with = paid_with_entry.get().strip()
            if paid_with == "":
                paid_with = None
            else:
                paid_with = paid_with.upper()

            if not all([invoicenum, date_received, company, amount, due_date, paid]):
                messagebox.showwarning("Input Error", "Please fill in all required fields.")
                return

            try:
                date_received = datetime.strptime(date_received, "%Y-%m-%d").date()
                due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
                if date_paid:
                    date_paid = datetime.strptime(date_paid, "%Y-%m-%d").date()
                else:
                    date_paid = None

                if date_received.month != self.selected_month or date_received.year != self.selected_year:
                    messagebox.showerror("Date Error",
                                         f"Please enter invoices received within {self.selected_month}/{self.selected_year}.")
                    return
            except ValueError:
                messagebox.showerror("Date Error", "Please use YYYY-MM-DD format for dates.")
                return

            if paid not in ["true", "false"]:
                messagebox.showerror("Input Error", "Paid must be True or False.")
                return

            try:
                amount = float(amount)
            except ValueError:
                messagebox.showerror("Input Error", "Amount must be a number.")
                return

            try:
                conn = get_connection()
                cursor = conn.cursor()
                conn.start_transaction()

                cursor.execute("""
                    INSERT INTO invoices (invoicenum, storename, datereceived, company, amount, duedate, paid, datepaid, paidwith)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (invoicenum, self.store_name, date_received, company, amount, due_date, paid == "true", date_paid,
                      paid_with))

                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "Invoice added successfully!")
                self.fetch_invoice_data()
                add_window.destroy()

            except Error as e:
                if conn:
                    conn.rollback()
                messagebox.showerror("Error", f"Error adding invoice: {e}")

    def delete_row(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select Error", "Please select a row.")
            return

        inv = self.tree.item(sel, "values")[0]
        if not messagebox.askyesno("Confirm", f"Delete invoice {inv}?"):
            return

        try:
            conn = get_connection()
            cur = conn.cursor()
            conn.start_transaction()

            cur.execute("DELETE FROM invoices WHERE invoicenum = %s", (inv,))
            conn.commit()

            cur.close()
            conn.close()

            self.fetch_invoice_data()
            messagebox.showinfo("Deleted", "Invoice deleted.")
        except Exception as e:
            if conn:
                conn.rollback()
            messagebox.showerror("Error", f"Error deleting invoice: {e}")

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
        edit_window.title("Edit Invoice Entry")

        labels = [
            "Date Received (YYYY-MM-DD)", "Company", "Amount", "Due Date (YYYY-MM-DD)",
            "Paid (True=1/False=0)", "Date Paid (YYYY-MM-DD)", "Paid With (CASH/CREDIT)"
        ]
        entries = []

        print(
            f"Row values: {row_values[1:]}")  # This should print the actual row values excluding the Invoice # (first value)
        # Skip the first value (Invoice #), use rest for editable fields
        for i, (label_text, value) in enumerate(zip(labels, row_values[1:])):
            # Debugging: Print out values before inserting into the entry fields
            tk.Label(edit_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(edit_window)
            # If the value is None, leave the entry empty, otherwise insert the value
            if value == "None":
                entry.insert(0, "")  # Leave it empty if the value is None
            else:
                if i in [0, 3, 5] and value:  # Handle any date fields
                    value = value.split(" ")[0]  # Strip time if present in date fields
                entry.insert(0, value)  # Insert the value into the entry field
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        def save_changes():
            new_values = [entry.get().strip() for entry in entries]

            # === Validate required fields ===
            if not all(new_values[:5]):
                messagebox.showerror("Input Error", "All fields except Date Paid and Paid With are required.")
                return

            # === Validate date_received and due_date ===
            for i in [0, 3]:  # Required date fields
                try:
                    datetime.strptime(new_values[i], "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Date Error", f"{labels[i]} must be in YYYY-MM-DD format.")
                    return

            # === Validate optional date_paid ===
            if new_values[5]:  # If it's not empty
                try:
                    datetime.strptime(new_values[5], "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Date Error", f"{labels[5]} must be in YYYY-MM-DD format.")
                    return
            else:
                new_values[5] = None

            # === Validate amount ===
            try:
                float(new_values[2])
            except ValueError:
                messagebox.showerror("Input Error", "Amount must be a valid number.")
                return

            # === Handle Paid With ===
            new_values[6] = new_values[6].upper() if new_values[6] else None

            # If all validations pass, update the database
            self.update_invoice_data(row_values[0], new_values)
            edit_window.destroy()

        save_button = ttk.Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=len(labels), columnspan=2, pady=10)

    def update_invoice_data(self, invoice_id, values):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            conn.start_transaction()

            update_query = """
                UPDATE invoices
                SET datereceived = %s,
                    company = %s,
                    amount = %s,
                    duedate = %s,
                    paid = %s,
                    datepaid = %s,
                    paidwith = %s
                WHERE invoicenum = %s
            """
            cursor.execute(update_query, (*values, invoice_id))
            conn.commit()

            cursor.close()
            conn.close()

            self.fetch_invoice_data()
            messagebox.showinfo("Success", "Invoice updated successfully!")

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Error updating invoice: {err}")

    def fetch_invoice_data(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT invoicenum, datereceived, company, amount, duedate, paid, datepaid, paidwith "
                "FROM invoices WHERE storename=%s AND ((MONTH(duedate) = %s AND YEAR(duedate) = %s) "
                "OR (MONTH(datereceived) = %s AND YEAR(datereceived) = %s)) "
                "ORDER BY CASE WHEN paid = FALSE THEN duedate ELSE NULL END ASC, "
                "CASE WHEN paid = TRUE THEN duedate ELSE NULL END DESC",
                (self.store_name, self.selected_month, self.selected_year, self.selected_month, self.selected_year)
            )
            data = cur.fetchall()
            cur.close()
            conn.close()
            # Clear
            for i in self.tree.get_children(): self.tree.delete(i)
            for row in data: self.tree.insert("", "end", values=row)
            self.resize_columns()
        except Exception as e:
            print(f"Error fetching invoices: {e}")

    def filter_by_date(self):
        sd = self.start_date_entry.get().strip()
        ed = self.end_date_entry.get().strip()
        if not sd or not ed:
            messagebox.showwarning("Input Error", "Enter both start and end dates.")
            return
        try:
            d1 = datetime.strptime(sd, "%Y-%m-%d").date()
            d2 = datetime.strptime(ed, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Date Error", "Dates must be YYYY-MM-DD.")
            return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute(
                "SELECT invoicenum, datereceived, company, amount, duedate, paid, datepaid, paidwith "
                "FROM invoices WHERE storename=%s AND datereceived BETWEEN %s AND %s",
                (self.store_name, d1, d2)
            )
            rows = cur.fetchall(); cur.close(); conn.close()
            for i in self.tree.get_children(): self.tree.delete(i)
            for r in rows: self.tree.insert("", "end", values=r)
            self.resize_columns()
        except Exception as e:
            messagebox.showerror("Error", f"Error filtering: {e}")

    def clear_filter(self):
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.fetch_invoice_data()
        messagebox.showinfo("Filter Cleared", "Showing all invoices.")

    def resize_columns(self):
        min_w = 100
        for i, col in enumerate(self.columns):
            max_len = len(col)
            for item in self.tree.get_children():
                val = self.tree.item(item)["values"][i]
                max_len = max(max_len, len(str(val)))
            self.tree.column(col, width=max(min_w, max_len * 10))
