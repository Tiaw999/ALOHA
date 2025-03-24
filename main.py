# main
import tkinter as tk
from gui.login_screen import LoginScreen

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Store Manager Login")
        self.resizable(False, False)
        self.current_screen = None  # Initialize current_screen
        # Set the initial screen to the login screen
        self.switch_screen(LoginScreen)

    def switch_screen(self, screen_class, *args):
        if self.current_screen is not None:
            self.current_screen.destroy()  # Remove the current screen

        # Pass the current screen as the previous_screen argument to all screens
        screen = screen_class(self, *args, previous_screen=self.current_screen)

        self.current_screen = screen  # Set the new screen
        self.current_screen.pack(fill=tk.BOTH, expand=True)

def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()
