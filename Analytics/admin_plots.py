import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Db_connect.db_test import create_connection

class AdminAnalytics(tk.Frame):
    def __init__(self, master, dashboard_frame):
        super().__init__(master)
        self.master = master
        self.dashboard_frame = dashboard_frame
        self.pack(fill="both", expand=True)
        self.chart_canvas = None

        # Consistent color palette
        self.colors = {
            "rented": "#9b59b6",
            "purchased": "#2ecc71",
            "membership": ["#f39c12", "#8e44ad"]
        }

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="📈 Admin Analytics", font=("Helvetica", 16, "bold")).pack(pady=20)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Top 5 Rented Books", width=25, command=self.top_rented_books).pack(side="left", padx=5)
        tk.Button(button_frame, text="Top 5 Purchased Books", width=25, command=self.top_purchased_books).pack(side="left", padx=5)
        tk.Button(button_frame, text="Membership Distribution", width=25, command=self.membership_distribution).pack(side="left", padx=5)
        tk.Button(button_frame, text="← Back to Dashboard", width=25, command=self.back_to_dashboard).pack(side="left", padx=5)

        self.chart_frame = tk.Frame(self)
        self.chart_frame.pack(fill="both", expand=True, pady=20)

    def clear_chart(self):
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()
            self.chart_canvas = None

    def top_rented_books(self):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.title, COUNT(r.rental_id) AS total_rented
                FROM rentals r
                JOIN books b ON r.book_id = b.book_id
                GROUP BY r.book_id
                ORDER BY total_rented DESC
                LIMIT 5
            """)
            data = cursor.fetchall()
            conn.close()

            if not data:
                messagebox.showinfo("Info", "No rental data available.")
                return

            titles, counts = zip(*data)

            self.clear_chart()
            fig, ax = plt.subplots(figsize=(8,5))
            bars = ax.bar(titles, counts, color=self.colors["rented"])
            ax.set_xlabel("Book Titles")
            ax.set_ylabel("Times Rented")
            ax.set_title("Top 5 Rented Books")
            ax.set_xticklabels(titles, rotation=45, ha="right")

            # Add counts on top of bars
            for bar in bars:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), str(int(bar.get_height())), ha='center', va='bottom')

            fig.tight_layout()
            self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            self.chart_canvas.draw()
            self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch rented books: {e}")

    def top_purchased_books(self):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.title, COUNT(t.transaction_id) AS total_purchased
                FROM transactions t
                JOIN books b ON t.book_id = b.book_id
                GROUP BY t.book_id
                ORDER BY total_purchased DESC
                LIMIT 5
            """)
            data = cursor.fetchall()
            conn.close()

            if not data:
                messagebox.showinfo("Info", "No purchase data available.")
                return

            titles, counts = zip(*data)

            self.clear_chart()
            fig, ax = plt.subplots(figsize=(8,5))
            bars = ax.bar(titles, counts, color=self.colors["purchased"])
            ax.set_xlabel("Book Titles")
            ax.set_ylabel("Times Purchased")
            ax.set_title("Top 5 Purchased Books")
            ax.set_xticklabels(titles, rotation=45, ha="right")

            # Add counts on top of bars
            for bar in bars:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), str(int(bar.get_height())), ha='center', va='bottom')

            fig.tight_layout()
            self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            self.chart_canvas.draw()
            self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch purchased books: {e}")

    def membership_distribution(self):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT membership_type, COUNT(*) 
                FROM users
                GROUP BY membership_type
            """)
            data = cursor.fetchall()
            conn.close()

            if not data:
                messagebox.showinfo("Info", "No user data available.")
                return

            labels, counts = zip(*data)

            self.clear_chart()
            fig, ax = plt.subplots(figsize=(6,6))
            ax.pie(counts, labels=labels, autopct="%1.1f%%", colors=self.colors["membership"], startangle=90)
            ax.set_title("Membership Distribution")
            fig.tight_layout()

            self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            self.chart_canvas.draw()
            self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch membership data: {e}")

    def back_to_dashboard(self):
        self.clear_chart()
        self.pack_forget()
        self.dashboard_frame.pack(fill="both", expand=True)
