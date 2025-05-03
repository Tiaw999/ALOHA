# staff_screen.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import get_connection

class StaffScreen(tk.Frame):
    def __init__(self, master, store_name, user, previous_screen, selected_month=None, selected_year=None):
        super().__init__(master)
        self.columns = ("Name", "Role", "Hourly Rate", "Bonus Rate")
        self.master = master
        self.store_name = store_name
        self.user = user
        self.previous_screen = previous_screen

        # Default selected_month and selected_year if not passed
        if selected_month is None or selected_year is None:
            self.selected_month = datetime.now().month
            self.selected_year = datetime.now().year
        else:
            self.selected_month = selected_month
            self.selected_year = selected_year

        self.master.geometry("900x600")
        self.master.title("Staff Management")
        self.create_widgets()
        self.fetch_staff_data()

    def create_widgets(self):
        # Store Name Label
        store_label = ttk.Label(self, text=f"Staff - {self.store_name}", font=("Arial", 18, "bold"))
        store_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Back Button
        back_button = ttk.Button(self, text="<- Back", command=self.go_back)
        back_button.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Treeview Table for Staff
        self.columns = ("Name", "Role", "Hourly Rate", "Bonus Rate")
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, width=150, anchor="w")

        self.tree.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Row for the action buttons
        btn_row = 3
        edit_btn = ttk.Button(self, text="Edit Row", command=self.edit_row)
        edit_btn.grid(row=btn_row, column=0, pady=5)

        add_row_btn = ttk.Button(self, text="Add Row", command=self.add_row)
        add_row_btn.grid(row=btn_row, column=1, pady=5)

        delete_button = ttk.Button(self, text="Delete Row", command=self.delete_row)
        delete_button.grid(row=btn_row, column=2, padx=10, pady=5, sticky="w")

    def add_row(self):
        """Open a pop-up window to add a new staff member"""
        add_window = tk.Toplevel(self)
        add_window.title("Add Staff Member")
        add_window.geometry("340x260")

        form_frame = tk.Frame(add_window)
        form_frame.pack(padx=10, pady=10)

        # Name
        tk.Label(form_frame, text="Name").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        name_entry = tk.Entry(form_frame)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Hourly Rate
        tk.Label(form_frame, text="Hourly Rate").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        hourly_entry = tk.Entry(form_frame)
        hourly_entry.grid(row=1, column=1, padx=10, pady=5)

        # Bonus Rate
        tk.Label(form_frame, text="Bonus Rate").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        bonus_entry = tk.Entry(form_frame)
        bonus_entry.grid(row=2, column=1, padx=10, pady=5)

        # Password
        tk.Label(form_frame, text="Password").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        password_entry = tk.Entry(form_frame, show="*")
        password_entry.grid(row=3, column=1, padx=10, pady=5)

        # Role
        tk.Label(form_frame, text="Role").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        role_combobox = ttk.Combobox(form_frame, values=["Owner", "Manager", "Employee"], state="readonly")
        role_combobox.grid(row=4, column=1, padx=10, pady=5)

        # Save button
        save_button = ttk.Button(form_frame, text="Save Staff Member", command=lambda: save_staff())
        save_button.grid(row=5, columnspan=2, pady=15)

        add_window.grab_set()  # Make the window modal

        def save_staff():
            name = name_entry.get().strip()
            hourly = hourly_entry.get().strip()
            bonus = bonus_entry.get().strip()
            password = password_entry.get().strip()
            role = role_combobox.get()

            if not all([name, hourly, bonus, password, role]):
                messagebox.showwarning("Input Error", "All fields are required.")
                return

            try:
                hourly = float(hourly)
                bonus = float(bonus)
            except ValueError:
                messagebox.showerror("Input Error", "Hourly Rate and Bonus Rate must be numbers.")
                return

            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO staff (name, storename, hourlyrate, bonusrate, password, role)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (name, self.store_name, hourly, bonus, password, role))
                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "Staff member added successfully!")
                self.fetch_staff_data()
                add_window.destroy()

            except Error as e:
                messagebox.showerror("Database Error", f"Error adding staff member: {e}")

    def delete_row(self):
        """Deletes a selected staff member from the Treeview and the database"""
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a row to delete.")
            return

        # Get the staff name and store from the selected row
        values = self.tree.item(selected_item, "values")
        name = values[0]
        storename = self.store_name  # Since this screen is store-specific

        # Confirm the deletion
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete {name} from {storename}?"
        )

        if confirm:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM staff WHERE name = %s AND storename = %s", (name, storename))
                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Success", f"Staff member {name} deleted successfully!")
                self.fetch_staff_data()  # Refresh the Treeview
            except Error as e:
                messagebox.showerror("Error", f"Failed to delete staff member: {e}")

    def edit_row(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a staff member to edit.")
            return

        # Get the staff name from the selected row
        selected_name = self.tree.item(selected_item, "values")[0]

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, role, hourlyrate, bonusrate, password
                FROM staff
                WHERE name = %s AND storename = %s
            """, (selected_name, self.store_name))
            staff_data = cursor.fetchone()
            cursor.close()
            conn.close()

            if staff_data:
                self.open_edit_dialog(staff_data)
            else:
                messagebox.showerror("Error", "Failed to retrieve staff details.")
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch staff data: {e}")

    def open_edit_dialog(self, row_values):
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Staff Member")

        labels = ["Name", "Role", "Hourly Rate", "Bonus Rate", "Password"]
        entries = []

        for i, (label_text, value) in enumerate(zip(labels, row_values)):
            tk.Label(edit_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)

            if label_text == "Role":
                entry = ttk.Combobox(edit_window, values=["Owner", "Manager", "Employee"], state="readonly")
                entry.set(value)
            elif label_text == "Password":
                entry = tk.Entry(edit_window, show = "*")
                entry.insert(0, value)
            else:
                entry = tk.Entry(edit_window)
                entry.insert(0, value)

            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        def save_changes():
            new_values = [entry.get().strip() for entry in entries]

            if not all(new_values):
                messagebox.showwarning("Input Error", "All fields must be filled.")
                return

            try:
                float(new_values[2])  # hourlyrate
                float(new_values[3])  # bonusrate
            except ValueError:
                messagebox.showerror("Input Error", "Hourly Rate and Bonus Rate must be numeric.")
                return

            name, role, hourlyrate, bonusrate, password = new_values

            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE staff
                    SET role = %s,
                        hourlyrate = %s,
                        bonusrate = %s,
                        password = %s
                    WHERE name = %s AND storename = %s
                """, (role, hourlyrate, bonusrate, password, name, self.store_name))
                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "Staff member updated successfully.")
                self.fetch_staff_data()
                edit_window.destroy()
            except Error as e:
                messagebox.showerror("Database Error", f"Failed to update staff: {e}")

        save_button = ttk.Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=len(labels), columnspan=2, pady=10)

    def update_staff_data(self, name, storename, new_values):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE staff
                SET hourlyrate = %s,
                    bonusrate = %s,
                    password = %s,
                    role = %s
                WHERE name = %s AND storename = %s
            """, (*new_values, name, storename))

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Staff record updated successfully!")
            self.fetch_staff_data()  # Refresh table

        except Error as e:
            messagebox.showerror("Error", f"Error updating staff data: {e}")

    def get_selected_month_year(self):
        return self.selected_month, self.selected_year

    def go_back(self):
        self.master.switch_screen(self.previous_screen.__class__, self.store_name, self.user)

    def fetch_staff_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Fetch all staff members at the current store
            query = """
                SELECT name, role, hourlyrate, bonusrate
                FROM staff
                WHERE storename = %s
                ORDER BY name ASC
            """
            cursor.execute(query, (self.store_name,))
            data = cursor.fetchall()

            # Debug print
            print(f"Fetched Staff Data: {data}")

            # Clear existing entries in the Treeview
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Insert fetched data into Treeview
            for row in data:
                self.tree.insert("", "end", values=row)

            # Resize Treeview columns
            self.resize_columns()

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error fetching staff data: {e}")

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



