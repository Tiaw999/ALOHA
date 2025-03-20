# gui/login_screen.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import db  # Import your db module here

class LoginScreen(tk.Frame):  # Ensure it inherits from tk.Frame
    def __init__(self, master):
        super().__init__(master)  # Call the initializer of tk.Frame
        print("Initializing Login Screen")  # Debugging line
        self.master = master
        self.master.configure(bg="#f0f0f0")

        self.frame = ttk.Frame(master, padding="30 30 30 30")
        self.frame.pack(expand=True)  # Pack the frame here instead of the LoginScreen itself

        ttk.Label(self.frame, text="Store Name:").grid(column=0, row=0, sticky=tk.W, pady=5)
        self.store_entry = ttk.Entry(self.frame, width=30)
        self.store_entry.grid(column=1, row=0, pady=5)

        ttk.Label(self.frame, text="Username:").grid(column=0, row=1, sticky=tk.W, pady=5)
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
        store = self.store_entry.get()
        user = self.user_entry.get()
        password = self.pass_entry.get()

        role = db.authenticate_user(store, user, password)  # Assuming authenticate_user is defined in db.py
        if role:
            messagebox.showinfo("Login Success", f"Welcome {role}: {user}")
            # Transition to owner_home or other screens here
        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")
