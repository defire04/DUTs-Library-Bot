from controllers.book_controller import BookController
from controllers.query_controller import QueryController


class LibraryController:

    @staticmethod
    def find_books_by_query_id(query_id):
        return BookController.find_book_by_ids(QueryController.find_by_id(query_id).string_books_id)
