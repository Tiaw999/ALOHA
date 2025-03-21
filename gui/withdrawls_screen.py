import tkinter as tk
from tkinter import ttk


class WithdrawlsScreen(tk.Frame):
    def withdrawals_screen():
        root = tk.Tk()
        root.title("Withdrawals Home Screen")
        root.geometry("1000x401")

        tk.Button(root, text="<-Back", bg="orange", command=root.destroy).pack(anchor='nw', padx=10, pady=10)
        tk.Label(root, text="Withdrawals", bg="purple", fg="white", font=("Arial", 14)).pack()

        frame = tk.Frame(root)
        frame.pack(pady=10)

        columns = ("DATE", "EMPNAME", "AMOUNT", "NOTES")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()

        tk.Button(root, text="Edit Table", bg="green").pack(side='left', padx=10, pady=10)
        tk.Button(root, text="Add row", bg="green").pack(side='right', padx=10, pady=10)

        root.mainloop()

    if __name__ == "__main__":
        withdrawals_screen()
