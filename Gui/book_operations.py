import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from Db_connect.db_test import create_connection

class BookOperations(tk.Frame):
    def __init__(self, master, user_id, user_email):
        super().__init__(master)
        self.master = master
        self.user_id = user_id          # numeric user_id for DB queries
        self.user_email = user_email    # email to display
        self.pack(fill="both", expand=True)

        tk.Label(
            self, text=f"📚 Welcome, {self.user_email}", 
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)

        # Notebook for tabs
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabs
        self.view_books_tab(notebook)
        self.rent_book_tab(notebook)
        self.return_book_tab(notebook)
        self.ai_recommend_tab(notebook)


        tk.Button(self, text="⬅ Back to Dashboard", command=self.back_to_dashboard).pack(pady=10)

    # ----------------- TAB 1: View Books -----------------
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

    # ----------------- TAB 2: Rent Book -----------------
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

            # Use user_id directly (already passed from Dashboard)
            user_id = self.user_id

            # Check book availability
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

            # Check if user already rented this book and hasn't returned it yet
            cursor.execute(
                "SELECT rental_id FROM rentals WHERE user_id=%s AND book_id=%s AND return_date IS NULL",
                (user_id, book_id)
            )
            active_rental = cursor.fetchone()
            if active_rental:
                messagebox.showwarning("Warning", "You already have this book rented.")
                conn.close()
                return

            # Calculate due date (e.g., 7 days from now)
            due_date = datetime.now() + timedelta(days=7)

            # Insert rental record
            cursor.execute(
                "INSERT INTO rentals (user_id, book_id, rent_date, due_date, fine) VALUES (%s, %s, %s, %s, %s)",
                (user_id, book_id, datetime.now().date(), due_date.date(), 0.00)
            )

            # Update book availability
            cursor.execute(
                "UPDATE books SET available_copies = available_copies - 1 WHERE book_id = %s",
                (book_id,)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Book ID {book_id} rented successfully!\nDue date: {due_date.date()}")

        except Exception as e:
            messagebox.showerror("Error", f"Rental failed: {e}")

    # ----------------- TAB 3: Return Book -----------------
    def return_book_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Return Book")

        ttk.Label(frame, text="Enter Book ID to Return:").pack(pady=5)
        self.return_book_id_entry = ttk.Entry(frame)
        self.return_book_id_entry.pack(pady=5)

        ttk.Button(frame, text="Return", command=self.return_book).pack(pady=10)

    def return_book(self):
        book_id = self.return_book_id_entry.get().strip()
        if not book_id:
            messagebox.showerror("Error", "Please enter a Book ID.")
            return

        try:
            conn = create_connection()
            cursor = conn.cursor()

            user_id = self.user_id

            # Find active rental
            cursor.execute(
                "SELECT rental_id, rent_date, due_date FROM rentals WHERE user_id=%s AND book_id=%s AND return_date IS NULL",
                (user_id, book_id)
            )
            rental = cursor.fetchone()
            if not rental:
                messagebox.showerror("Error", "No active rental found for this book.")
                conn.close()
                return

            rental_id, rent_date, due_date = rental

            # Calculate fine if returned late
            today = datetime.now().date()
            fine = 0.0
            if today > due_date:
                days_late = (today - due_date).days
                fine = round(days_late * 5.0, 2)  # ₹5 per day fine (example)

            # Update rental record
            cursor.execute(
                "UPDATE rentals SET return_date=%s, fine=%s WHERE rental_id=%s",
                (today, fine, rental_id)
            )

            # Update book availability
            cursor.execute(
                "UPDATE books SET available_copies = available_copies + 1 WHERE book_id = %s",
                (book_id,)
            )

            conn.commit()
            conn.close()

            msg = f"Book ID {book_id} returned successfully!"
            if fine > 0:
                msg += f"\nLate fee: ₹{fine}"
            messagebox.showinfo("Success", msg)

        except Exception as e:
            messagebox.showerror("Error", f"Return failed: {e}")

            # ----------------- TAB 4: AI Book Recommendations -----------------
    def ai_recommend_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="AI Recommendations")

        ttk.Label(
            frame,
            text="📖 Personalized Book Suggestions Based on Your Reading History",
            font=("Helvetica", 12, "bold")
        ).pack(pady=10)

        ttk.Button(
            frame, text="✨ Get Recommendations", command=self.show_recommendations
        ).pack(pady=10)

        cols = ("Title", "Author", "Category")
        self.recommend_tree = ttk.Treeview(frame, columns=cols, show="headings", height=8)
        for col in cols:
            self.recommend_tree.heading(col, text=col)
            self.recommend_tree.column(col, width=150, anchor="center")
        self.recommend_tree.pack(fill="both", expand=True, padx=10, pady=10)

    # ✅ UNINDENT THIS COMPLETELY so it’s at the same level as `def ai_recommend_tab`
    def show_recommendations(self):
        from ai_features import recommend_books
        try:
            # Get recommended books and reason
            books, reason = recommend_books(self.user_id)

            # Clear old recommendations
            for i in self.recommend_tree.get_children():
                self.recommend_tree.delete(i)

            # Handle empty result
            if not books:
                self.recommend_tree.insert("", "end", values=("No recommendations available", "", ""))
                if hasattr(self, "reason_label"):
                    self.reason_label.config(text="❌ No data available for recommendations.")
                else:
                    self.reason_label = ttk.Label(
                        self.recommend_tree.master,
                        text="❌ No data available for recommendations.",
                        foreground="red"
                    )
                    self.reason_label.pack(pady=5)
                return

            # Insert new results
            for book in books:
                self.recommend_tree.insert("", "end", values=book)

            # Display reason below the table
            if hasattr(self, "reason_label"):
                self.reason_label.config(text=f"💡 {reason}")
            else:
                self.reason_label = ttk.Label(
                    self.recommend_tree.master,
                    text=f"💡 {reason}",
                    foreground="blue"
                )
                self.reason_label.pack(pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load recommendations: {e}")
    # ----------------- TAB 4: AI Book Recommendations -----------------
    def ai_recommend_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="AI Recommendations")

        ttk.Label(
            frame,
            text="📖 Personalized Book Suggestions Based on Your Reading History",
            font=("Helvetica", 12, "bold")
        ).pack(pady=10)

        ttk.Button(
            frame, text="✨ Get Recommendations", command=self.show_recommendations
        ).pack(pady=10)

        cols = ("Title", "Author", "Category")
        self.recommend_tree = ttk.Treeview(frame, columns=cols, show="headings", height=8)
        for col in cols:
            self.recommend_tree.heading(col, text=col)
            self.recommend_tree.column(col, width=150, anchor="center")
        self.recommend_tree.pack(fill="both", expand=True, padx=10, pady=10)

    # ✅ UNINDENT THIS COMPLETELY so it’s at the same level as `def ai_recommend_tab`
    def show_recommendations(self):
        from ai_features import recommend_books
        try:
            # Get recommended books and reason
            books, reason = recommend_books(self.user_id)

            # Clear old recommendations
            for i in self.recommend_tree.get_children():
                self.recommend_tree.delete(i)

            # Handle empty result
            if not books:
                self.recommend_tree.insert("", "end", values=("No recommendations available", "", ""))
                if hasattr(self, "reason_label"):
                    self.reason_label.config(text="❌ No data available for recommendations.")
                else:
                    self.reason_label = ttk.Label(
                        self.recommend_tree.master,
                        text="❌ No data available for recommendations.",
                        foreground="red"
                    )
                    self.reason_label.pack(pady=5)
                return

            # Insert new results
            for book in books:
                self.recommend_tree.insert("", "end", values=book)

            # Display reason below the table
            if hasattr(self, "reason_label"):
                self.reason_label.config(text=f"💡 {reason}")
            else:
                self.reason_label = ttk.Label(
                    self.recommend_tree.master,
                    text=f"💡 {reason}",
                    foreground="blue"
                )
                self.reason_label.pack(pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load recommendations: {e}")


    # ----------------- BACK TO DASHBOARD -----------------
    def back_to_dashboard(self):
        from Gui.dashboard import DashboardPage
        self.destroy()
        DashboardPage(self.master, self.user_email)
