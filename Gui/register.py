import tkinter as tk
from tkinter import messagebox
from Db_connect.db_test import create_connection

class RegistrationPage(tk.Frame):
    def __init__(self, master, switch_to_login):
        super().__init__(master)
        self.master = master
        self.switch_to_login = switch_to_login
        self.theme = master.get_theme()
        self.configure(bg=self.theme["bg"])
        self.pack()
        self.create_widgets()
        self.apply_theme()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="BookHive Registration", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=20)

        self.name_label = tk.Label(self, text="Name:")
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.email_label = tk.Label(self, text="Email:")
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        self.phone_label = tk.Label(self, text="Phone:")
        self.phone_label.pack(pady=5)
        self.phone_entry = tk.Entry(self)
        self.phone_entry.pack()

        self.mem_label = tk.Label(self, text="Membership Type:")
        self.mem_label.pack(pady=5)
        self.membership_var = tk.StringVar(value="regular")
        self.regular_radio = tk.Radiobutton(self, text="Regular", variable=self.membership_var, value="regular", bg=self.theme["bg"])
        self.premium_radio = tk.Radiobutton(self, text="Premium", variable=self.membership_var, value="premium", bg=self.theme["bg"])
        self.regular_radio.pack()
        self.premium_radio.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.register_button = tk.Button(self, text="Register", command=self.register_user)
        self.register_button.pack(pady=20)
        self.back_button = tk.Button(self, text="Back to Login", command=self.switch_to_login)
        self.back_button.pack(pady=10)

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
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Email already registered!")
                conn.close()
                return

            query = """
            INSERT INTO users (name, email, phone, membership_type, password)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, email, phone, membership, password))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"User {name} registered successfully!")
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.switch_to_login()

        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")
