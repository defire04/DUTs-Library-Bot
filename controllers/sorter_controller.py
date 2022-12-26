from typing import List

from models.book import Book


class Sorter:
    @staticmethod
    def sort_by_year(books: List[Book]):
        return sorted(books, key=lambda book: book.year_of_publication)

    @staticmethod
    def sort_by_year_reverse(books: List[Book]):
        return books.reverse()
