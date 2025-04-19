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
        selected_month, selected_year = None, None
        owner_name = None
        previous_screen_ref = self.current_screen

        # Screens that use month/year context
        month_aware_screens = [OwnerHome, RevenueScreen, ExpensesScreen, PayrollScreen,
                               StaffScreen, TimesheetScreen, MerchandiseScreen, InvoiceScreen]

        # Screens that need owner_name (whether or not they use month/year)
        owner_aware_screens = [LoginScreen, OwnerHome, WithdrawalsScreen]

        # Get context from the previous screen
        if previous_screen_ref:
            # If the previous screen supports month/year, get them
            if hasattr(previous_screen_ref, "get_selected_month_year"):
                selected_month, selected_year = previous_screen_ref.get_selected_month_year()

            # If the previous screen supports owner_name, get it
            if hasattr(previous_screen_ref, "get_owner_name"):
                owner_name = previous_screen_ref.get_owner_name()

        # Destroy current screen
        if self.current_screen is not None:
            self.current_screen.destroy()

        # Create new screen with appropriate arguments
        if screen_class in owner_aware_screens[1:]:
            screen = screen_class(
                self, *args,
                previous_screen=previous_screen_ref,
                selected_month=selected_month,
                selected_year=selected_year,
                owner_name=owner_name
            )
        elif screen_class in month_aware_screens:
            screen = screen_class(
                self, *args,
                previous_screen=previous_screen_ref,
                selected_month=selected_month,
                selected_year=selected_year
            )
        else:
            screen = screen_class(self, *args, previous_screen=previous_screen_ref)

        self.current_screen = screen
        self.current_screen.pack(fill=tk.BOTH, expand=True)


def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()
