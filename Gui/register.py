import tkinter as tk
from tkinter import messagebox
from Db_connect.db_test import create_connection

class RegistrationPage(tk.Frame):
    def __init__(self, master, switch_to_login):
        super().__init__(master)
        self.master = master
        self.switch_to_login = switch_to_login
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="BookHive Registration", font=("Helvetica", 18, "bold")).pack(pady=20)

        # Name
        tk.Label(self, text="Name:").pack(pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        # Email
        tk.Label(self, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        # Phone
        tk.Label(self, text="Phone:").pack(pady=5)
        self.phone_entry = tk.Entry(self)
        self.phone_entry.pack()

        # Membership Type
        tk.Label(self, text="Membership Type:").pack(pady=5)
        self.membership_var = tk.StringVar(value="regular")
        tk.Radiobutton(self, text="Regular", variable=self.membership_var, value="regular").pack()
        tk.Radiobutton(self, text="Premium", variable=self.membership_var, value="premium").pack()

        # Password
        tk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        # Register Button
        tk.Button(self, text="Register", command=self.register_user).pack(pady=20)

        # Back to Login Button inside the frame
        tk.Button(self, text="Back to Login", command=self.switch_to_login).pack(pady=10)

    def register_user(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        membership = self.membership_var.get()
        password = self.password_entry.get().strip()

        if not (name and email and password):
            messagebox.showerror("Error", "Name, Email and Password are required")
            return

        try:
            conn = create_connection()
            cursor = conn.cursor()

            # Check for duplicate email
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Email already registered!")
                conn.close()
                return

            # Insert new user
            query = """
            INSERT INTO users (name, email, phone, membership_type, password)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, email, phone, membership, password))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"User {name} registered successfully!")
            # Clear fields after registration
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

            # Switch back to login page
            self.switch_to_login()

        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")
