# gui/owner_home.py
import tkinter as tk

# Placeholder imports for navigation — you’ll create these screens soon
# from gui.revenue_screen import RevenueScreen
# from gui.expenses_screen import ExpensesScreen
# from gui.payroll_screen import PayrollScreen
# from gui.staff_screen import StaffScreen
# from gui.timesheet_screen import TimesheetScreen
# from gui.withdrawals_screen import WithdrawalsScreen
# from gui.merchandise_screen import MerchandiseScreen
# from gui.invoice_screen import InvoiceScreen

class OwnerHome(tk.Frame):
    def __init__(self, master, store_name):
        super().__init__(master)
        self.master = master
        self.store_name = store_name

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=f"Owner Home - {self.store_name}", font=("Arial", 24)).pack(pady=20)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

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

        for idx, (text, command) in enumerate(buttons):
            btn = tk.Button(button_frame, text=text, width=15, command=command)
            btn.grid(row=idx//2, column=idx%2, padx=10, pady=10)

        tk.Button(self, text="Back", command=self.go_back).pack(pady=20)

    def go_to_revenue(self):
        print("Go to Revenue Screen")
        # self.master.switch_screen(RevenueScreen, self.store_name)

    def go_to_expenses(self):
        print("Go to Expenses Screen")
        # self.master.switch_screen(ExpensesScreen, self.store_name)

    def go_to_payroll(self):
        print("Go to Payroll Screen")
        # self.master.switch_screen(PayrollScreen, self.store_name)

    def go_to_staff(self):
        print("Go to Staff Screen")
        # self.master.switch_screen(StaffScreen, self.store_name)

    def go_to_timesheet(self):
        print("Go to Timesheet Screen")
        # self.master.switch_screen(TimesheetScreen, self.store_name)

    def go_to_withdrawals(self):
        print("Go to Withdrawals Screen")
        # self.master.switch_screen(WithdrawalsScreen, self.store_name)

    def go_to_merchandise(self):
        print("Go to Merchandise Screen")
        # self.master.switch_screen(MerchandiseScreen, self.store_name)

    def go_to_invoices(self):
        print("Go to Invoice Screen")
        # self.master.switch_screen(InvoiceScreen, self.store_name)

    def go_back(self):
        self.master.switch_screen(None)  # Goes back to login screen