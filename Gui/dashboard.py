import tkinter as tk
from Gui.book_operations import BookOperations
from Analytics.plots import UserAnalytics
from Db_connect.db_test import create_connection

class DashboardPage(tk.Frame):
    def __init__(self, master, email):
        super().__init__(master)
        self.master = master
        self.email = email
        self.theme = master.get_theme()
        self.configure(bg=self.theme["bg"])
        self.pack(fill="both", expand=True)

        self.user_id, self.username = self.get_user_info(email)
        self.create_widgets()
        self.apply_theme()

    def get_user_info(self, email):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, name FROM users WHERE email=%s", (email,))
            result = cursor.fetchone()
            conn.close()
            return result if result else (None, email)
        except Exception as e:
            print("Error fetching user info:", e)
            return None, email

    def create_widgets(self):
        self.title_label = tk.Label(
            self, text=f"📊 Welcome {self.username}!",
            font=("Helvetica", 16, "bold")
        )
        self.title_label.pack(pady=20)

        self.book_button = tk.Button(
            self, text="📚 Book Operations", width=20,
            command=self.open_book_operations
        )
        self.book_button.pack(pady=10)

        self.analytics_button = tk.Button(
            self, text="📈 View My Analytics", width=20,
            command=self.show_dashboard
        )
        self.analytics_button.pack(pady=10)

        self.logout_button = tk.Button(
            self, text="🚪 Logout", width=20,
            command=self.logout
        )
        self.logout_button.pack(pady=20)

    def apply_theme(self):
        for w in self.winfo_children():
            if isinstance(w, tk.Label):
                w.configure(bg=self.theme["bg"], fg=self.theme["fg"])
            elif isinstance(w, tk.Button):
                w.configure(
                    bg=self.theme["button_bg"],
                    fg=self.theme["button_fg"],
                    activebackground=self.theme["fg"],
                    activeforeground=self.theme["bg"]
                )

    def open_book_operations(self):
        self.pack_forget()
        BookOperations(self.master, self.user_id, self.email)

    def show_dashboard(self):
        if self.user_id:
            self.pack_forget()
            self.analytics_frame = UserAnalytics(
                self.master, self.user_id, self.username,
                switch_to_dashboard=self.back_to_dashboard
            )
            self.analytics_frame.pack(fill="both", expand=True)
        else:
            tk.messagebox.showerror("Error", "User information not found.")

    def back_to_dashboard(self):
        if hasattr(self, "analytics_frame"):
            self.analytics_frame.pack_forget()
            self.analytics_frame.destroy()
        self.pack(fill="both", expand=True)

    def logout(self):
        self.pack_forget()
        self.master.show_login()
