# close_store.py
import tkinter as tk

class CloseStore(tk.Frame):
    def __init__(self, root, store_name, previous_screen):
        super().__init__(root)
        self.root = root
        self.root.title("Closing Tasks")
        self.store_name = store_name
        self.previous_screen = previous_screen
        self.pack(fill=tk.BOTH, expand=True)

        # Back Button - Top Left
        self.back_button = tk.Button(self, text="<- Back", command=self.go_back)
        self.back_button.place(x=10, y=10)

        # Form Title
        tk.Label(self, text="Enter the following:").grid(row=1, columnspan=2, pady=20)

        # Reg Entry
        tk.Label(self, text="Reg:").grid(row=2, column=0, sticky='w', padx=10)
        self.reg_entry = tk.Entry(self)
        self.reg_entry.grid(row=2, column=1, padx=5)

        # Credit Entry
        tk.Label(self, text="Credit:").grid(row=3, column=0, sticky='w', padx=10)
        self.credit_entry = tk.Entry(self)
        self.credit_entry.grid(row=3, column=1, padx=5)

        # Cash Entry
        tk.Label(self, text="Cash In Envelope:").grid(row=4, column=0, sticky='w', padx=10)
        self.cash_entry = tk.Entry(self)
        self.cash_entry.grid(row=4, column=1, padx=5)

        # Enter Button - Styled Blue
        self.enter_button = tk.Button(
            self,
            text="Enter",
            bg="#007bff",
            fg="white",
            activebackground="#0056b3",
            activeforeground="white"
        )
        self.enter_button.grid(row=5, column=0, columnspan=2, pady=20)

    def go_back(self):
        print("Back to previous screen")
        if self.previous_screen:
            self.root.switch_screen(self.previous_screen.__class__, self.store_name)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x600")
    app = CloseStore(root)
    app.mainloop()