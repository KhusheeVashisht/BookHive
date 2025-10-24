import tkinter as tk
from Gui.book_operations import BookOperations
from Analytics.plots import UserAnalytics
from Db_connect.db_test import create_connection

class DashboardPage(tk.Frame):
    def __init__(self, master, email):
        super().__init__(master)
        self.master = master
        self.email = email
        self.pack(fill="both", expand=True)

        # Fetch both user_id and name
        self.user_id, self.username = self.get_user_info(email)
        self.create_widgets()

    def get_user_info(self, email):
        """Fetch user_id and name from the database using email."""
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, name FROM users WHERE email=%s", (email,))
            result = cursor.fetchone()
            conn.close()

            if result:
                return result[0], result[1]  # (user_id, name)
            else:
                return None, email  # fallback
        except Exception as e:
            print("Error fetching user info:", e)
            return None, email

    def create_widgets(self):
        tk.Label(
            self, text=f"📊 Welcome {self.username}!",
            font=("Helvetica", 16, "bold")
        ).pack(pady=20)

        tk.Button(
            self, text="📚 Book Operations", width=20,
            command=self.open_book_operations
        ).pack(pady=10)

        tk.Button(
            self, text="📈 View My Analytics", width=20,
            command=self.show_dashboard
        ).pack(pady=10)

        tk.Button(
            self, text="🚪 Logout", width=20,
            command=self.logout
        ).pack(pady=20)

    def open_book_operations(self):
        self.pack_forget()
        # Pass both user_id (for DB) and email (for display)
        BookOperations(self.master, self.user_id, self.email)
 # not username


    def show_dashboard(self):
        if self.user_id:
            # Hide current dashboard frame
            self.pack_forget()

            # Create the analytics frame and store it
            self.analytics_frame = UserAnalytics(
                self.master, self.user_id, self.username,
                switch_to_dashboard=self.back_to_dashboard
            )
            self.analytics_frame.pack(fill="both", expand=True)
        else:
            tk.messagebox.showerror("Error", "User information not found.")

    def back_to_dashboard(self):
        # Hide the analytics frame
        if hasattr(self, "analytics_frame"):
            self.analytics_frame.pack_forget()
            self.analytics_frame.destroy()
            del self.analytics_frame

        # Show this dashboard again
        self.pack(fill="both", expand=True)



    def logout(self):
        """Return to the login page"""
        self.pack_forget()
        self.master.show_login()
