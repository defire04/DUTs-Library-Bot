from typing import List

from controllers.category_controller import CategoryController
from models.book import Book
from services.book_service import BookService
from controllers.query_controller import QueryController


class BookController:

    @staticmethod
    def reset_all_table():
        BookService.reset_all_table()

    @staticmethod
    def insert(book):
        BookService.insert(book)

    @staticmethod
    def find_by_title(title):
        return BookController.books_without_duplicates(BookController.result_to_list(BookService.find_by_title(title)))

    @staticmethod
    def find_books_by_book_category(category_id):
        return BookController.result_to_list(BookService.find_books_by_book_category(category_id))

    @staticmethod
    def find_books_by_author(author: str):
        return BookController.result_to_list(BookService.find_books_by_author(author))

    @staticmethod
    def find_by_title_and_create_query(title):
        books = BookController.find_by_title(title)

        if not books:
            return {
                "books": books,
            }
        query_id = QueryController.create(title, books)

        return {
            "books": books,
            "query_id": query_id
        }

    @staticmethod
    def find_by_book_category_and_create_query(category_id):
        books = BookController.find_books_by_book_category(category_id)

        if not books:
            return {
                "books": books,
            }
        query_id = QueryController.create(CategoryController.find_book_category_by_id(category_id).title, books)

        return {
            "books": books,
            "query_id": query_id
        }

    @staticmethod
    def books_without_duplicates(books):
        books_without_duplicates: List[Book] = []
        for book in books:
            if book not in books_without_duplicates:
                books_without_duplicates.append(book)
        return books_without_duplicates

    @staticmethod
    def find_book_by_ids(request_books):
        return BookController.result_to_list(BookService.find_book_by_ids(request_books))

    @staticmethod
    def replace_c():
        BookService.replace_c()

    @staticmethod
    def clean_dataset():
        BookService.clean_dataset()

    @staticmethod
    def finalize():
        BookService.finalize()

    @staticmethod
    def result_to_list(find_result):
        books: List[Book] = []

        for book in find_result:
            books.append(Book.create_book(*book))

        return books
