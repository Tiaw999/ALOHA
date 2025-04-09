# loghours_screen.py
import tkinter as tk
from tkinter import ttk

class LogHours(tk.Frame):
    def __init__(self, root, store_name, previous_screen):
        super().__init__(root)
        self.root = root
        self.store_name = store_name
        self.previous_screen = previous_screen
        self.root.geometry("900x600")
        self.root.title("Log Hours")

        self.pack(fill=tk.BOTH, expand=True)

        # Back Button - Top Left
        back_button = tk.Button(self, text="<- Back", command=self.go_back)
        back_button.place(x=10, y=10)

        # Form Title
        tk.Label(self, text="Enter the following:").grid(row=1, columnspan=4, pady=20)

        # Clock In
        tk.Label(self, text="Clock In time:").grid(row=2, column=0, sticky='w', padx=10)
        self.clock_in_hr = tk.Entry(self, width=5)
        self.clock_in_hr.grid(row=2, column=1)
        self.clock_in_min = tk.Entry(self, width=5)
        self.clock_in_min.grid(row=2, column=2)
        self.clock_in_ampm = ttk.Combobox(self, values=["AM", "PM"], width=3)
        self.clock_in_ampm.grid(row=2, column=3)

        # Clock Out
        tk.Label(self, text="Clock Out time:").grid(row=3, column=0, sticky='w', padx=10)
        self.clock_out_hr = tk.Entry(self, width=5)
        self.clock_out_hr.grid(row=3, column=1)
        self.clock_out_min = tk.Entry(self, width=5)
        self.clock_out_min.grid(row=3, column=2)
        self.clock_out_ampm = ttk.Combobox(self, values=["AM", "PM"], width=3)
        self.clock_out_ampm.grid(row=3, column=3)

        # Register In
        tk.Label(self, text="Reg $ In:").grid(row=4, column=0, sticky='w', padx=10)
        self.reg_in = tk.Entry(self)
        self.reg_in.grid(row=4, column=1, columnspan=2, sticky='w')

        # Register Out
        tk.Label(self, text="Reg $ Out:").grid(row=5, column=0, sticky='w', padx=10)
        self.reg_out = tk.Entry(self)
        self.reg_out.grid(row=5, column=1, columnspan=2, sticky='w')

        # Enter Button - Styled Blue
        self.enter_button = tk.Button(
            self,
            text="Enter",
            bg="#007bff",  # Bootstrap blue
            fg="white",    # White text
            activebackground="#0056b3",  # Darker blue on click
            activeforeground="white"
        )
        self.enter_button.grid(row=6, column=0, columnspan=4, pady=20)

    def go_back(self):
        print("Back to previous screen")
        if self.previous_screen:
            self.root.switch_screen(self.previous_screen.__class__, self.store_name)