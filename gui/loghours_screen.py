### timesheet_app.py
import tkinter as tk
from tkinter import ttk
##pushing pus

class Loghour(tk.Frame):
    def __init__(self, root):
        self.root = root
        self.root.title("Log Hours Entry")

        tk.Label(root, text="Enter the following:").grid(row=0, columnspan=2, pady=5)

        tk.Label(root, text="Clock In time:").grid(row=1, column=0, sticky='w')
        self.clock_in_hr = tk.Entry(root, width=5)
        self.clock_in_hr.grid(row=1, column=1)
        self.clock_in_min = tk.Entry(root, width=5)
        self.clock_in_min.grid(row=1, column=2)
        self.clock_in_ampm = ttk.Combobox(root, values=["AM", "PM"], width=3)
        self.clock_in_ampm.grid(row=1, column=3)

        tk.Label(root, text="Clock Out time:").grid(row=2, column=0, sticky='w')
        self.clock_out_hr = tk.Entry(root, width=5)
        self.clock_out_hr.grid(row=2, column=1)
        self.clock_out_min = tk.Entry(root, width=5)
        self.clock_out_min.grid(row=2, column=2)
        self.clock_out_ampm = ttk.Combobox(root, values=["AM", "PM"], width=3)
        self.clock_out_ampm.grid(row=2, column=3)

        tk.Label(root, text="Reg $ In:").grid(row=3, column=0, sticky='w')
        self.reg_in = tk.Entry(root)
        self.reg_in.grid(row=3, column=1, columnspan=2)

        tk.Label(root, text="Reg $ Out:").grid(row=4, column=0, sticky='w')
        self.reg_out = tk.Entry(root)
        self.reg_out.grid(row=4, column=1, columnspan=2)

        self.enter_button = tk.Button(root, text="Enter", bg="lightgreen")
        self.enter_button.grid(row=5, column=0, columnspan=4, pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = Loghour(root)
    root.mainloop()
