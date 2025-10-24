import tkinter as tk
from tkinter import messagebox
from Db_connect.db_test import create_connection
from Gui.admin_dashboard import AdminDashboardPage  # we’ll create this next

class AdminLoginPage(tk.Frame):
    def __init__(self, master, switch_to_user_login):
        super().__init__(master)
        self.master = master
        self.switch_to_user_login = switch_to_user_login
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="BookHive Admin Login", font=("Helvetica", 18, "bold")).pack(pady=20)

        tk.Label(self, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        tk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", command=self.login_admin).pack(pady=20)

        # Switch back to user login
        tk.Button(self, text="← User Login", command=self.switch_to_user_login).pack(pady=10)

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
