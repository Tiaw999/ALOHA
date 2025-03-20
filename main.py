# main
import tkinter as tk
import ttkbootstrap as ttk
from gui.login_screen import LoginScreen

def main():
    root = tk.Tk()  # Use Tk() for the root window
    root.title("Store Manager Login")  # Set window title
    root.geometry("400x300")  # Set window size

    # Create the LoginScreen
    login_screen = LoginScreen(root)
    login_screen.pack(expand=True, fill="both")  # Ensure the screen is packed

    root.mainloop()  # Start the Tkinter main loop

if __name__ == "__main__":
    main()