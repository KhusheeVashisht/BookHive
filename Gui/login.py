import tkinter as tk
from tkinter import messagebox
from Gui.dashboard import DashboardPage
from Db_connect.db_test import create_connection

class LoginPage(tk.Frame):
    def __init__(self, master, switch_to_register, switch_to_admin_login=None):
        super().__init__(master)
        self.master = master
        self.switch_to_register = switch_to_register
        self.switch_to_admin_login = switch_to_admin_login  # optional callback
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="BookHive Login", font=("Helvetica", 18, "bold")).pack(pady=20)

        tk.Label(self, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        tk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", command=self.login_user).pack(pady=20)

        # Register button
        tk.Button(self, text="Register", command=self.switch_to_register).pack(pady=10)

        # Optional Admin Login button
        if self.switch_to_admin_login:
            tk.Button(self, text="Admin Login", fg="red", command=self.switch_to_admin_login).pack(pady=10)

    def login_user(self):
        email = self.email_entry.get().strip()
        pwd = self.password_entry.get().strip()

        if not (email and pwd):
            messagebox.showerror("Error", "Please enter both email and password")
            return

        try:
            conn = create_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE email=%s AND password=%s"
            cursor.execute(query, (email, pwd))
            result = cursor.fetchone()
            conn.close()

            if result:
                messagebox.showinfo("Success", f"Welcome {email}!")
                self.destroy()  # remove login frame
                DashboardPage(self.master, email)  # navigate to user dashboard
            else:
                messagebox.showerror("Error", "Invalid email or password")
        except Exception as e:
            messagebox.showerror("Error", f"Database connection failed: {e}")
