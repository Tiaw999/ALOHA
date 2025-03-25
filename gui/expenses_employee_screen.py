
import tkinter as tk
from tkinter import ttk

class LogExpenses(tk.Frame):
    def __init__(self, root, store_name=None, previous_screen=None):
        super().__init__(root)
        self.root = root
        self.root.title("Expense Entry")
        self.store_name = store_name
        self.previous_screen = previous_screen
        self.pack(fill=tk.BOTH, expand=True)

        # Back Button - Top Left
        self.back_button = tk.Button(self, text="<- Back", command=self.go_back)
        self.back_button.place(x=10, y=10)

        # Form Title
        tk.Label(self, text="Enter the following:").grid(row=1, columnspan=2, pady=20)

        # Expense Type
        tk.Label(self, text="Expense Type:").grid(row=2, column=0, sticky='w', padx=10)
        self.expense_type = tk.Entry(self)
        self.expense_type.grid(row=2, column=1, padx=5)

        # Expense Amount
        tk.Label(self, text="Expense Amount:").grid(row=3, column=0, sticky='w', padx=10)
        self.expense_amount = tk.Entry(self)
        self.expense_amount.grid(row=3, column=1, padx=5)

        # Enter Button - Styled Blue
        self.enter_button = tk.Button(
            self,
            text="Enter",
            bg="#007bff",  # Bootstrap blue
            fg="white",    # White text
            activebackground="#0056b3",
            activeforeground="white"
        )
        self.enter_button.grid(row=4, column=0, columnspan=2, pady=20)

    def go_back(self):
        print("Back to previous screen")
        if self.previous_screen:
            self.root.switch_screen(self.previous_screen.__class__, self.store_name)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x600")
    app = LogExpenses(root)
    app.mainloop()