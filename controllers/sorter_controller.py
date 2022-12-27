from typing import List

from datetime import date
from models.book import Book
from controllers.book_controller import BookController



def sort_year(book):
    current_year = date.today().year

    if not book.year_of_publication:
        return current_year + 1
    return  book.year_of_publication

class Sorter:
    @staticmethod
    def sort_by_year(books: List[Book]):
        return sorted(books, key=sort_year)

    @staticmethod
    def sort_by_year_reverse(books: List[Book]):
        return Sorter.sort_by_year(books).reverse()


