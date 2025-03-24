# main
import tkinter as tk
from gui.login_screen import LoginScreen

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Store Manager Login")
        self.resizable(False, False)

        # Set the initial screen to the login screen
        self.switch_screen(LoginScreen)

    def switch_screen(self, screen_class, *args):
        """Switch the current screen to the new screen."""
        # Destroy the current screen/frame
        for widget in self.winfo_children():
            widget.destroy()

        # Create and pack the new screen
        screen = screen_class(self, *args)
        screen.pack(expand=True, fill="both")

def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()
