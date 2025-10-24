import tkinter as tk
from tkinter import ttk, messagebox
from ai_features import admin_ai_query  

class AdminAIPage(tk.Frame):
    def __init__(self, master, dashboard):
        super().__init__(master)
        self.master = master
        self.dashboard = dashboard
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="🤖 BookHive AI Query Assistant", font=("Helvetica", 16, "bold")).pack(pady=15)

        self.query_entry = tk.Entry(self, width=60, font=("Arial", 12))
        self.query_entry.pack(pady=10)
        tk.Button(self, text="Ask AI", command=self.process_query, width=20).pack(pady=5)

        self.result_tree = ttk.Treeview(self, columns=("col1", "col2"), show="headings", height=10)
        self.result_tree.pack(pady=10)

        self.status_label = tk.Label(self, text="", font=("Arial", 11))
        self.status_label.pack(pady=5)

        tk.Button(self, text="⬅️ Back", command=self.go_back, width=20).pack(pady=10)

    def process_query(self):
        query = self.query_entry.get().strip()
        if not query:
            messagebox.showwarning("Empty", "Please enter a question.")
            return

        headers, data, message = admin_ai_query(query)

        # Clear old data
        for col in self.result_tree["columns"]:
            self.result_tree.heading(col, text="")
        for row in self.result_tree.get_children():
            self.result_tree.delete(row)

        # Update new data
        if headers:
            self.result_tree["columns"] = [f"col{i}" for i in range(len(headers))]
            for i, header in enumerate(headers):
                self.result_tree.heading(f"col{i}", text=header)
            for row in data:
                self.result_tree.insert("", "end", values=row)
        else:
            self.result_tree.insert("", "end", values=("No data found", ""))

        self.status_label.config(text=message)
        self.query_entry.delete(0, tk.END)

    def go_back(self):
        self.pack_forget()
        self.dashboard.pack(fill="both", expand=True)
