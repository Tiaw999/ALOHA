
import tkinter as tk
from tkinter import ttk

class ExpenseEmployeeScreen(tk.Frame):
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Entry")

        tk.Label(root, text="Enter the following:").grid(row=0, columnspan=2, pady=5)

        tk.Label(root, text="Expense Type:").grid(row=1, column=0, sticky='w')
        self.expense_type = tk.Entry(root)
        self.expense_type.grid(row=1, column=1)

        tk.Label(root, text="Expense Amount:").grid(row=2, column=0, sticky='w')
        self.expense_amount = tk.Entry(root)
        self.expense_amount.grid(row=2, column=1)

        self.enter_button = tk.Button(root, text="Enter", bg="lightgreen")
        self.enter_button.grid(row=3, column=0, columnspan=2, pady=5)

        self.back_button = tk.Button(root, text="<- Back", bg="orange")
        self.back_button.grid(row=4, column=0, columnspan=2, pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseEmployeeScreen(root)
    root.mainloop()