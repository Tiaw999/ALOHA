# gui/login_screen.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import db  # Make sure to import the db module where get_stores is defined

# Import your home screen modules
from gui.owner_home import OwnerHome
from gui.manager_home import ManagerHome
from gui.employee_home import EmployeeHome

class LoginScreen(tk.Frame):
    def __init__(self, master, previous_screen):
        super().__init__(master)
        self.master = master
        self.master.configure(bg="#f0f0f0")
        self.previous_screen = previous_screen
        self.master.title("Login Screen")
        # Set the geometry to fit the screen
        self.master.geometry("900x600")
        self.frame = ttk.Frame(self, padding="30 30 30 30")
        self.frame.pack(expand=True)

        # Create widgets
        ttk.Label(self.frame, text="Store Name:").grid(column=0, row=0, sticky=tk.W, pady=5)

        # Fetch store names from the database and populate the dropdown
        self.store_names = db.get_stores()  # Call the get_stores function from db.py
        self.store_var = tk.StringVar()  # Variable to store the selected store

        self.store_dropdown = ttk.Combobox(self.frame, textvariable=self.store_var, values=self.store_names)
        self.store_dropdown.grid(column=1, row=0, pady=5)

        ttk.Label(self.frame, text="Name:").grid(column=0, row=1, sticky=tk.W, pady=5)
        self.user_entry = ttk.Entry(self.frame, width=30)
        self.user_entry.grid(column=1, row=1, pady=5)

        ttk.Label(self.frame, text="Password:").grid(column=0, row=2, sticky=tk.W, pady=5)
        self.pass_entry = ttk.Entry(self.frame, show="*", width=30)
        self.pass_entry.grid(column=1, row=2, pady=5)

        self.login_button = ttk.Button(self.frame, text="Login", command=self.login)
        self.login_button.grid(column=1, row=3, pady=20)

        for child in self.frame.winfo_children():
            child.grid_configure(padx=10)

    def login(self):
        store = self.store_var.get()
        user = self.user_entry.get()
        password = self.pass_entry.get()

        role = db.authenticate_user(store, user, password)
        if role:
            messagebox.showinfo("Login Success", f"Welcome {role}: {user}")

            # Switch to the appropriate home screen based on the role
            if role == "Owner":
                self.master.switch_screen(OwnerHome, store, user)
            elif role == "Manager":
                self.master.switch_screen(ManagerHome, store, user)
            else:
                self.master.switch_screen(EmployeeHome, store, user)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")


