import tkinter as tk
from tkinter import messagebox
from Gui.admin_books import AdminBooksPage
from Gui.admin_users import AdminUsersPage
from Analytics.admin_plots import AdminAnalytics
from admin_ai_query import AdminAIPage


class AdminDashboardPage(tk.Frame):
    def __init__(self, master, admin_id, admin_name):
        super().__init__(master)
        self.master = master
        self.admin_id = admin_id
        self.admin_name = admin_name
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(
            self, text=f"👑 Welcome Admin {self.admin_name}!",
            font=("Helvetica", 16, "bold")
        ).pack(pady=20)

        tk.Button(
            self, text="📚 Manage Books", width=25,
            command=self.open_manage_books
        ).pack(pady=10)

        tk.Button(
            self, text="👤 Manage Users", width=25,
            command=self.open_manage_users
        ).pack(pady=10)

        tk.Button(
            self, text="📈 View Analytics", width=25,
            command=self.open_analytics
        ).pack(pady=10)

        # ✅ NEW AI CHAT BUTTON
        tk.Button(
            self, text="🤖 AI Query Assistant", width=25,
            command=self.open_ai_query
        ).pack(pady=10)

        tk.Button(
            self, text="🚪 Logout", width=25,
            command=self.logout
        ).pack(pady=20)

    def open_manage_books(self):
        self.pack_forget()
        AdminBooksPage(self.master, self)  # Pass dashboard as callback for Back button

    def open_manage_users(self):
        self.pack_forget()
        AdminUsersPage(self.master, self)  # Pass dashboard as callback for Back button

    def open_analytics(self):
        self.pack_forget()
        AdminAnalytics(self.master, self)  # Pass dashboard as callback for Back button

    # ✅ NEW FUNCTION TO OPEN AI PAGE
    def open_ai_query(self):
        self.pack_forget()
        AdminAIPage(self.master, self)

    def logout(self):
        self.pack_forget()
        self.master.show_login()  # Return to main user login
