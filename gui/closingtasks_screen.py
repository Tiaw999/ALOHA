import tkinter as tk


class ClosingTasks(tk.Frame):
    def __init__(self, root):
        self.root = root
        self.root.title("Closing Tasks Home Screen")

        tk.Label(root, text="Enter the following:").grid(row=0, columnspan=2, pady=5)

        tk.Label(root, text="Reg:").grid(row=1, column=0, sticky='w')
        self.reg_entry = tk.Entry(root)
        self.reg_entry.grid(row=1, column=1)

        tk.Label(root, text="Credit:").grid(row=2, column=0, sticky='w')
        self.credit_entry = tk.Entry(root)
        self.credit_entry.grid(row=2, column=1)

        tk.Label(root, text="Cash In Envelope:").grid(row=3, column=0, sticky='w')
        self.cash_entry = tk.Entry(root)
        self.cash_entry.grid(row=3, column=1)

        self.enter_button = tk.Button(root, text="Enter", bg="lightgreen")
        self.enter_button.grid(row=4, column=0, columnspan=2, pady=5)

        self.back_button = tk.Button(root, text="<- Back", bg="orange")
        self.back_button.grid(row=5, column=0, columnspan=2, pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = ClosingTasks(root)
    root.mainloop()
