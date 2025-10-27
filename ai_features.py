from Db_connect.db_test import create_connection
from Util.search_algorithms import find_similar_books
import random


# ---------------------- USER BOOK RECOMMENDER ----------------------
def recommend_books(user_id):
    """Recommends books to a user based on their rental history."""
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Fetch user's most recent rental (for category + author)
        cursor.execute("""
            SELECT b.category, b.author FROM rentals r
            JOIN books b ON r.book_id = b.book_id
            WHERE r.user_id = %s
            ORDER BY r.rent_date DESC LIMIT 1
        """, (user_id,))
        recent = cursor.fetchone()

        # Get all books (so we can filter)
        cursor.execute("SELECT title, author, category FROM books")
        all_books = cursor.fetchall()

        if recent:
            category, author = recent
            books = find_similar_books(all_books, base_category=category, base_author=author)
            reason = f"Because you read books in '{category}'"
        else:
            # No history — suggest random books
            books = random.sample(all_books, min(3, len(all_books)))
            reason = "Popular picks among readers"

        conn.close()
        return books, reason

    except Exception as e:
        print("AI Recommendation Error:", e)
        return [], "No recommendations available"


# ---------------------- ADMIN AI QUERY ASSISTANT ----------------------
def admin_ai_query(question: str):
    """
    Interprets admin questions and runs analytics queries.
    Returns (headers, data, message).
    """
    question_lower = question.lower().strip()
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # 🔹 TOP RENTED BOOKS
        if "top" in question_lower and "rent" in question_lower:
            cursor.execute("""
                SELECT b.title, COUNT(r.rental_id) AS total_rented
                FROM rentals r
                JOIN books b ON r.book_id = b.book_id
                GROUP BY b.book_id
                ORDER BY total_rented DESC
                LIMIT 5
            """)
            data = cursor.fetchall()
            headers = ["Book Title", "Total Rentals"]
            return headers, data, "📊 Top rented books retrieved successfully!"

        # 🔹 TOP PURCHASED BOOKS
        elif "buy" in question_lower or "purchase" in question_lower:
            cursor.execute("""
                SELECT b.title, COUNT(t.transaction_id) AS total_sales
                FROM transactions t
                JOIN books b ON t.book_id = b.book_id
                GROUP BY b.book_id
                ORDER BY total_sales DESC
                LIMIT 5
            """)
            data = cursor.fetchall()
            headers = ["Book Title", "Total Purchases"]
            return headers, data, "💰 Top purchased books retrieved successfully!"

        # 🔹 MEMBERSHIP DISTRIBUTION
        elif "membership" in question_lower or "member" in question_lower:
            cursor.execute("""
                SELECT membership_type, COUNT(user_id)
                FROM users
                GROUP BY membership_type
            """)
            data = cursor.fetchall()
            headers = ["Membership Type", "Count"]
            return headers, data, "👥 Membership distribution retrieved successfully!"

        # 🔹 TOTAL COUNTS
        elif "count" in question_lower or "total" in question_lower:
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM books")
            total_books = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM rentals")
            total_rentals = cursor.fetchone()[0]
            summary = [
                ("Total Users", total_users),
                ("Total Books", total_books),
                ("Total Rentals", total_rentals)
            ]
            headers = ["Entity", "Count"]
            return headers, summary, "📘 System totals generated successfully!"

        # 🔹 Fallback for unrelated queries
        else:
            return [], [], (
                "🤖 I'm sorry, I can only assist with BookHive-related data.\n"
                "Try asking about rentals, books, purchases, or memberships."
            )

    except Exception as e:
        return [], [], f"⚠️ AI Query Error: {e}"

    finally:
        conn.close()
