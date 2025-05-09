# gui/owner_home.py
import tkinter as tk
from ttkbootstrap import ttk
from datetime import datetime

# Imports for navigation
from gui.revenue_screen import RevenueScreen
from gui.expenses_screen import ExpensesScreen
from gui.payroll_screen import PayrollScreen
from gui.staff_screen import StaffScreen
from gui.timesheet_screen import TimesheetScreen
from gui.withdrawals_screen import WithdrawalsScreen
from gui.merchandise_screen import MerchandiseScreen
from gui.invoice_screen import InvoiceScreen


class OwnerHome(tk.Frame):
    def __init__(self, master, store_name, user, previous_screen, selected_month=None, selected_year=None):
        super().__init__(master)
        self.master = master
        self.store_name = store_name
        # Default selected_month and selected_year if not passed (for when coming from login)
        if selected_month is None or selected_year is None:
            self.selected_month = datetime.now().month
            self.selected_year = datetime.now().year
        else:
            self.selected_month = selected_month
            self.selected_year = selected_year
        self.user = user
        self.previous_screen = previous_screen
        self.master.title("Owner Home")
        self.master.geometry("900x600")
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = ttk.Label(self, text=f"Owner Home - {self.store_name}", font=("Arial", 24))
        title_label.pack(pady=20)

        # Frame for the Month and Year Dropdown
        date_frame = ttk.Frame(self)
        date_frame.pack(pady=10, padx=20)

        # Get current month and year
        current_year = datetime.now().year  # Current year (e.g., 2025)

        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

        years = [str(year) for year in range(current_year, current_year - 5, -1)]  # Last 5 years

        # Month Dropdown (Combobox)
        month_label = ttk.Label(date_frame, text="Select Month:")
        month_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.month_combobox = ttk.Combobox(date_frame, values=months)
        self.month_combobox.grid(row=0, column=1, padx=10, pady=5)
        self.month_combobox.set(months[self.selected_month - 1])  # Set the default month to the current month

        # Year Dropdown (Combobox)
        year_label = ttk.Label(date_frame, text="Select Year:")
        year_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        self.year_combobox = ttk.Combobox(date_frame, values=years)
        self.year_combobox.grid(row=0, column=3, padx=10, pady=5)
        self.year_combobox.set(str(self.selected_year))  # Set the default year to the current year

        # Frame for Buttons (Revenue, Expenses, etc.)
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10, padx=20)

        # Create Button List
        buttons = [
            ("Revenue", self.go_to_revenue),
            ("Expenses", self.go_to_expenses),
            ("Payroll", self.go_to_payroll),
            ("Staff", self.go_to_staff),
            ("Timesheet", self.go_to_timesheet),
            ("Withdrawals", self.go_to_withdrawals),
            ("Merchandise", self.go_to_merchandise),
            ("Invoices", self.go_to_invoices)
        ]

        # Place buttons in grid with 2 columns
        for idx, (text, command) in enumerate(buttons):
            btn = ttk.Button(button_frame, text=text, width=20, command=command)
            btn.grid(row=idx // 2, column=idx % 2, padx=10, pady=10)

        # Add Back button to return to login screen (Top-Left)
        back_button = ttk.Button(self, text="<- Back", command=self.go_back)
        back_button.place(x=10, y=10)  # Top-left corner with slight padding

        # Make sure the columns in the grid expand properly
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Allow dynamic resizing of rows in the grid
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=1)

        # Force a redraw of widgets to resolve any rendering issues
        self.update()

    def get_selected_month_year(self):
        # Get the selected month and year from the comboboxes
        selected_month = self.month_combobox.get()  # This will be a string like "April"
        selected_year = self.year_combobox.get()  # This will be a string like "2025"

        # Convert the month name to its corresponding integer (1 for January, 2 for February, etc.)
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

        if selected_month in month_names:
            selected_month_int = month_names.index(selected_month) + 1  # Convert to 1-12
        else:
            print("Error: Invalid month selected.")
            return None, None  # Return None if invalid month

        selected_year_int = int(selected_year)  # Convert year to an integer

        return selected_month_int, selected_year_int  # Return the month and year as integers

    def go_to_revenue(self):
        print("Go to Revenue Screen")
        self.master.switch_screen(RevenueScreen, self.store_name, self.user)

    def go_to_expenses(self):
        print("Go to Expenses Screen")
        self.master.switch_screen(ExpensesScreen, self.store_name, self.user)

    def go_to_payroll(self):
        print("Go to Payroll Screen")
        self.master.switch_screen(PayrollScreen, self.store_name, self.user)

    def go_to_staff(self):
        print("Go to Staff Screen")
        self.master.switch_screen(StaffScreen, self.store_name, self.user)

    def go_to_timesheet(self):
        print("Go to Timesheet Screen")
        self.master.switch_screen(TimesheetScreen, self.store_name, self.user)

    def go_to_withdrawals(self):
        print("Go to Withdrawals Screen")
        self.master.switch_screen(WithdrawalsScreen, self.store_name, self.user)

    def go_to_merchandise(self):
        print("Go to Merchandise Screen")
        self.master.switch_screen(MerchandiseScreen, self.store_name, self.user)

    def go_to_invoices(self):
        print("Go to Invoice Screen")
        self.master.switch_screen(InvoiceScreen, self.store_name, self.user)

    def go_back(self):
        print("Back to Login Screen")
        from gui.login_screen import LoginScreen
        # Call master.switch_screen with None to go back to the login screen
        self.master.switch_screen(LoginScreen)

    def get_owner_name(self):
        return self.owner_name