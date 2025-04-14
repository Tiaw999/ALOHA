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
        previous_screen_ref = self.current_screen

        # Screens that use month/year context
        month_aware_screens = [OwnerHome, RevenueScreen, ExpensesScreen, PayrollScreen,
                               StaffScreen, TimesheetScreen, WithdrawalsScreen,
                               MerchandiseScreen, InvoiceScreen]

        # If coming from a screen that uses month/year, get its values
        if type(previous_screen_ref) in month_aware_screens:
            selected_month, selected_year = previous_screen_ref.get_selected_month_year()
            if selected_month is None or selected_year is None:
                print("Error: Could not retrieve valid month/year.")
                return

        if self.current_screen is not None:
            self.current_screen.destroy()

        # If going to a screen that uses month/year, pass the values
        if screen_class in month_aware_screens:
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
