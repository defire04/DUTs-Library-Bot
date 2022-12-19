from typing import List

from models.book import Book
from services.query_servise import QueryService


class QueryController:

    @staticmethod
    def create(sql: str, books: List[Book]):
        query_id = QueryService.find_by_search_string(sql)
        if query_id is None:
            query_id = QueryController.insert(sql, books)

        return query_id

    @staticmethod
    def insert(sql: str, books: List[Book]):
        string_books_id = []

        for book in books:
            string_books_id.append(str(book.id))

        return QueryService.insert(sql, " ".join(string_books_id))

    @staticmethod
    def find_by_id(query_id):
        return QueryService.find_by_id(query_id)

    @staticmethod
    def finalize():
        QueryService.finalize()

