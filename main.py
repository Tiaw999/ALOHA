# main
import tkinter as tk
from gui.login_screen import LoginScreen
from gui.owner_home import OwnerHome
from gui.revenue_screen import RevenueScreen
from gui.expenses_screen import ExpensesScreen
from gui.payroll_screen import PayrollScreen
from gui.staff_screen import StaffScreen
from gui.timesheet_screen import TimesheetScreen
from gui.withdrawals_screen import WithdrawalsScreen
from gui.merchandise_screen import MerchandiseScreen
from gui.invoice_screen import InvoiceScreen


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Store Manager Login")
        self.resizable(False, False)
        self.current_screen = None  # Initialize current_screen
        # Set the initial screen to the login screen
        self.switch_screen(LoginScreen)

    def switch_screen(self, screen_class, *args):
        # Check if coming from OwnerHome
        selected_month, selected_year = None, None
        if isinstance(self.current_screen, OwnerHome):
            # Fetch selected month/year before destroying the screen
            selected_month, selected_year = self.current_screen.get_selected_month_year()
            if selected_month is None or selected_year is None:
                print("Error: Could not retrieve valid month/year.")
                return  # Exit if values are not available

        if self.current_screen is not None:
            # Destroy the current screen
            self.current_screen.destroy()

        # Check if the new screen needs the month/year
        if screen_class in [RevenueScreen, ExpensesScreen, PayrollScreen, StaffScreen, TimesheetScreen, WithdrawalsScreen, MerchandiseScreen, InvoiceScreen]:  # Add other screens here that need the month/year
            screen = screen_class(self, *args, previous_screen=self.current_screen,
                                  selected_month=selected_month,
                                  selected_year=selected_year)
        else:
            # For screens that don't need the month/year, just pass the previous screen
            screen = screen_class(self, *args, previous_screen=self.current_screen)

        self.current_screen = screen  # Set the new screen
        self.current_screen.pack(fill=tk.BOTH, expand=True)  # Ensure it fills the window properly

def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()
