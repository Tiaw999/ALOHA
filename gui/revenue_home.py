import tkinter as tk


class RevenueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Revenue Home Screen")
        self.root.geometry("600x400")

        # Store Name Label
        tk.Label(root, text="Store Name", font=("Arial", 14, "bold")).grid(row=0, column=1, columnspan=2, pady=10)

        # Back Button
        tk.Button(root, text="<- Back", bg="orange", fg="black", font=("Arial", 12)).grid(row=1, column=0, padx=10,
                                                                                          pady=5)

        # Revenue Button
        tk.Button(root, text="Revenue", bg="red", fg="white", font=("Arial", 12)).grid(row=1, column=2, padx=10, pady=5)

        # Table (Treeview)
        columns = ("Date", "Reg", "Credit", "Cash in Envelope")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Edit Table Button
        tk.Button(root, text="Edit Table", bg="green", fg="white", font=("Arial", 12), command=self.edit_table).grid(
            row=3, column=1, pady=5)

        # Add Row Button
        tk.Button(root, text="Add Row", bg="green", fg="white", font=("Arial", 12), command=self.add_row).grid(row=3,
                                                                                                               column=2,
                                                                                                               pady=5)

    def add_row(self):
        """Adds an empty row to the table."""
        self.tree.insert("", "end", values=("", "", "", ""))

    def edit_table(self):
        """Function to handle editing (placeholder for actual implementation)."""
        print("Edit table clicked")


if __name__ == "__main__":
    root = tk.Tk()
    app = RevenueApp(root)
    root.mainloop()
