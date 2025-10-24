import tkinter as tk
from tkinter import messagebox, ttk
from Db_connect.db_test import create_connection

class AdminUsersPage(tk.Frame):
    def __init__(self, master, dashboard_frame):
        super().__init__(master)
        self.master = master
        self.dashboard_frame = dashboard_frame
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_users()

    def create_widgets(self):
        tk.Label(self, text="👥 Manage Users", font=("Helvetica", 16, "bold")).pack(pady=10)

        # CRUD buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Add User", command=lambda: self.user_window("Add User")).pack(side="left", padx=5)
        tk.Button(button_frame, text="Edit Selected User", command=self.edit_user_window).pack(side="left", padx=5)
        tk.Button(button_frame, text="Delete Selected User", command=self.delete_user).pack(side="left", padx=5)
        tk.Button(button_frame, text="← Back to Dashboard", command=self.back_to_dashboard).pack(side="left", padx=5)

        # Treeview to display users
        columns = ("user_id", "name", "email", "phone", "membership_type", "role")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            header = col.replace("_", " ").title()
            self.tree.heading(col, text=header)
        self.tree.pack(fill="both", expand=True, pady=10)

    def load_users(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, name, email, phone, membership_type, role FROM users")
            for user in cursor.fetchall():
                self.tree.insert("", "end", values=user)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {e}")

    def edit_user_window(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a user to edit")
            return
        values = self.tree.item(selected, "values")
        self.user_window("Edit User", values)

    def user_window(self, action, user=None):
        window = tk.Toplevel(self)
        window.title(action)
        window.geometry("400x450")

        labels = ["Name", "Email", "Phone", "Password", "Membership Type", "Role"]
        entries = {}

        for label in labels:
            tk.Label(window, text=f"{label}:").pack(pady=5)
            entry = tk.Entry(window)
            entry.pack(pady=5)
            entries[label] = entry

        # Pre-fill if editing
        if user:
            entries["Name"].insert(0, user[1])
            entries["Email"].insert(0, user[2])
            entries["Phone"].insert(0, user[3])
            entries["Membership Type"].insert(0, user[4])
            entries["Role"].insert(0, user[5])

        def save():
            name = entries["Name"].get().strip()
            email = entries["Email"].get().strip()
            phone = entries["Phone"].get().strip()
            password = entries["Password"].get().strip()
            membership = entries["Membership Type"].get().strip().lower()
            role = entries["Role"].get().strip().lower()

            if not (name and email and phone and membership and role):
                messagebox.showerror("Error", "All fields except password are required")
                return

            if membership not in ("regular", "premium"):
                messagebox.showerror("Error", "Membership type must be 'regular' or 'premium'")
                return

            if role not in ("user", "admin"):
                messagebox.showerror("Error", "Role must be 'user' or 'admin'")
                return

            if not phone.isdigit():
                messagebox.showerror("Error", "Phone must be numeric")
                return

            try:
                conn = create_connection()
                cursor = conn.cursor()
                if action == "Add User":
                    cursor.execute(
                        "INSERT INTO users (name, email, phone, password, membership_type, role) VALUES (%s, %s, %s, %s, %s, %s)",
                        (name, email, phone, password or "1234", membership, role)
                    )
                elif action == "Edit User" and user:
                    if password:
                        cursor.execute(
                            "UPDATE users SET name=%s, email=%s, phone=%s, password=%s, membership_type=%s, role=%s WHERE user_id=%s",
                            (name, email, phone, password, membership, role, user[0])
                        )
                    else:
                        cursor.execute(
                            "UPDATE users SET name=%s, email=%s, phone=%s, membership_type=%s, role=%s WHERE user_id=%s",
                            (name, email, phone, membership, role, user[0])
                        )
                conn.commit()
                conn.close()
                self.load_users()
                window.destroy()
                messagebox.showinfo("Success", f"{action} successful!")
            except Exception as e:
                messagebox.showerror("Error", f"{action} failed: {e}")

        tk.Button(window, text="Save", command=save).pack(pady=20)

    def delete_user(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a user to delete")
            return
        user_id = self.tree.item(selected, "values")[0]
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this user?")
        if confirm:
            try:
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
                conn.commit()
                conn.close()
                self.load_users()
                messagebox.showinfo("Success", "User deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Delete failed: {e}")

    def back_to_dashboard(self):
        self.pack_forget()
        self.dashboard_frame.pack(fill="both", expand=True)
