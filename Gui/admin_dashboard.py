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

        # 🌈 Get and apply current theme
        self.theme = master.get_theme()
        self.configure(bg=self.theme["bg"])
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.apply_theme()

    def create_widgets(self):
        self.title_label = tk.Label(
            self, text=f"👑 Welcome Admin {self.admin_name}!",
            font=("Helvetica", 16, "bold")
        )
        self.title_label.pack(pady=20)

        # Buttons frame
        self.button_frame = tk.Frame(self, bg=self.theme["bg"])
        self.button_frame.pack(pady=10)

        # Navigation Buttons
        self.books_btn = tk.Button(self.button_frame, text="📚 Manage Books", width=25,
                                   command=self.open_manage_books)
        self.users_btn = tk.Button(self.button_frame, text="👤 Manage Users", width=25,
                                   command=self.open_manage_users)
        self.analytics_btn = tk.Button(self.button_frame, text="📈 View Analytics", width=25,
                                       command=self.open_analytics)
        self.ai_btn = tk.Button(self.button_frame, text="🤖 AI Query Assistant", width=25,
                                command=self.open_ai_query)
        self.logout_btn = tk.Button(self.button_frame, text="🚪 Logout", width=25,
                                    command=self.logout)

        # Pack buttons vertically
        for btn in (self.books_btn, self.users_btn, self.analytics_btn, self.ai_btn, self.logout_btn):
            btn.pack(pady=8)

    def apply_theme(self):
        """Apply theme colors to dashboard widgets."""
        widgets = [self, self.title_label, self.button_frame,
                   self.books_btn, self.users_btn, self.analytics_btn,
                   self.ai_btn, self.logout_btn]

        for w in widgets:
            if isinstance(w, tk.Label):
                w.configure(bg=self.theme["bg"], fg=self.theme["fg"])
            elif isinstance(w, tk.Frame):
                w.configure(bg=self.theme["bg"])
            elif isinstance(w, tk.Button):
                w.configure(
                    bg=self.theme["button_bg"],
                    fg=self.theme["button_fg"],
                    activebackground=self.theme["fg"],
                    activeforeground=self.theme["bg"]
                )

    def open_manage_books(self):
        self.pack_forget()
        AdminBooksPage(self.master, self)

    def open_manage_users(self):
        self.pack_forget()
        AdminUsersPage(self.master, self)

    def open_analytics(self):
        self.pack_forget()
        AdminAnalytics(self.master, self)

    def open_ai_query(self):
        self.pack_forget()
        AdminAIPage(self.master, self)

    def logout(self):
        self.pack_forget()
        self.master.show_login()
