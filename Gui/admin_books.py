import tkinter as tk
from tkinter import messagebox, ttk
from Db_connect.db_test import create_connection

class AdminBooksPage(tk.Frame):
    def __init__(self, master, dashboard_frame):
        super().__init__(master)
        self.master = master
        self.dashboard_frame = dashboard_frame
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_books()

    def create_widgets(self):
        tk.Label(self, text="📚 Manage Books", font=("Helvetica", 16, "bold")).pack(pady=10)

        # CRUD buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Add Book", command=self.add_book_window).pack(side="left", padx=5)
        tk.Button(button_frame, text="Edit Selected Book", command=self.edit_book_window).pack(side="left", padx=5)
        tk.Button(button_frame, text="Delete Selected Book", command=self.delete_book).pack(side="left", padx=5)
        tk.Button(button_frame, text="← Back to Dashboard", command=self.back_to_dashboard).pack(side="left", padx=5)

        # Treeview to display books
        columns = ("book_id", "title", "author", "category", "available_copies", "price", "rent_per_day")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            header = col.replace("_", " ").title()
            self.tree.heading(col, text=header)
        self.tree.pack(fill="both", expand=True, pady=10)

    def load_books(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT book_id, title, author, category, available_copies, price, rent_per_day FROM books")
            for book in cursor.fetchall():
                self.tree.insert("", "end", values=book)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load books: {e}")

    def add_book_window(self):
        self.book_window("Add Book")

    def edit_book_window(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a book to edit")
            return
        values = self.tree.item(selected, "values")
        self.book_window("Edit Book", values)

    def book_window(self, action, book=None):
        window = tk.Toplevel(self)
        window.title(action)
        window.geometry("400x400")

        labels = ["Title", "Author", "Category", "Available Copies", "Price", "Rent per Day"]
        entries = {}

        for label in labels:
            tk.Label(window, text=f"{label}:").pack(pady=5)
            entry = tk.Entry(window)
            entry.pack(pady=5)
            entries[label] = entry

        if book:
            entries["Title"].insert(0, book[1])
            entries["Author"].insert(0, book[2])
            entries["Category"].insert(0, book[3])
            entries["Available Copies"].insert(0, book[4])
            entries["Price"].insert(0, book[5])
            entries["Rent per Day"].insert(0, book[6])

        def save():
            try:
                title = entries["Title"].get().strip()
                author = entries["Author"].get().strip()
                category = entries["Category"].get().strip()
                copies = int(entries["Available Copies"].get().strip())
                price = float(entries["Price"].get().strip())
                rent_per_day = float(entries["Rent per Day"].get().strip())

                if not (title and author and category):
                    messagebox.showerror("Error", "Title, Author, and Category are required")
                    return

                conn = create_connection()
                cursor = conn.cursor()

                if action == "Add Book":
                    cursor.execute(
                        "INSERT INTO books (title, author, category, available_copies, price, rent_per_day) VALUES (%s, %s, %s, %s, %s, %s)",
                        (title, author, category, copies, price, rent_per_day)
                    )
                elif action == "Edit Book" and book:
                    cursor.execute(
                        "UPDATE books SET title=%s, author=%s, category=%s, available_copies=%s, price=%s, rent_per_day=%s WHERE book_id=%s",
                        (title, author, category, copies, price, rent_per_day, book[0])
                    )

                conn.commit()
                conn.close()
                self.load_books()
                window.destroy()
                messagebox.showinfo("Success", f"{action} successful!")
            except Exception as e:
                messagebox.showerror("Error", f"{action} failed: {e}")

        tk.Button(window, text="Save", command=save).pack(pady=20)

    def delete_book(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a book to delete")
            return
        book_id = self.tree.item(selected, "values")[0]
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this book?")
        if confirm:
            try:
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM books WHERE book_id=%s", (book_id,))
                conn.commit()
                conn.close()
                self.load_books()
                messagebox.showinfo("Success", "Book deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Delete failed: {e}")

    def back_to_dashboard(self):
        self.pack_forget()
        self.dashboard_frame.pack(fill="both", expand=True)
