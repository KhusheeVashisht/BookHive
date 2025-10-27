import tkinter as tk
from tkinter import messagebox
from Gui.dashboard import DashboardPage
from Db_connect.db_test import create_connection

class LoginPage(tk.Frame):
    def __init__(self, master, switch_to_register, switch_to_admin_login=None):
        super().__init__(master)
        self.master = master
        self.switch_to_register = switch_to_register
        self.switch_to_admin_login = switch_to_admin_login
        self.theme = master.get_theme()  # get current theme
        self.configure(bg=self.theme["bg"])
        self.create_widgets()
        self.apply_theme()  # apply colors

    def create_widgets(self):
        self.title_label = tk.Label(self, text="BookHive Login", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=20)

        self.email_label = tk.Label(self, text="Email:")
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", command=self.login_user)
        self.login_button.pack(pady=20)

        self.register_button = tk.Button(self, text="Register", command=self.switch_to_register)
        self.register_button.pack(pady=10)

        if self.switch_to_admin_login:
            self.admin_button = tk.Button(self, text="Admin Login", fg="red", command=self.switch_to_admin_login)
            self.admin_button.pack(pady=10)

    def apply_theme(self):
        """Apply theme colors to all widgets."""
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
                self.destroy()
                DashboardPage(self.master, email)
            else:
                messagebox.showerror("Error", "Invalid email or password")
        except Exception as e:
            messagebox.showerror("Error", f"Database connection failed: {e}")
