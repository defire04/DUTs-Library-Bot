from typing import List

from datetime import date
from models.book import Book


def sort_year(book):
    current_year = date.today().year

    if not book.year_of_publication:
        return current_year + 1
    return book.year_of_publication
    


class Sorter:
    @staticmethod
    def sort_by_year(books: List[Book]):
        return sorted(books, key=sort_year)

    @staticmethod
    def sort_by_year_reverse(books: List[Book]):
        return sorted(Sorter.sort_by_year(books)[::-1], key=lambda book: book.year_of_publication is None)

    @staticmethod
    def sort_by_author(books: List[Book]):
        return sorted(books, key=lambda book: book.author)

    @staticmethod
    def sort_by_author_reverse(books: List[Book]):
        return Sorter.sort_by_author(books)[::-1]

    @staticmethod
    def sort_by_title(books: List[Book]):
        return sorted(books, key=lambda book: book.title)

    @staticmethod
    def sort_by_title_reverse(books: List[Book]):
        return Sorter.sort_by_title(books)[::-1]
