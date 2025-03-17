# gui/login_screen.py
import tkinter as tk
from tkinter import ttk, messagebox

# Placeholder imports — you'll create these files later
# from gui.owner_home import OwnerHome
# from gui.manager_home import ManagerHome
# from gui.employee_home import EmployeeHome

class LoginScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.selected_role = tk.StringVar(value="Owner")
        self.password_var = tk.StringVar()
        self.store_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Welcome!", font=("Arial", 24)).pack(pady=20)

        # Store Dropdown
        tk.Label(self, text="Select Store:").pack(pady=(10, 0))
        self.store_dropdown = ttk.Combobox(self, textvariable=self.store_var, values=self.get_stores())
        self.store_dropdown.pack(pady=5)

        # Role Buttons
        tk.Label(self, text="Select Role:").pack(pady=(15, 0))
        role_frame = tk.Frame(self)
        role_frame.pack(pady=5)

        for role in ["Owner", "Manager", "Employee"]:
            btn = tk.Radiobutton(role_frame, text=role, variable=self.selected_role, value=role)
            btn.pack(side="left", padx=10)

        # Password Entry
        tk.Label(self, text="Password:").pack(pady=(15, 0))
        tk.Entry(self, textvariable=self.password_var, show="*").pack(pady=5)

        # Login Button
        tk.Button(self, text="Enter", command=self.login).pack(pady=20)

    def get_stores(self):
        # TODO: Replace with real store data from database
        return ["Store 1", "Store 2", "Store 3"]

    def login(self):
        store = self.store_var.get()
        role = self.selected_role.get()
        password = self.password_var.get()

        if not store or not password:
            messagebox.showwarning("Missing Info", "Please select a store and enter your password.")
            return

        # TODO: Replace with real authentication
        if password == "password123":  # Placeholder password check
            messagebox.showinfo("Login Successful", f"Welcome, {role} of {store}!")

            # Navigate to the correct home screen
            if role == "Owner":
                print("Go to Owner Home Screen")
                self.master.switch_screen(OwnerHome, store)
            elif role == "Manager":
                print("Go to Manager Home Screen")
                # self.master.switch_screen(ManagerHome, store)
            else:
                print("Go to Employee Home Screen")
                # self.master.switch_screen(EmployeeHome, store)

        else:
            messagebox.showerror("Login Failed", "Incorrect password. Try again.")