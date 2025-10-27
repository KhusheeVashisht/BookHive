import tkinter as tk
from tkinter import messagebox
from Db_connect.db_test import create_connection
from Gui.admin_dashboard import AdminDashboardPage  # we’ll create this next

class AdminLoginPage(tk.Frame):
    def __init__(self, master, switch_to_user_login):
        super().__init__(master)
        self.master = master
        self.switch_to_user_login = switch_to_user_login
        self.theme = master.get_theme()  # get current theme
        self.configure(bg=self.theme["bg"])
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.apply_theme()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="BookHive Admin Login", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=20)

        self.email_label = tk.Label(self, text="Email:")
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", command=self.login_admin)
        self.login_button.pack(pady=20)

        self.switch_button = tk.Button(self, text="← User Login", command=self.switch_to_user_login)
        self.switch_button.pack(pady=10)

    def apply_theme(self):
        """Apply theme colors to all widgets for visual consistency."""
        widgets = self.winfo_children()
        for w in widgets:
            if isinstance(w, tk.Label):
                w.configure(bg=self.theme["bg"], fg=self.theme["fg"])
            elif isinstance(w, tk.Entry):
                w.configure(bg="white")
            elif isinstance(w, tk.Button):
                w.configure(
                    bg=self.theme["button_bg"],
                    fg=self.theme["button_fg"],
                    activebackground=self.theme["fg"],
                    activeforeground=self.theme["bg"]
                )

    def login_admin(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showerror("Error", "Email and Password are required")
            return

        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id, name FROM users WHERE email=%s AND password=%s AND role='admin'",
                (email, password)
            )
            result = cursor.fetchone()
            conn.close()

            if result:
                user_id, name = result
                messagebox.showinfo("Success", f"Welcome Admin {name}!")
                self.pack_forget()
                AdminDashboardPage(self.master, user_id, name)
            else:
                messagebox.showerror("Error", "Invalid admin credentials")
        except Exception as e:
            messagebox.showerror("Database Error", f"Error: {e}")
