from services.book_service import BookService
from services.query_servise import QueryService


class LibraryController:

    @staticmethod
    def find_books_by_query_id(query_id):
        return BookService.find_book_by_ids(QueryService.find_by_id(query_id).string_books_id)
