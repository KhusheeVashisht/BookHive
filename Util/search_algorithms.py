# Util/searching_algorithms.py
import random

def find_similar_books(all_books, base_category=None, base_author=None):
    """
    Filters and prioritizes books similar to user's past interest.
    - If base_category exists, prefer same category.
    - If base_author exists, prefer same author.
    """
    if not all_books:
        return []

    # Priority 1: Same category
    if base_category:
        category_matches = [b for b in all_books if b[2].lower() == base_category.lower()]
        if category_matches:
            return random.sample(category_matches, min(3, len(category_matches)))

    # Priority 2: Same author
    if base_author:
        author_matches = [b for b in all_books if b[1].lower() == base_author.lower()]
        if author_matches:
            return random.sample(author_matches, min(3, len(author_matches)))

    # Fallback: Random 3 books
    return random.sample(all_books, min(3, len(all_books)))
