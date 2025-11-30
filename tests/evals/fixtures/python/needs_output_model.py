from typing import Dict


def get_book_details(isbn: str) -> Dict[str, str | int | float]:
    """
    Retrieves book details by ISBN.

    Args:
        isbn: The ISBN of the book.

    Returns:
        Dictionary containing book details.
    """
    return {
        "title": "Hello",
        "author": "World",
        "year": 2024,
        "price": 29.99,
        "publisher": "Amazon",
        "category": "Fiction",
    }
