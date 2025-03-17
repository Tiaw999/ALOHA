# main.py
import tkinter as tk
from gui.login_screen import LoginScreen

class RetailApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Retail Management System")
        self.geometry("800x600")
        self.resizable(False, False)

        # Start with the login screen
        self.current_screen = None
        self.switch_screen(LoginScreen)

    def switch_screen(self, ScreenClass, *args, **kwargs):
        """Destroys current screen and loads a new one."""
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = ScreenClass(self, *args, **kwargs)
        self.current_screen.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = RetailApp()
    app.mainloop()