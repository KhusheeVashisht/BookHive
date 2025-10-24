import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mysql.connector

class UserAnalytics(tk.Frame):
    def __init__(self, master, user_id, username, switch_to_dashboard):
        super().__init__(master)
        self.master = master
        self.user_id = user_id
        self.username = username
        self.switch_to_dashboard = switch_to_dashboard  # callback to dashboard
        self.pack(fill="both", expand=True)
        self.configure(bg="#f4f1fe")  # light purple background
        self.create_widgets()

    def create_widgets(self):
        # Title frame with Back button
        title_frame = tk.Frame(self, bg="#f4f1fe")
        title_frame.pack(fill="x", pady=10)

        tk.Button(title_frame, text="← Back to Dashboard", command=self.switch_to_dashboard,
                  bg="#9b59b6", fg="white", font=("Helvetica", 10, "bold")).pack(side="left", padx=20)

        tk.Label(
            title_frame,
            text=f"📈 Analytics for {self.username}",
            font=("Helvetica", 18, "bold"),
            bg="#f4f1fe",
            fg="#4b0082"
        ).pack(side="left", padx=20)

        # Fetch user data
        rented, returned, pending, purchased, fines = self.get_user_data()

        # Summary cards frame
        summary_frame = tk.Frame(self, bg="#f4f1fe")
        summary_frame.pack(pady=10)

        cards = [
            ("Books Rented", rented, "#dcd6f7"),
            ("Books Purchased", purchased, "#c2f0c2"),
            ("Books Returned", returned, "#fce2ce"),
            ("Pending Returns", pending, "#f7caca"),
            ("Fines", fines, "#f0c2f0")
        ]

        for title, value, color in cards:
            card = tk.Frame(summary_frame, bg=color, relief="ridge", bd=2, padx=15, pady=10)
            card.pack(side="left", padx=10)
            tk.Label(card, text=title, font=("Helvetica", 12, "bold"), bg=color).pack()
            tk.Label(card, text=value, font=("Helvetica", 14), bg=color).pack()

        # Charts frame
        chart_frame = tk.Frame(self, bg="#f4f1fe")
        chart_frame.pack(fill="both", expand=True, pady=20)

        self.plot_graphs(chart_frame, rented, purchased, returned, pending)

    def get_user_data(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # change if needed
                database="bookhive_db"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM rentals WHERE user_id = %s", (self.user_id,))
            rented = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM rentals WHERE user_id = %s AND return_date IS NOT NULL", (self.user_id,))
            returned = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM rentals WHERE user_id = %s AND return_date IS NULL", (self.user_id,))
            pending = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM transactions WHERE user_id = %s", (self.user_id,))
            purchased = cursor.fetchone()[0]

            fines = 0  # Replace with real fines calculation if available

            conn.close()
            return rented, returned, pending, purchased, fines
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error fetching user info: {e}")
            return 0, 0, 0, 0, 0

    def plot_graphs(self, frame, rented, purchased, returned, pending):
        fig, axs = plt.subplots(1, 2, figsize=(10, 5), facecolor="#f4f1fe")

        if rented + purchased == 0:
            rented, purchased = 1, 1
        if returned + pending == 0:
            returned, pending = 1, 1

        axs[0].bar(["Rented", "Purchased"], [rented, purchased], color=["#9b59b6", "#2ecc71"])
        axs[0].set_title("Books Rented vs Purchased", fontsize=12, color="#4b0082")
        axs[0].set_facecolor("#f4f1fe")
        axs[0].tick_params(colors="#4b0082")

        labels = ["Returned", "Pending"]
        sizes = [returned, pending]
        colors = ["#8e44ad", "#f39c12"]
        axs[1].pie(
            sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors,
            textprops={'color':"#4b0082"}
        )
        axs[1].set_title("Return Status", fontsize=12, color="#4b0082")

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
