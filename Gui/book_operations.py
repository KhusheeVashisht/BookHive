import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from Db_connect.db_test import create_connection

class BookOperations(tk.Frame):
    def __init__(self, master, user_id, user_email):
        super().__init__(master)
        self.master = master
        self.user_id = user_id
        self.user_email = user_email
        self.theme = master.get_theme()
        self.configure(bg=self.theme["bg"])
        self.pack(fill="both", expand=True)

        tk.Label(
            self, text=f"📚 Welcome, {self.user_email}",
            font=("Helvetica", 16, "bold"), bg=self.theme["bg"], fg=self.theme["fg"]
        ).pack(pady=10)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.view_books_tab(notebook)
        self.rent_book_tab(notebook)
        self.my_rentals_tab(notebook)
        self.ai_recommend_tab(notebook)

        tk.Button(
            self, text="⬅ Back to Dashboard",
            bg=self.theme["button_bg"], fg=self.theme["button_fg"],
            activebackground=self.theme["fg"], activeforeground=self.theme["bg"],
            command=self.back_to_dashboard
        ).pack(pady=10)

    # --- Tabs ---
    def view_books_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="View Books")

        cols = ("ID", "Title", "Author", "Category", "Price", "Available")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=10)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Refresh Books", command=self.load_books).pack(pady=5)
        self.load_books()

    def load_books(self):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT book_id, title, author, category, price, available_copies FROM books")
            rows = cursor.fetchall()
            conn.close()

            for i in self.tree.get_children():
                self.tree.delete(i)
            for row in rows:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load books: {e}")

    def rent_book_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Rent a Book")

        ttk.Label(frame, text="Enter Book ID:").pack(pady=5)
        self.book_id_entry = ttk.Entry(frame)
        self.book_id_entry.pack(pady=5)

        ttk.Button(frame, text="Rent", command=self.rent_book).pack(pady=10)

    def rent_book(self):
        book_id = self.book_id_entry.get().strip()
        if not book_id:
            messagebox.showerror("Error", "Please enter a Book ID.")
            return
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT available_copies FROM books WHERE book_id=%s", (book_id,))
            book = cursor.fetchone()
            if not book:
                messagebox.showerror("Error", "Book not found.")
                conn.close()
                return
            if book[0] <= 0:
                messagebox.showerror("Error", "Book not available.")
                conn.close()
                return

            cursor.execute(
                "SELECT rental_id FROM rentals WHERE user_id=%s AND book_id=%s AND return_date IS NULL",
                (self.user_id, book_id)
            )
            active_rental = cursor.fetchone()
            if active_rental:
                messagebox.showwarning("Warning", "You already have this book rented.")
                conn.close()
                return

            due_date = datetime.now() + timedelta(days=7)
            cursor.execute(
                "INSERT INTO rentals (user_id, book_id, rent_date, due_date, fine) VALUES (%s, %s, %s, %s, %s)",
                (self.user_id, book_id, datetime.now().date(), due_date.date(), 0.00)
            )
            cursor.execute(
                "UPDATE books SET available_copies = available_copies - 1 WHERE book_id = %s",
                (book_id,)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Book ID {book_id} rented successfully!\nDue date: {due_date.date()}")
        except Exception as e:
            messagebox.showerror("Error", f"Rental failed: {e}")

    def my_rentals_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="My Rentals")

        ttk.Label(frame, text="📋 View your current and past rentals",
                  font=("Helvetica", 12, "bold")).pack(pady=10)

        cols = ("Book Title", "Rent Date", "Due Date", "Return Date", "Fine (₹)", "Status")
        self.rentals_tree = ttk.Treeview(frame, columns=cols, show="headings", height=8)
        for col in cols:
            self.rentals_tree.heading(col, text=col)
            self.rentals_tree.column(col, width=120, anchor="center")
        self.rentals_tree.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="🔄 Refresh", command=self.load_user_rentals).pack(pady=5)
        self.load_user_rentals()

    def load_user_rentals(self):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.title, r.rent_date, r.due_date, r.return_date, r.fine
                FROM rentals r JOIN books b ON r.book_id = b.book_id
                WHERE r.user_id = %s ORDER BY r.rent_date DESC
            """, (self.user_id,))
            rows = cursor.fetchall()
            conn.close()
            for i in self.rentals_tree.get_children():
                self.rentals_tree.delete(i)
            today = datetime.now().date()
            for row in rows:
                title, rent_date, due_date, return_date, fine = row
                rent_date = rent_date.strftime("%Y-%m-%d") if rent_date else "-"
                due_date_display = due_date.strftime("%Y-%m-%d") if due_date else "-"
                return_date_display = return_date.strftime("%Y-%m-%d") if return_date else "-"
                if return_date:
                    status = "✅ Returned"
                elif due_date and due_date < today:
                    status = "⚠️ Overdue"
                elif due_date and (due_date - today).days <= 2:
                    status = "🕓 Due soon"
                else:
                    status = "📖 Active"
                self.rentals_tree.insert("", "end", values=(
                    title, rent_date, due_date_display, return_date_display, f"{fine:.2f}", status
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load rentals: {e}")

    def ai_recommend_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="AI Recommendations")

        ttk.Label(frame, text="📖 Personalized Book Suggestions", font=("Helvetica", 12, "bold")).pack(pady=10)
        ttk.Button(frame, text="✨ Get Recommendations", command=self.show_recommendations).pack(pady=10)

        cols = ("Title", "Author", "Category")
        self.recommend_tree = ttk.Treeview(frame, columns=cols, show="headings", height=8)
        for col in cols:
            self.recommend_tree.heading(col, text=col)
            self.recommend_tree.column(col, width=150, anchor="center")
        self.recommend_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def show_recommendations(self):
        from ai_features import recommend_books
        try:
            books, reason = recommend_books(self.user_id)
            for i in self.recommend_tree.get_children():
                self.recommend_tree.delete(i)
            if not books:
                self.recommend_tree.insert("", "end", values=("No recommendations available", "", ""))
                return
            for book in books:
                self.recommend_tree.insert("", "end", values=book)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load recommendations: {e}")

    def back_to_dashboard(self):
        from Gui.dashboard import DashboardPage
        self.destroy()
        DashboardPage(self.master, self.user_email)
